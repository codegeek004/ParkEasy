from faker import Faker
import random
import mysql.connector

# Establishing the connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',  # Should be 'user' instead of 'username'
    password='root',
    database='parking'
)
cursor = conn.cursor()  # Fix: add parentheses to call the method

fake = Faker()


def generate_payments(num_entries):
    payments = []
    Total_Price = 0 
    modeOfPayment = ''
    for PaymentID in range(1, num_entries):  # Fix: iterate exactly num_entries times
     
        TotalPrice = 0 
        mode = ''
        SNo=1
        VehicleID=1
        payments.append((PaymentID, TotalPrice, mode, SNo, VehicleID))
    return payments

def insert_into_mysql_data(payments):
    try:
        print('In try')
        insert_query = '''INSERT IGNORE  INTO payment (PaymentID, TotalPrice, mode, SNo, VehicleID) VALUES (%s, %s, %s, %s,  %s)'''
        cursor.executemany(insert_query, payments)
        print('Successfully executed insert query')
        conn.commit()  # Fix: commit the connection, not the cursor
    except mysql.connector.Error as e:
        print('In except')
        conn.rollback()  # Roll back the transaction in case of error
        print(f"Error: {e}")
    finally:
        cursor.close()  # Close cursor after operations
        conn.close()  # Close connection after operations

num_entries = 90 
payment_data = generate_payments(num_entries)
insert_into_mysql_data(payment_data)

