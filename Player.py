from datetime import timedelta, date
import random
from Avatar import Avatar

MAX_AGE = 60
MIN_AGE = 16

PASS_MIN_LEN = 8
PASS_MAX_LEN = 20

COUNTRIES = [ "France", "USA", "UK", "Canada", "Australia", "China", "Turkey", "Germany", "Italy", "Spain", "Poland", "Japan", "Russia", "Brazil", "Mexico", "India", "Indonesia"]
NAMES = [ "John", "Josh", "Jane", "Juan", "Xin", "San", "Merry", "Peter", "Paul", "Jack", "Tom", "Jerry", "Marry", "Anna", "Maria", "Kate", "Alex", "Alexandra", "Sandra", "Sandy", "Samantha", "Sam", "Sara", "Sarah", "Sally", "Sonia", "Sofia", "Sofie", "Sophie", "Sophia", "Zack", "Luke", "Lucas", "Lucy", "Lucie", "Lily"]
SURNAMES = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Yin", "Ali", "Lee", "Wang", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou", "Xu", "Sun", "Ma", "Zhu", "Hu", "Gao", "Lin", "He", "Guo"]
class Player:
    def __init__(self, login):
        self.login = login
        self.passoword = self.generate_password()
        self.gender = random.randint(0, 2)
        self.email = f"{login}@mail.com"
        self.set_name()
        self.set_birthday()
        self.set_country()
        self.generate_avatars()

    def set_name(self):
        self.name = random.choice(NAMES)
        self.surname = random.choice(SURNAMES)

    def set_birthday(self):
        player_age = random.randint(MIN_AGE, MAX_AGE)
        player_birthday = random.randint(1, 365)
        self.birthday = date.today() - timedelta(days=player_birthday+player_age*365)
    
    def set_country(self):
        self.country = random.choice(COUNTRIES)

    def generate_password(self):
        str_to_draw = ['0123456789', '!@#$%^&*()-=_+', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz']
        self.password = ''

        def draw_from_str(str, draws):
           self.password += ''.join(random.choice(str) for _ in range(draws))
        
        for draw_str in str_to_draw:
           draw_from_str(draw_str, random.randint(1, 3))

        password_len = len(self.password)
        last_draws = random.randint(PASS_MIN_LEN - password_len, PASS_MAX_LEN - password_len)
        draw_from_str(str_to_draw[-1], last_draws)    


    def generate_avatars(self):
        self.avatars = []
        avatars_amount = random.randint(1, 3)
        for _ in range(avatars_amount):
            self.avatars.append(Avatar(self.login))

    
    def __str__(self):
        return f"{self.login},{self.password},{self.email},{self.gender},{self.birthday},{self.name},{self.surname},{self.country}"