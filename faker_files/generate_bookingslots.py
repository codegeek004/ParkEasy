import random
from datetime import time, date
import mysql.connector
from db import db,cursor
def generate_time_pairs(n):
    time_pairs = []
    for _ in range(1,n):
        hour_from = random.randint(0, 23)
        minute_from = random.randint(0, 59)
        second_from = random.randint(0, 59)
        time_from = time(hour_from, minute_from, second_from)
        
        total_seconds_from = hour_from * 3600 + minute_from * 60 + second_from
        remaining_seconds = 24 * 3600 - total_seconds_from - 1
        
        if remaining_seconds >= 3600:
            added_seconds = random.randint(3600, remaining_seconds)  
        else:
            added_seconds = remaining_seconds  
        
        total_seconds_to = total_seconds_from + added_seconds
        
        hours_to = total_seconds_to // 3600
        minutes_to = (total_seconds_to % 3600) // 60
        seconds_to = total_seconds_to % 60
        time_to = time(hours_to, minutes_to, seconds_to)
        
        duration_hours = added_seconds // 3600
        duration_minutes = (added_seconds % 3600) // 60
        duration_str = f"{duration_hours} hour{'s' if duration_hours != 1 else ''}"
        if duration_minutes > 0:
            duration_str += f" {duration_minutes} min"

        time_pairs.append((time_from, time_to, duration_str))
    return time_pairs

time_pairs = generate_time_pairs(90)

try:
    VehicleID = 1 

    insert_query = """
        INSERT INTO bookingslot (BSlotID, Date, TimeFrom, TimeTo, duration, VehicleID)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    insert_date = date(2004, 11, 14)  

    for bslot_id, (time_from, time_to, duration) in enumerate(time_pairs, start=1):
        cursor.execute(insert_query, (bslot_id, insert_date, time_from, time_to, duration, VehicleID))

    db.commit()
    print("Data inserted successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

db.close()
cursor.close()
