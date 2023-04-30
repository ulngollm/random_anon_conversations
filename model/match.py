class MatchStatus:
    ACTIVE = 0
    CLOSED = 2


class Match:
    def __init__(self, id: int, user_match_id: int) -> None:
        self.id = id
        self.match = user_match_id