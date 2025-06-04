from faker import Faker
import mysql.connector
from db import db,cursor
import random
import re
fake = Faker()

def Slot(num_slots):
    slots = []
    for SlotID in range(num_slots):
        space = 'car'
        price = 13
        slots.append((SlotID, space, price))
    return slots

def InsertIntoMySqlData(slots):
    try:
        insert_query = 'INSERT INTO slots VALUES (%s, %s, %s)'
        
        for entry in slots:
            print(entry)

        cursor.executemany(insert_query, slots)
        db.commit()
    except mysql.connector.Error as e:
        print(e)
        db.rollback()


num_slots = 90
slots_data = Slot(num_slots)
InsertIntoMySqlData(slots_data)
