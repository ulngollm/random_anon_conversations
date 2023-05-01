from db.queries.match import MatchManager
from model.user import UserStatus
from model.match import MatchStatus, Match


class MatchService:
    def __init__(self, storage: MatchManager) -> None:
        self.cache = dict()
        self.storage = storage


    def get_current_match(self, user_id: int) -> Match:
        match =  self.cache.get(user_id)
        if match != None:
            return match

        open_conversation = self.storage.get_active_conversation(user_id)
        match_id = open_conversation[1] if open_conversation[1] != user_id else open_conversation[2]
        conv_id = open_conversation[0]
        match = Match(conv_id, match_id)

        self.cache[user_id] = Match(conv_id, match_id)
        self.cache[match_id] = Match(conv_id, user_id)
        return match
        
    

    def open_conversation(self, user_id1, user_id2):
        conv_id = self.storage.open_conversation(user_ids=(user_id1, user_id2))
        self.cache[user_id1] = Match(conv_id, user_id2)
        self.cache[user_id2] = Match(conv_id, user_id1)


    def close_conversation(self, match: Match):
        self.storage.close_current_conversation(match.id)
        match_1 = self.cache.pop(match.match)
        conversation = self.cache.pop(match_1.match)


    def search(self, user_id: int):
        user = self.storage.search_match(user_id, UserStatus.ACTIVE)
        if user == None:
            return
        
        return user[0]