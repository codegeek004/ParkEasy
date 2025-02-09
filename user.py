import mysql.connector
from faker import Faker

# Connect to your MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='parking'
)

cursor = conn.cursor()

# Initialize Faker
fake = Faker()

# Get the current maximum value of SNo
cursor.execute("SELECT MAX(SNo) FROM user")
result = cursor.fetchone()
current_max_sno = result[0] if result[0] is not None else 0

# Define the range of UserID to insert
start_user_id = 0  
end_user_id = 1000

# Insert new records
for user_id in range(start_user_id, end_user_id + 1):
    username = fake.user_name()
    password = fake.password()
    role = 'user'  # or any role you want to assign
    sno = current_max_sno + (user_id - start_user_id + 1)

    # Insert the new record with the current UserID and incremented SNo
    cursor.execute("""
        INSERT IGNORE INTO user (UserID, username, password, role, SNo)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, username, password, role, sno))

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

