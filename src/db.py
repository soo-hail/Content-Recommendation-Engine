import os
import psycopg2

from dotenv import load_dotenv

# Load Environment Variables from .env file
load_dotenv()

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB_NAME'),
    user=os.getenv('POSTGRES_DB_USER'),
    password=os.getenv('POSTGRES_DB_PASSWORD'),
    host=os.getenv('POSTGRES_DB_HOST'),
    port=os.getenv('POSTGRES_DB_PORT')
)

cursor = conn.cursor()

# CREATE TABLE TO STORE USER WATCHED-MOVIES(HISTORY)
cursor.execute('''
     CREATE TABLE IF NOT EXISTS user_history (
         indx SERIAL PRIMARY KEY,
         userId INTEGER NOT NULL,
         movieId INTEGER NOT NULL,
         title TEXT NOT NULL,
         rating FLOAT NOT NULL
     );                  
''')

conn.commit()

cursor.close()

conn.close()
