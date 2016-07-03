# Database operations for CoreStore
from corestore import app
from tinydb import TinyDB, where, Query


class WarriorExistsWithThatNameException (Exception):
    pass


class WarriorExistsWithThatAuthorException (Exception):
    pass


def open_warrior_database():
    'Get an object from which warriors can be recovered.'
    db = TinyDB(app.config['DB_PATH'])
    table = db.table(app.config['DB_WARRIOR_TABLE'])
    return table


def add_warrior(warrior):
    'Add a warrior to the database, returning an ID'
    db = open_warrior_database()
    return db.insert(warrior)


def get_warrior_by_id(id):
    db = open_warrior_database()
    return db.get(eid=id)


def get_warrior_by_name(name):
    db = open_warrior_database()
    Warrior = Query()
    return db.search(Warrior.name == name)[0]


def remove_warrior_by_name(name):
    db = open_warrior_database()
    Warrior = Query()
    return db.remove(Warrior.name == name)


def warrior_exists(warrior):
    db = open_warrior_database()
    Warrior = Query()
    if len(db.search(Warrior.name == warrior['name'])) > 0:
        raise WarriorExistsWithThatNameException
    if len(db.search(Warrior.author == warrior['author'])) > 0:
        raise WarriorExistsWithThatAuthorException
    return True


def get_warrior_from_data(name, author, source):
    warrior = {'name': name.strip("\r"),
               'author': author.strip("\r"),
               'source': source}
    return warrior


def list_warriors():
    db = open_warrior_database()
    return db.all()
