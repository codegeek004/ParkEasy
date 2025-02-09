import random
from datetime import time, date
import mysql.connector

def generate_time_pairs(n):
    time_pairs = []
    for _ in range(n):
        hour_from = random.randint(0, 23)
        minute_from = random.randint(0, 59)
        second_from = random.randint(0, 59)
        time_from = time(hour_from, minute_from, second_from)
        
        total_seconds_from = hour_from * 3600 + minute_from * 60 + second_from
        remaining_seconds = 24 * 3600 - total_seconds_from - 1
        
        if remaining_seconds >= 3600:
            added_seconds = random.randint(3600, remaining_seconds)  # At least 1 hour
        else:
            added_seconds = remaining_seconds  # Use the remaining time
        
        total_seconds_to = total_seconds_from + added_seconds
        
        hours_to = total_seconds_to // 3600
        minutes_to = (total_seconds_to % 3600) // 60
        seconds_to = total_seconds_to % 60
        time_to = time(hours_to, minutes_to, seconds_to)
        
        # Compute duration in hours and minutes
        duration_hours = added_seconds // 3600
        duration_minutes = (added_seconds % 3600) // 60
        duration_str = f"{duration_hours} hour{'s' if duration_hours != 1 else ''}"
        if duration_minutes > 0:
            duration_str += f" {duration_minutes} min"

        time_pairs.append((time_from, time_to, duration_str))
    return time_pairs

# Generate time slots for BSlotID 0 to 90 (91 entries)
time_pairs = generate_time_pairs(91)

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'parking'
}

try:
    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    VehicleID = 1  # Assuming a static VehicleID for all

    # Insert query template
    insert_query = """
        INSERT IGNORE INTO bookingslot (BSlotID, Date, TimeFrom, TimeTo, duration, VehicleID)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    insert_date = date(2004, 11, 14)  # Change to date.today() for current date

    # Insert data from BSlotID 0 to 90
    for bslot_id, (time_from, time_to, duration) in enumerate(time_pairs, start=1):
        cursor.execute(insert_query, (bslot_id, insert_date, time_from, time_to, duration, VehicleID))

    # Commit changes
    connection.commit()
    print("Data inserted successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close connections
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()

