import random
from collections import OrderedDict
from datetime import timedelta, datetime
from copy import deepcopy
from Item import Item
from Equipment import Equipment

SESSION_TIME_PROBABILITY = OrderedDict({
    0.42 : (0,60),
    0.25 : (61,120),
    0.16 : (101,200),
    0.07 : (201,300),
    0.04 : (301,400),
    0.03 : (401,500),
    0.02 : (501,600),
    0.01 : (601,900)
})

INTERVAL_BETWEEN_SESSIONS = 7200
GAME_RELEASE_POINT = datetime(2015,1,1)
NOW = datetime.now()
SECONDS_SINCE_RELEASE = int((NOW - GAME_RELEASE_POINT).total_seconds())

class Session:
    class_counter = 0
    def __init__(self, avatar_id,last_session=None):
        if last_session:
            self.generate_session(last_session.end)
            self.level = last_session.level
            self.perks = deepcopy(last_session.perks)
        else:
            first_session_time = random.randint(0, SECONDS_SINCE_RELEASE)
            self.generate_session(GAME_RELEASE_POINT + timedelta(seconds=first_session_time))
            self.level = 1
            self.perks = OrderedDict({
                'strength' : 1,
                'agility' : 1,
                'intelligence' : 1,
                'charisma' : 1,
                'magic' : 1,
                'vitality' : 1
            })
       
        self.avatar_id = avatar_id
        self.id = Session.class_counter
        Session.class_counter += 1
        levels_gained = self.compute_levels_gained()
        self.split_points(levels_gained)
        self.generate_items()            

    def generate_session(self, last_session_end):
        time_between_sessions = random.randint(1, INTERVAL_BETWEEN_SESSIONS)
        time_delta_between_sessions = timedelta(minutes=time_between_sessions)
        self.start = last_session_end + time_delta_between_sessions
        self.time = self.generate_session_time()
        self.end = self.start + timedelta(minutes=self.time)


    def compute_levels_gained(self):
        levels_gained = 0
        draws = (self.time // 30)
        for _ in range(draws):
            if self.level < 20:
                levels_gained += random.randint(0, 3)
            elif self.level < 40:
                levels_gained += random.randint(0, 2)
            elif self.level < 60:
                levels_gained += random.randint(0, 1)
            else:
                if random.random() < 0.3:
                    levels_gained += 1
        self.level += levels_gained
        return levels_gained


    def split_points(self, levels_gained):
        for _ in range(levels_gained):
            perk = random.choice([key for key in self.perks.keys()])
            self.perks[perk] += 1


    def generate_items(self):
        self.items = []
        ids = []
        if self.time > 5:
            items_got = random.randint(1, self.time // 5)
        else:
            items_got = 0
            
        for _ in range(items_got):
            item_id = random.randint(0, Item.class_counter)
            if item_id in ids:
                self.items[ids.index(item_id)].amount += 1
            else:
                self.items.append(Equipment(self.id, item_id))
                ids.append(item_id)


    def perks_to_str(self):
        return_str = ""
        for perk in self.perks.keys():
            return_str += f"{self.perks[perk]},"
        return return_str


    def __str__(self):
        return f"{self.id},{self.start},{self.end},{self.time},{self.avatar_id},{self.perks_to_str()}{self.level}"

    @staticmethod
    def generate_session_time():
        rand_num = random.random()
        probability = 0
        for prob in SESSION_TIME_PROBABILITY:
            probability += prob
            if rand_num < probability:
                time_span = SESSION_TIME_PROBABILITY[prob]
                session_time = random.randint(time_span[0], time_span[1])
                return session_time
            
   