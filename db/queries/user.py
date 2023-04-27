import sqlite3


from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = os.getenv('DB_NAME')


def add(user_id: int, default_status: int = 0):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'INSERT INTO users(user_id, status) values(?, ?)', 
        (user_id,default_status,)
    )
    conn.commit()
    conn.close()


def set_status(user_id: int, status: int = 0):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'UPDATE users SET status = ? WHERE user_id = ?', 
        (status, user_id,)
    )
    conn.commit()
    conn.close()


def find(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    result = conn.cursor().execute(
        'SELECT * from users WHERE user_id = ?', 
        (user_id,)
    ).fetchone()
    conn.close()
    return result
