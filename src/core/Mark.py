from enum import Enum


class MarkStatus(Enum):
    ACTIVE = True
    DISACTIVE = False


class Mark:
    mark_desc: str
    balance: int
    card_id: int
    card_desc: str = ""
    has_complete = MarkStatus.ACTIVE

    def __init__(self, mark_desc, card_id, card_desc, balance=0):
        self.mark_desc = mark_desc
        self.card_id = card_id
        self.card_desc = card_desc
        self.balance = balance

    def get_mark_desc(self):
        return self.mark_desc

    def get_card_id(self):
        return self.card_id

    def get_balance(self):
        return self.balance

    def get_card_desc(self):
        return self.card_desc

    def get_complete(self):
        return self.has_complete

    def set_balance(self, new_balance):
        self.balance += new_balance

    def set_card_id(self, new_id):
        self.card_id = new_id

    def set_card_desc(self, new_desc):
        self.card_desc = new_desc

    def set_complete(self, status):
        self.has_complete = status
