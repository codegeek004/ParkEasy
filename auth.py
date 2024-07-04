from flask import redirect, render_template, url_for, request, session, flash, Blueprint
from flask import current_app, g
import mysql.connector
from db import db, cursor
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
from utils import requires_role
auth = Blueprint('auth', __name__)
secret_key='flaskdev140401020402yhanddhe0eb'
@auth.route('/register')
def register_form():
    return render_template('auth/register.html')

def ValidUser(username):
    # pattern = "^[a-zA-Z][a-zA-Z\s'-]*$"
    pattern = "^[a-zA-Z0-9_.-]+$"
    return re.match(pattern, username)

@auth.route('/register', methods=['POST'])
def register():
    print('register function initiated')
    if request.method == 'POST':
        UserID=request.form.get('UserID')
        username = request.form.get('username')
        #OwnerID = request.form.get('OwnerID')
        VehicleID = session.get('VehicleID')
        OwnerID = session['OwnerID'] 
        password = request.form['password']
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']

        if len(password) > 8:
            flash('Password should not be more than 8 letters', 'error')
        elif len(password) < 6:
            flash('Password cannot be less than 6 letters', 'error')

        if ' ' in username:
            flash('Username cannot contain spaces', 'error')
            return redirect(url_for('auth.register_form'))

        if not ValidUser(username):
            flash('Username cannot start with numbers')
            return redirect(url_for('auth.register_form'))

        #Check if username already exists
        check_user_query = 'SELECT username FROM user WHERE username=%s'
        cursor.execute(check_user_query,(username,))
        db.commit()
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Username is already taken. Please try a different username', 'error')
            return redirect(url_for('auth.register_form'))


        insert_query = '''
            INSERT INTO user(username, password, role) VALUES (%s, %s, 'user')
        '''


        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')


        user_data = (username, hashed_password)

        try:
            cursor.execute(insert_query, user_data)
            db.commit()
            print('User Data added successfully')
        except mysql.connector.Error as e:
            db.rollback()
            print(e)
            flash('Error adding user','error')
            return redirect(url_for('auth.register_form'))

        print(user_data)
        
        try:
            print('Update query k upar')
            update_query = '''
                UPDATE owner o
                SET name=%s, address=%s, contact=%s
                WHERE OwnerID=%s

       '''

            print('Update wale Try mai gaya')
            cursor.execute(update_query, (name, address, contact))
            db.commit()
            rows_affected = cursor.rowcount
            if rows_affected == 0:
                print('No rows were updated.')
            else:
                print(f'Rows updated: {rows_affected}')
            print('Data updated successfully')
        except mysql.connector.Error as e:
            db.rollback()
            print('update wale except ke andar')
            print(e)
            flash('Error adding owner')
            return redirect(url_for('auth.register_form'))
    print('fetch query ke upar')
    fetch_query = '''
        SELECT OwnerID FROM owner WHERE name='', address=''
    '''
    print('fetch query ke niche')
    print(OwnerID)
    
    cursor.execute(fetch_query, (name, address, OwnerID))
    db.commit()
   
    availableSlots = cursor.fetchall()
    availableSlots = [slot[0] for slot in availableSlots]
    return render_template('auth/register.html', availableSlots=availableSlots)



##############################Admin login#############################################
@auth.route('/adminlogin')
def AdminLoginForm():
    return render_template('auth/adminlogin.html')

@auth.route('/adminlogin', methods=['POST'])
def AdminLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        get_user_query = 'SELECT username, password, role FROM Admin WHERE username=%s'
        cursor.execute(get_user_query, (username,))
        userData = cursor.fetchone()

        if len(password) > 8:
            flash('Password should not be more than 8 letters', 'error')

        if userData and password:
            session['username'] = userData[0]
            session['role'] = userData[2]
            print(session['role'])
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('auth/adminlogin.html')
#################################################################################
@auth.route('/login')
def login_form():
    return render_template('auth/login.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(password) > 8:
            flash('Password should not be more than 8 letters', 'error')
        #query to fetch user's hashed password
        get_user_query = 'SELECT username, password FROM user WHERE username=%s'
        cursor.execute(get_user_query,(username,))
        db.commit()
        user_data = cursor.fetchone()
        if user_data and check_password_hash(user_data[1], password):
            session['username'] = user_data[0]
            session['role'] = 'user'
            # flash('login successful', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid username or password', 'error')

        return redirect(url_for('auth.login_form'))
            # return render_template('auth/login.html', message='Invalid username or password', message_type='error')
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


# Login required for authentication
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # if session.get('username'):
        if 'username' in session:
            return view(*args, **kwargs)
        else:
            flash('You are not logged in, Please login to continue', 'error')
            return redirect(url_for('auth.login_form'))
        #chatgpt code
        g.user = session['username']
        return view(*args, **kwargs)
    # return wrapped_view()
    return wrapped_view
###########################
# #################

cursor.execute('SELECT COUNT(*) FROM slots')
slots_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) FROM sensor')
sensor_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) FROM vehicle')
vehicle_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) FROM bookingslot')
bookingslot_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) FROM owner')
owner_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) FROM payment')
payment_count = cursor.fetchone()



####dashboard########
@auth.route('/dashboard')
def dashboard():
    if 'role' in session:
        return render_template('dashboard.html',
                               slots_count = slots_count[0],
                               vehicle_count = vehicle_count[0],
                               bookingslot_count = bookingslot_count[0],
                               sensor_count = sensor_count[0],
                               owner_count = owner_count[0],
                               payment_count = payment_count[0], role=session['role'])

    else:
        return redirect(url_for('auth.login_form'))



