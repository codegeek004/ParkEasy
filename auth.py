from flask import redirect, render_template, url_for, request, session, flash, Blueprint
from flask import current_app, g
import mysql.connector
from db import db, cursor
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
from utils import requires_role
import requests
from authlib.integrations.flask_client import OAuth
from flask import current_app as app
from oauth_config import google

auth = Blueprint('auth', __name__)

# Renders the register form
@auth.route('/register')
def register_form():
	return render_template('auth/register.html')

# Regex for valid username
def ValidUser(username):
	pattern = "^[A-z|0-9]"
	return re.match(pattern, username)

# Regex for valid contact
def ValidContact(contact):
	pattern = "^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$"
	return re.match(pattern, contact)

# Regex for valid password
def ValidPassword(password):
	pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
	return re.match(pattern, password)

# Regex for valid name
def ValidName(name):
	pattern = "^[A-z]"
	return re.match(pattern, name)

# Regex for valid address
def ValidAddress(address):
	pattern = "[0-9|A-z]"
	return re.match(pattern, address)

@auth.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		session['username'] = username
		password = request.form['password']
		name = request.form['name']
		address = request.form['address']
		contact = request.form['contact']
		S_No = request.form['SNo']

		if len(password) > 15:
			flash('Password is too long', 'error')
			return redirect(url_for('auth.register_form'))

		elif len(password) < 6:
			flash('Password should include minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character', 'error')
			return redirect(url_for('auth.register_form'))

		if ' ' in username:
			flash('Username cannot contain spaces', 'error')
			return redirect(url_for('auth.register_form'))

		if not ValidUser(username):
			flash('Username cannot contain special characters', 'error')
			return redirect(url_for('auth.register_form'))

		if not ValidContact(contact):
			flash('Contact is not valid', 'error')
			return redirect(url_for('auth.register_form'))

		if not ValidPassword(password):
			flash("Password should include minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character", "error")
			return redirect(url_for('auth.register_form'))

		if not ValidName(name):
			flash("Name should not contain special characters.", 'error')
			return redirect(url_for('auth.register_form'))

		if not ValidAddress(address):
			flash("Address should not contain special characters", "error")
			return redirect(url_for('auth.register_form'))

		# Check if user is already logged in
		check_user_query = 'SELECT username FROM user WHERE username=%s'
		cursor.execute(check_user_query, (username,))
		db.commit()
		existing_user = cursor.fetchone()
		if existing_user:
			flash('Username is already taken. Please try a different username', 'error')
			return redirect(url_for('auth.register_form'))

		try:
			maxSNo = 'SELECT MAX(SNo) FROM user'
			cursor.execute(maxSNo)
			db.commit()
			result = cursor.fetchone()
			maxS_No = result[0]
			# owner_id = result[1]
			incrementedSNo = maxS_No + 1
			session['incrementedSNo'] = incrementedSNo
			hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

			insert_query = '''
				INSERT INTO user(username, password, role, SNo) VALUES (%s, %s, 'user', %s)
			'''
			user_data = (username, hashed_password, incrementedSNo)
			cursor.execute(insert_query, user_data)
			db.commit()
		except mysql.connector.Error as e:
			db.rollback()
			flash('Error inserting user', 'error')
			return redirect(url_for('auth.register_form'))

		try:
			incrementedSNo = session.get('incrementedSNo')
			insert_query = '''
				INSERT INTO owner (name, address, contact, SNo) 
				VALUES(%s, %s, %s, %s)
			'''
			cursor.execute(insert_query, (name, address, contact, incrementedSNo))
			db.commit()
			return redirect(url_for('auth.login'))
		except mysql.connector.Error as e:
			db.rollback()
			print(e)
			flash('Error adding owner data', 'danger')

	return render_template('auth/register.html')

############################## Admin login #############################################
@auth.route('/adminlogin')
def AdminLoginForm():
	return render_template('auth/adminlogin.html')

@auth.route('/adminlogin', methods=['POST', 'GET'])
def AdminLogin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		role = 'admin'

		get_user_query = "SELECT username, password, role, SNo FROM Admin WHERE username=%s"
		cursor.execute(get_user_query, (username,))
		db.commit()
		userData = cursor.fetchone()

		if len(password) > 8:
			flash('Password should not be more than 8 letters', 'error')

		if userData and check_password_hash(userData[1], password): 
			session['username'] = userData[0]
			session['role'] = userData[2]
			return redirect(url_for('auth.admin_dashboard'))
		else:
			flash('Invalid username or password', 'danger')

	username = session.get('username')
	db.commit()
	return render_template('auth/adminlogin.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if len(password) > 25:
			flash('Password should not be more than 8 characters', 'error')
			return redirect(url_for('auth.login'))

		fetch_query = "SELECT username, password, SNo FROM user WHERE username=%s"
		cursor.execute(fetch_query, (username,))
		user_data = cursor.fetchone()
		db.commit()

		if user_data and check_password_hash(user_data[1], password):
			session['username'] = user_data[0]
			session['role'] = 'user'

			if session['role'] == 'admin':
				return redirect(url_for('auth.dashboard'))
			else:
				fetch_query = '''
					SELECT p.mode FROM Payment p
					INNER JOIN user u ON p.SNo = u.SNo 
					WHERE u.username = %s and p.mode <> ''
				'''
				cursor.execute(fetch_query, (username,))
				db.commit()
				data = cursor.fetchone()
				if data is not None:
					return redirect(url_for('index'))
				else:
					return redirect(url_for('index'))
		else:
			flash('Invalid username or password', 'error')
			return redirect(url_for('auth.login'))

	return render_template('auth/login.html')

@auth.route('/login')
def login_form():
	return render_template('auth/login.html')  

@auth.route('/logout')
def logout():
	session.clear()
	return render_template('index.html')

# This ensures that there is no access to website without login
def login_required(view):
	@wraps(view)
	def wrapped_view(*args, **kwargs):
		if 'username' in session:
			return view(*args, **kwargs)
		else:
			flash('You are not logged in, Please login to continue', 'error')
			return redirect(url_for('auth.login_form'))

		g.user = session['username']
		return view(*args, **kwargs)

	return wrapped_view

cursor.execute('SELECT COUNT(*) FROM slots')
slots_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) FROM sensor')
sensor_count = cursor.fetchone()

cursor.execute("SELECT COUNT(*) FROM vehicle WHERE VehicleType <> ''")
vehicle_count = cursor.fetchone()

cursor.execute("SELECT COUNT(*) FROM bookingslot WHERE duration <> '' ")
bookingslot_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) FROM owner')
owner_count = cursor.fetchone()

cursor.execute("SELECT COUNT(*) FROM payment WHERE TotalPrice <> 0")
payment_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) FROM allotment')
history_count = cursor.fetchone()

@auth.route('/admin')
@requires_role('admin')
def admin_dashboard():
	if 'role' in session:
		return render_template('dashboard.html',
							   slots_count=slots_count[0],
							   vehicle_count=vehicle_count[0],
							   bookingslot_count=bookingslot_count[0],
							   sensor_count=sensor_count[0],
							   owner_count=owner_count[0],
							   history_count=history_count[0],
							   payment_count=payment_count[0], role=session['role'])

	else:
		return redirect(url_for('auth.login_form'))


@auth.route('/user/dashboard')
@login_required
@requires_role('user')
def dashboard():
	username = session.get('username')
	if request.method == 'GET':
		try:
			fetch_query = '''
				 SELECT u.username, o.name, o.contact, o.address  
				 from user u  
				 inner join owner o on o.SNo = u.SNo  
				 where username=%s
			'''
			cursor.execute(fetch_query, (username,))
			user = cursor.fetchone()
			print(user)
			db.commit()
			return render_template('dashboard.html', user=user, role=session['role'])
		except Exception as e:
			print('e', e)

			flash(f'There is some issue with your data!{e}', 'error')
			return redirect(url_for('auth.login_form'))

	return render_template('user/dashboard.html')


@auth.route('/login/google/')
def google_login():
	redirect_uri = "http://127.0.0.1:5000/auth"
	return google.authorize_redirect(redirect_uri)

@auth.route('/auth')
def google_auth():
	print('inside googla auth')
	token = google.authorize_access_token()
	nonce = token.get('nonce')
	user = google.parse_id_token(token, nonce=nonce)
	print(user)
	name = user.get('name')
	give_name = user.get('given_name')
	family_name = user.get('family_name')
	email = user.get('email')
	if give_name and family_name:
		username = give_name + '_' + family_name
	else:
		username = give_name
	login_mode = 'google-auth'
	
	session['user'] = user
	session['username'] = username
	

	try:
		print('fetch qury wala try')
		fetch_query = '''
			SELECT u.username, u.login_mode, u.SNo, o.name, o.address, o.contact, o.SNo 
			FROM user u INNER JOIN owner o 
			ON u.SNo=O.SNo
			WHERE u.username=%s
		'''
		cursor.execute(fetch_query, (username,))
		data = cursor.fetchone()
	except Exception as e:
		print('fetch query wala none', e)
		
	if data is None:
		print('data is none, fetch Sno')
		try:
			cursor.execute('SELECT MAX(SNo) FROM user')
			maxSNo = cursor.fetchone()
			maxSNo = maxSNo[0]
			incrementedSNo = maxSNo+1
		
		except mysql.connector.Error as e:
			print(e)
		
		try:
			print('insert query of user')

			insert_user_query = '''
				INSERT INTO user(username, SNo, login_mode) VALUES(%s, %s, %s)
			'''
			cursor.execute(insert_user_query, (username, incrementedSNo, login_mode,))
			db.commit()
		except Exception as e:
			print('Error adding oauth user data')


		try:
			print('insert query of owner')
			insert_owner_query = '''
				INSERT INTO owner(name, SNo, email) VALUES(%s, %s, %s)
			'''
			cursor.execute(insert_owner_query, (name, incrementedSNo, email,))
			db.commit()
		except mysql.connector.Error as e:
			print('Error adding owner oauth data')

		return redirect(url_for('auth.insert_owner_details'))
	elif data is not None:
		address = data[4]
		contact = data[5]
		print('address', address)
		print('contact', contact)
		if address is None:
			print('address aur contact None mai gaya')
			return redirect(url_for('auth.insert_owner_details'))
		if contact is None:
			print('address aur contact None mai gaya')
			return redirect(url_for('auth.insert_owner_details'))



	return redirect(url_for('index'))

@auth.route('/owner-details/add', methods = ['GET','POST'])
def insert_owner_details():
	print('inside insert_owner_details')
	if request.method == 'POST':
		address = request.form['address']
		contact = request.form['contact']
  
		try:
			username = session.get('username')
			print('username', username)
			fetch_query = '''
				SELECT SNo from user where username=%s
			'''
			cursor.execute(fetch_query, (username,))
			db.commit()
			SNo = cursor.fetchone()
		except Exception as e:
			print('fetch query wala', e)
			flash('Error adding data', 'error')
			return redirect(url_for('index'))

		if SNo is not None:
			SNo = SNo[0]
			try:
				print('address', address)
				print('contact', contact)
				insert_query = '''
				UPDATE owner set address=%s, contact=%s where SNo=%s
				'''
				cursor.execute(insert_query, (address,contact,SNo,))
				db.commit()
				return redirect(url_for('index'))
			except mysql.connector.Error as e:
				print(e)
				flash('Error adding data', 'Error')
		else:
			try:
				cursor.execute('SELECT MAX(SNo) FROM user')
				maxSNo = cursor.fetchone()
				maxSNo = maxSNo[0]
				incrementedSNo = maxSNo+1
			
			except mysql.connector.Error as e:
				print(e)

			try:
				insert_query = '''
					INSERT INTO owner(address, contact, SNo) VALUES (%s, %s, %s)
				'''
				cursor.execute(insert_query, (address,contact,incrementedSNo,))
				db.commit()
				return redirect(url_for('index'))
			except mysql.connector.Error as e:
				print(e)
				flash('Error adding data', 'Error')


		
	return render_template('add/insert_owner_details.html')


