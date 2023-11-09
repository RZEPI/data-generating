import calendar

from datetime import datetime, timedelta
from random import randint, choice
from os import path
from Types import Types

GAME_RELEASE_POINT = datetime(2015,1,1, 0, 0, 21)
FIRST_CHECKPOINT = datetime(2020, 1, 1, 0, 0)
SECOND_CHECKPOINT = datetime(2021, 1, 1, 0, 0)

FIRST_VERSION = "1.0"

TYPES = [Types.CONTENT, Types.BUGFIX, Types.PERFORMANCE, Types.QUALITY_OF_LIFE]

def add_to_version(version, type):
    version_splited = version.split(".")
    if type == Types.CONTENT:
        return str(int(version_splited[0]) + 1) + "." + version_splited[1]
    else:
        return version_splited[0] + "." + str(int(version_splited[1]) + randint(1, 9))


def randomize_date(last_date):
    last_day = calendar.monthrange(last_date.year, last_date.month)[1]
    end_of_month = datetime(last_date.year, last_date.month, last_day)
    days_remaining = (end_of_month - last_date).days

    if days_remaining < 3:
        return None
    else:
        return last_date + timedelta(days=randint(1, days_remaining), hours=randint(0, 23), minutes=randint(0, 59))   
    

def content_version_life(version, date):
    updates_am = randint(0,4)
    last_update = date
    updates = []
    for _ in range(updates_am):
        update_type = choice(TYPES[1:])
        version = add_to_version(version, update_type)
        if not (update_date := randomize_date(last_update)):
            break
        last_update = update_date
        updates.append((version, update_type,update_date))
    return updates

def make_content_update(last_version, date):
    update = []
    current_version = add_to_version(last_version, Types.CONTENT)
    content_update_date = datetime(year=date.year, month=date.month, day=date.day, hour=randint(0, 23), minute=randint(0, 59))
    update.append((current_version, Types.CONTENT, content_update_date))
    update += content_version_life(current_version, content_update_date)
    return update, current_version


def save_to_file(updates, file_number):
    with open(path.join(path.dirname(__file__), f"updates{file_number}.csv"), "w") as file:
        for update in updates:
            file.write(f"{file_number+2}.{update[0]},{update[1].value},{update[2]}\n")


def add_month(date):
    if date.month == 12:
        return datetime(date.year + 1, 1, 1)
    else:
       return datetime(date.year, date.month + 1, 1)

def run_checkpoint(updates, version, current_date, checkpoint, file_number):
    while current_date < checkpoint:
        update, version = make_content_update(version, current_date)
        updates += update
        current_date = add_month(current_date)
    save_to_file(updates, file_number)
    return updates, version, current_date

current_date = GAME_RELEASE_POINT

updates = []
version  = FIRST_VERSION
upadtes, version, current_date = run_checkpoint(updates, version, current_date, FIRST_CHECKPOINT, 1)
run_checkpoint(updates, version, current_date, SECOND_CHECKPOINT, 2)