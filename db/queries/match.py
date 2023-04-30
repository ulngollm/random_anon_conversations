import sqlite3
from model.match import MatchStatus


# пока только с 1 статусом, разрешающим поиск
# todo запретить повтор пар
class MatchManager:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
    

    def search_match(self, user_id: int, allowed_status: int):
        conn = sqlite3.connect(self.db_name)
        user = conn.cursor().execute(
            'SELECT user_id from users WHERE user_id != ? and status = ? LIMIT 1', 
            (user_id, allowed_status,)
        ).fetchone()

        conn.commit()
        conn.close()
        return user


    def open_conversation(self, user_ids: tuple) -> int:
        conn = sqlite3.connect(self.db_name)
        id = conn.cursor().execute(
            'INSERT into matches(user_1_id, user_2_id) values(?,?)',
            user_ids
        ).lastrowid
        conn.commit()
        conn.close()
        return id
        
    
    def close_current_conversation(self, conversation_id: int, status_closed: int = MatchStatus.CLOSED):
        conn = sqlite3.connect(self.db_name)
        conn.cursor().execute(
            'UPDATE matches SET status = ? WHERE id = ?', 
            (status_closed, conversation_id,)
        )
        conn.commit()
        conn.close()


    def get_active_conversation(self, user_id: int, status_active: int = MatchStatus.ACTIVE):
        conn = sqlite3.connect(self.db_name)
        result = conn.cursor().execute(
            'SELECT * from matches WHERE status = ? and (user_1_id = ? or user_2_id = ?)', 
            (status_active, user_id, user_id,)
        ).fetchone()
        conn.close()
        return result