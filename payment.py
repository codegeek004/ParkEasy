from flask import redirect, render_template, request, url_for, Blueprint, flash, session
from db import db, cursor
import mysql.connector
from auth import login_required
from datetime import datetime, time
from utils import requires_role
payment = Blueprint('payment', __name__)

@payment.route('/payment')
@login_required
@requires_role('admin')
def display():
    update_query = '''
        UPDATE payment p
        JOIN bookingslot b ON p.PaymentID = b.BSlotID
        SET TotalPrice=Null, Mode=Null
        WHERE b.TimeFrom is Null and b.TimeTo is Null
    '''
    try:
        cursor.execute(update_query)
        db.commit()
    except mysql.connector.Error as e:
        db.rollback()
        flash('Error updating data to null')

    cursor.execute('SELECT * FROM payment')
    db.commit()
    data = cursor.fetchall()

    Null_query = 'SELECT p.PaymentID FROM payment p JOIN bookingslot b on p.PaymentID = b.BSlotID WHERE b.TimeFrom is Null and b.TimeTo is Null'
    cursor.execute(Null_query)
    NullID = cursor.fetchone()

    return render_template('view/payment.html', data=data, NullID=NullID)

@payment.route('/payment/add', methods=['GET', 'POST'])
@login_required
def add_data():
    if request.method == 'POST':
        PaymentID = session.get('VehicleID')
        mode = request.form['mode']

        try:
            fetch_query = '''
                SELECT v.VehicleType, b.TimeFrom, b.TimeTo, b.duration
                FROM payment p   
                JOIN vehicle v on p.PaymentID = v.VehicleID
                JOIN bookingslot b on p.PaymentID = b.BSlotID
                WHERE p.PaymentID=%s
            '''
            cursor.execute(fetch_query, (PaymentID,))
            data = cursor.fetchone()

            if data is None:
                flash('No data found', 'error')
                return redirect(url_for('payment.add_data'))

            VehicleType = data[0]
            TimeFrom = data[1]
            TimeTo = data[2]
            duration = data[3]
            Duration = int(duration)

            print('TimeTo: ', TimeTo,'TimeFrom:', TimeFrom)
            rate = 0
            if VehicleType in ['sedan', 'SUV', 'Hatchback', 'Coupe']:
                rate = 13
            elif VehicleType == '2-Wheeler':
                rate = 8
            elif VehicleType == 'Heavy-Vehicle':
                rate = 15
            elif VehicleType == 'Luxury-Vehicle':
                rate = 18


            print(rate)
            print(duration)
            TotalPrice = rate * Duration 
            print(TotalPrice)
            TotalPrice = float(TotalPrice)
            print(TotalPrice)

            update_query = '''
                UPDATE payment
                SET mode=%s, TotalPrice=%s
                WHERE PaymentID=%s
            '''

            if not TotalPrice:
                flash('No data found','error')

            
            cursor.execute(update_query, (mode, TotalPrice, PaymentID,))
            db.commit()

            # Redirect to generate receipt page after successful update
            return render_template('add/payment.html',duration=duration, TotalPrice=TotalPrice, PaymentID=PaymentID)

        except mysql.connector.Error as e:
            print(e)
            db.rollback()
            flash('Error processing your payment', 'error')
            return redirect(url_for('payment.add_data'))

    return render_template('add/payment.html')



def receipt(PaymentID):
    return render_template('view/GenerateReceipt.html',PaymentID=PaymentID)




@payment.route('/payment/edit/<int:PaymentID>', methods = ['GET','POST'])
@login_required
def edit_data(PaymentID):
    if request.method == 'POST':
        TotalPrice = request.form['TotalPrice']
        Mode = request.form['Mode']
        try:
            update_query = '''UPDATE payment
            SET TotalPrice=%s, Mode=%s
            WHERE PaymentID=%s'''
            cursor.execute(update_query, (TotalPrice, Mode, PaymentID,))
            #flash('Data updated successfully')
            return redirect(url_for('payment.display'))
        except mysql.connector.Error as e:
            db.rollback()
            flash('Error updating data')
    fetch_query = 'SELECT PaymentID, TotalPrice, Mode FROM payment WHERE PaymentID=%s'
    cursor.execute(fetch_query, (PaymentID,))
    db.commit()
    data = cursor.fetchone()
    if data is None:
        flash('No data found')
        return redirect(url_for('payment.display'))
    return render_template('edit/payment.html', data=data)

@payment.route('/payment/delete/<int:PaymentID>', methods = ['GET','POST'])
@login_required
def delete_data(PaymentID):
    if request.method == 'POST':

        try:
            delete_query = 'DELETE FROM payment WHERE PaymentID = %s'
            cursor.execute(delete_query, (PaymentID,))
            db.commit()
            #flash('Data deleted successfully')
            return redirect(url_for('payment.display'))
        except mysql.connector.Error as e:
            db.rollback()
            flash('Error deleting data')
    fetch_query = 'SELECT PaymentID, TotalPrice, Mode FROM payment WHERE PaymentID = %s'
    cursor.execute(fetch_query, (PaymentID,))
    db.commit()
    data = cursor.fetchone()
    if data is None:
        flash('No data found')
        return redirect(url_for('payment.display'))
    return render_template('delete/payment.html',data=data)


@payment.route('/payment/generate_receipt/<int:PaymentID>', methods=['GET', 'POST'])
@login_required


def Generate_Receipt(PaymentID):


    Null_query = '''
        SELECT v.VehicleType, v.VehicleNumber, p.TotalPrice
        FROM vehicle v 
        JOIN bookingslot b ON v.VehicleID = b.BSlotID
        JOIN payment p ON v.VehicleID = p.PaymentID
        WHERE b.TimeFrom is Null AND b.TimeTo is Null
        
    '''
    cursor.execute(Null_query)
    NullID = cursor.fetchall()

    try:
        fetch_query = '''
            SELECT v.VehicleType, v.VehicleNumber, b.date, p.PaymentID, p.TotalPrice, p.Mode, b.TimeFrom, b.TimeTo
            FROM payment p 
            JOIN bookingslot b ON p.PaymentID = b.BSlotID 
            JOIN vehicle v  ON p.PaymentID = v.VehicleID
            WHERE p.PaymentID=%s
        '''
        cursor.execute(fetch_query, (PaymentID,))
        db.commit()
        data = cursor.fetchone()
        print(data)
        # VehicleType, VehicleNumber, ReceiptID, Price, date, Mode, TimeFrom, TimeTo = data

        if data is None:
            flash('Slot not booked. Please book the slot to generate receipt', 'danger')
            return redirect(url_for('payment.display'))


        VehicleType = data[0]
        VehicleNumber = data[1]
        Date = data[2]
        ReceiptID = data[3]
        Price = data[4]
        Mode = data[5]
        TimeFrom = data[6]
        TimeTo = data[7]
        if TimeFrom is None or TimeTo is None:
            flash('Booking slot time data is missing', 'error')
            return redirect(url_for('payment.display'))

        duration = (datetime.strptime(str(TimeTo), '%H:%M:%S') - datetime.strptime(str(TimeFrom), '%H:%M:%S')).seconds / 3600

        rate=0
        if VehicleType == '2-Wheeler':
            rate = 8
        elif VehicleType == 'Sedan':
            rate = 13
        elif VehicleType == 'SUV':
            rate = 13
        elif VehicleType == 'Hatchback':
            rate = 13
        elif VehicleType == 'Heavy-Vehicle':
            rate = 15
        elif VehicleType == 'Luxury-Vehicle':
            rate = 18
        Price = rate * duration
        return render_template('view/GenerateReceipt.html', strftime=datetime.strftime, PaymentID=PaymentID,
                               VehicleType=VehicleType, VehicleNumber=VehicleNumber, date=Date, ReceiptID=ReceiptID, Price=Price, Mode=Mode, TimeFrom=TimeFrom, TimeTo=TimeTo)

    except mysql.connector.Error as e:
        print(e)
        db.rollback()
        flash('Error generating receipt', 'error')
        return redirect(url_for('payment.display'))




