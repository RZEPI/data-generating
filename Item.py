import random

CATEGORIES_AMOUNT = 16

class Item:
    class_counter = 0

    def __init__(self, name):
        self.id = Item.class_counter
        self.name = name
        self.category = random.randint(0, CATEGORIES_AMOUNT-1)
        self.max_amount = random.randint(0, 100)
        self.strength = random.choice([None, random.randint(1, 100)])
        self.speed = random.choice([None, random.randint(1, 100)])
        self.armor = random.choice([None, random.randint(1, 100)])

        Item.class_counter += 1
    

    def __str__(self):
        return f"{self.id},{self.name},{self.category},{self.max_amount},{self.strength},{self.speed},{self.armor}"