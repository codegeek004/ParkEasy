from faker import Faker
import mysql.connector
import random
import re
fake = Faker()

conn = mysql.connector.connect(
        host = 'localhost',
        username = 'root',
        password = 'root',
        database = 'parking')
cursor = conn.cursor()

def Slot(num_slots):
    slots = []
    for SlotID in range(0, 80):
        space = 'Heavy Vehicle'
        price = 13
        slots.append((SlotID, space, price))
    return slots

def InsertIntoMySqlData(slots):
    try:
        update_query = 'INSERT IGNORE INTO slots VALUES (%s, %s, %s)'
        
        for entry in slots:
            print(entry)

        cursor.executemany(insert_query, slots)
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
        conn.rollback()


num_slots = 90
slots_data = Slot(num_slots)
InsertIntoMySqlData(slots_data)
        











