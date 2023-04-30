import sqlite3

class UserManager:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    
    def add(self, user_id: int, default_status: int = 0):
        conn = sqlite3.connect(self.db_name)
        conn.cursor().execute(
            'INSERT INTO users(user_id, status) values(?, ?)', 
            (user_id,default_status,)
        )
        conn.commit()
        conn.close()


    def set_status(self, user_id: int, status: int = 0):
        conn = sqlite3.connect(self.db_name)
        conn.cursor().execute(
            'UPDATE users SET status = ? WHERE user_id = ?', 
            (status, user_id,)
        )
        conn.commit()
        conn.close()


    def find(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        result = conn.cursor().execute(
            'SELECT * from users WHERE user_id = ?', 
            (user_id,)
        ).fetchone()
        conn.close()
        return result
