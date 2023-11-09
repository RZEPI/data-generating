import random

class Equipment:
    def __init__(self, session_id, item_id):
        self.session_id = session_id
        self.item_id = item_id
        self.amount = 1
        self.is_equipped = random.randint(0, 1)

    def __str__(self):
        return f"{self.session_id},{self.item_id},{self.amount},{self.is_equipped}"
