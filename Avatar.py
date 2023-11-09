from random import choice, randint

CLASSES = ["Warrior", "Mage", "Rogue", "Priest", "Paladin", "Hunter", "Shaman", "Druid", "Warlock"]

class Avatar:
    class_counter = 0
    def __init__(self, player_login):
        self.player_login = player_login
        self.id = Avatar.class_counter
        self.avatar_class = choice(CLASSES)

        self.session_number = randint(1, 1000)
        Avatar.class_counter += 1


    def __str__(self):
        return f"{self.id},{self.player_login},{self.avatar_class}"
        