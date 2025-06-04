from faker import Faker
import random
import mysql.connector
from db import db, cursor

fake = Faker()


def generate_payments(num_entries):
    payments = []
    Total_Price = 0 
    modeOfPayment = ''
    for PaymentID in range(1, num_entries):  
     
        TotalPrice = 0 
        mode = ''
        SNo=1
        VehicleID=1
        payments.append((PaymentID, TotalPrice, mode, SNo, VehicleID))
    return payments

def insert_into_mysql_data(payments):
    try:
        print('In try')
        insert_query = '''INSERT INTO payment (PaymentID, TotalPrice, mode, SNo, VehicleID) VALUES (%s, %s, %s, %s,  %s)'''
        cursor.executemany(insert_query, payments)
        print('Successfully executed insert query')
        db.commit()  
    except mysql.connector.Error as e:
        print('In except')
        dbrollback()  
        print(f"Error: {e}")
    finally:
        cursor.close() 
        db.close() 

num_entries = 90 
payment_data = generate_payments(num_entries)
insert_into_mysql_data(payment_data)


