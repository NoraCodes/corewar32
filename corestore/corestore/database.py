# Database operations for CoreStore
from corestore import app
from tinydb import TinyDB, where, Query


class WarriorExistsWithThatNameException (Exception):
    pass


class WarriorExistsWithThatAuthorException (Exception):
    pass


def add_warrior(warrior):
    'Add a warrior to the database, returning an ID'
    db = TinyDB(app.config['DB_PATH'])
    return db.insert(warrior)


def warrior_exists(warrior):
    db = TinyDB(app.config['DB_PATH'])
    Warrior = Query()
    if len(db.search(Warrior.name == warrior['name'])) > 0:
        raise WarriorExistsWithThatNameException
    if len(db.search(Warrior.author == warrior['author'])) > 0:
        raise WarriorExistsWithThatAuthorException
    return True


def get_warrior_from_data(name, author, source):
    warrior = {'name': name,
               'author': author,
               'source': source}
    return warrior


def list_warriors():
    db = TinyDB(app.config['DB_PATH'])
    return db.all()
