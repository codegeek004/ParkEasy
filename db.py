import mysql.connector
import psycopg2
from decouple import config
"""db_config1 = {
        'host' : config('host', cast=str),
        'user' : config('user', cast =str),
        'password' : config('password', cast=str),
        'database' : config('database', cast=str),
        }
"""
DATABASE_URL = config("DATABASE_URL") 
#db = mysql.connector.connect(**db_config1)
db = psycopg.connect(DATABASE_URL)
cursor = db.cursor(buffered=True)




