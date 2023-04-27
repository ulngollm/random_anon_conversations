import sqlite3
from match import MatchStatus

from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = os.getenv('DB_NAME')


# пока только с 1 статусом, разрешающим поиск
# todo запретить повтор пар
def search_match(user_id: int, allowed_status: int):
    conn = sqlite3.connect(DB_NAME)
    user = conn.cursor().execute(
        'SELECT user_id from users WHERE user_id != ? and status = ? LIMIT 1', 
        (user_id, allowed_status,)
    ).fetchone()
    if user == None:
        return
    
    conn.cursor().execute(
        'INSERT into matches(user_1_id, user_2_id) values(?,?)',
        (user[0], user_id,)
    )
    conn.commit()
    conn.close()
    return user[0]


def close_current_conversation(user_id: int, status_closed: int = 0, status_active: int = 0):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'UPDATE matches SET status = ? WHERE user_1_id = ? or user_2_id = ? and status = ?', 
        (status_closed, user_id, user_id, status_active,)
    )
    conn.commit()
    conn.close()


def get_active_conversation(user_id: int, status_active: int = 0):
    conn = sqlite3.connect(DB_NAME)
    result = conn.cursor().execute(
        'SELECT user_1_id, user_2_id from matches WHERE status = ? and user_1_id = ? or user_2_id = ?', 
        (status_active, user_id, user_id,)
    ).fetchone()
    conn.close()
    return result