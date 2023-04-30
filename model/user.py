class User:
    def __init__(self, status: int, user_id: int) -> None:
        self.status = status
        self.id = user_id


class UserStatus:
    NEW = -1
    ACTIVE = 0
    BUSY = 1
    FREEZED = 2