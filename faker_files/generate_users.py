import mysql.connector
from faker import Faker
from db import db, cursor


fake = Faker()

try:
    def generate_fake_users(num_users):
        for userID in range(num_users):
            username = fake.user_name()
            password = fake.password()
            role = 'user'
            SNo = userID 
            login_mode = 'basic-auth'
            insert_query = '''INSERT INTO user(userID, username, password, role, SNo, login_mode) VALUES(%s, %s, %s, %s, %s, %s)'''
            cursor.execute(insert_query, (userID, username, password, role, SNo, login_mode,))
            
            db.commit()
except mysql.connector.Error as e:
    db.rollback()
    print(e)
generate_fake_users(1000)
db.close()
cursor.close()


