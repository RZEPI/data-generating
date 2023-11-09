from datetime import datetime
from os import path

from Item import Item
from Player import Player
from Session import Session


FIRST_CHECKPOINT = datetime(2020, 1, 1)
SECOND_CHECKPOINT = datetime(2021, 1, 1)
PART_OF_DATA_FOR_CHECKPOINT = 0.2

def make_file(filename):
    return path.join(path.dirname(__file__), f"bulk\{filename}.csv")

def make_files(filename):
    files = []
    for i in range(1,3):
        files.append(make_file(f"{filename}{i}"))
    return files


BASE_FILES = ("basenames.csv", "baseitems.csv")

NAMES_FILE = make_files("names")
ITEMS_FILE = make_files("items")
PLAYERS_FILE = make_files("players")
AVATARS_FILE = make_files("avatars")
SESSIONS_FILE = make_files("sessions")
EQUIPMENTS_FILE = make_files("equipments")


def generate_items():
    item_list = []
    with open(BASE_FILES[1], "r") as file:
        items = file.readlines()
    for item_name in items:
        item_list.append(Item(item_name.strip()))
    return item_list


def make_logins(prefixes, suffixes, names):
    logins = set()
    for prefix in prefixes:
        for name in names:
            for suffix in suffixes:
                logins.add(f"{prefix}{name}{suffix}")
    return logins


def make_pivot(list_len):
    return list_len - int(list_len * PART_OF_DATA_FOR_CHECKPOINT)


def generate_names():
    prefixes = []
    names = []
    suffixes = []
    with open(BASE_FILES[0], "r") as file:
        while (line:=file.readline()):
            line_str = line.replace("\n", "").replace(" ", "")
            prefix, name, suffix = line_str.split(",")
            prefixes.append(prefix)
            names.append(name)
            suffixes.append(suffix)
            
    return make_logins(prefixes, suffixes, names)


def generate_players(names):
    players = []
    for name in names:
        player = Player(name)
        players.append(player)
    return players


def save_all_list_to_file(collection, pivot, filepaths):
    save_to_file(collection[:pivot], filepaths[0])
    save_to_file(collection, filepaths[1])


def save_to_file(collection, filepath):
    with open(filepath, "w") as file:
        for element in collection:
            file.write(str(element) + "\n")


def get_avatars(players):
    avatars = []
    for player in players:
        avatars += player.avatars
    return avatars


names = generate_names()

items = generate_items()
pivot_items = make_pivot(len(items))
save_all_list_to_file(items, pivot_items, ITEMS_FILE)

players = generate_players(names)
players = players[:len(players)//50]
pivot_players = make_pivot(len(players))
save_all_list_to_file(players, pivot_players, PLAYERS_FILE)

avatars = get_avatars(players)
avatars_pivot = make_pivot(len(avatars))
save_all_list_to_file(avatars, avatars_pivot, AVATARS_FILE)

sessions = []
for avatar in avatars:
    for i in range(avatar.session_number):
        if i == 0:
            sessions.append(Session(avatar.id))
        else:
            sessions.append(Session(avatar.id, sessions[-1]))

equipments = []
sessions1 = []
equipments1 = []
for session in sessions:
    if session.start < FIRST_CHECKPOINT:
        sessions1.append(session)
        equipments1 += session.items
    elif session.start < SECOND_CHECKPOINT:
        equipments += session.items
    else:
        sessions.remove(session)

save_to_file(sessions1, SESSIONS_FILE[0])
save_to_file(equipments1, EQUIPMENTS_FILE[0])
save_to_file(sessions, SESSIONS_FILE[1])
save_to_file(equipments, EQUIPMENTS_FILE[1])