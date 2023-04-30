from model.user import User, UserStatus

class UserService:
    def __init__(self, state: dict, storage) -> None:
        self.state = state
        self.storage = storage


    def set_freeze(self, user_id: int):    
        self._set_status(user_id, UserStatus.FREEZED)


    def set_active(self, user_id: int):
        self._set_status(user_id, UserStatus.ACTIVE)


    def set_busy(self, user_id: int):
        self._set_status(user_id, UserStatus.BUSY)


    def _set_status(self, user_id: int, status: int):
        self.state[user_id] = status 
        self.storage.set_status(user_id, status)


    def get_status(self, user_id: int) -> int:
        return self.state.get(user_id, UserStatus.NEW)

    
    def find(self, user_id: int) -> User:
        raw_user = self.storage.find(user_id)
        return User(raw_user[1], raw_user[2])


    def authenticate(self, user_id: int) -> User:
        user_status = self.get_status(user_id)
        return User(user_status, user_id)