import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
conn = sqlite3.connect(DB_NAME)


conn.cursor().execute('''
    CREATE TABLE users
    (   
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        status INTEGER DEFAULT 0
    )
''')

conn.commit()
conn.close()