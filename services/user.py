from config import state
from model.user import User, UserStatus
from db.queries import user as user_storage

class UserService:
    def __init__(self, state: dict) -> None:
        self.state = state


    def set_freeze(self, user_id: int):    
        self._set_status(user_id, UserStatus.FREEZED)


    def set_active(self, user_id: int):
        self._set_status(user_id, UserStatus.ACTIVE)


    def set_busy(self, user_id: int):
        self._set_status(user_id, UserStatus.BUSY)


    def _set_status(self, user_id: int, status: int):
        self.state[user_id] = status 
        user_storage.set_status(user_id, status)


    def get_status(self, user_id: int) -> int:
        return self.state[user_id]

    
    def find(self, user_id: int) -> User:
        raw_user = user_storage.find(user_id)
        return User(raw_user[1], raw_user[2])


    def authenticate(self, user_id: int) -> User:
        user_status = self.get_status(user_id)
        return User(user_status, user_id)