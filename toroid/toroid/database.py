from tinydb import TinyDB, Query
from toroid import app, warrior
from toroid import warrior_dict_relations as wdr


def get_warrior_db():
    ' Get the DB table in which warriors are stored '
    return TinyDB(app.config['DB_PATH']).table(app.config['DB_WARRIOR_TABLE'])


def purge_warrior_db():
    ' Remove EVERYTHING from the warrior database '
    TinyDB(app.config['DB_PATH']).purge_table(app.config['DB_WARRIOR_TABLE'])


def dbwarrior_to_warrior(dbwarrior):
    ' Convert the data returned by TinyDB into a Warrior object '
    return wdr.dict_to_warrior(dbwarrior)


def warrior_to_dbwarrior(warrior):
    ' Convert a Warrior object into data that TinyDB can store '
    return wdr.warrior_to_dict(warrior)


def list_warriors():
    ' Return a list of all warriors from the database. '
    return map(dbwarrior_to_warrior,
               get_warrior_db().all())


def list_warriors_raw():
    ' Return a list of all warriors from the database, as dbwarriors. '
    return get_warrior_db().all()


def get_warrior_by_name(name):
    ' Return the warrior with the given name, or False if none exists. '
    db = get_warrior_db()
    Warrior = Query()
    try:
        return dbwarrior_to_warrior(db.search(Warrior.name == name)[0])
    except IndexError:
        return False


def get_warrior_by_author(author):
    ' Return the warrior with the given author, or False if none exists. '
    db = get_warrior_db()
    Warrior = Query()
    try:
        return dbwarrior_to_warrior(db.search(Warrior.author == author)[0])
    except IndexError:
        return False


def add_warrior(warrior):
    ' Return the ID of the warrior after inserting it into the database. '
    db = get_warrior_db()
    return db.insert(warrior_to_dbwarrior(warrior))


def delete_warrior_by_name(name):
    ' Delete all warriors with the given name. '
    db = get_warrior_db()
    Warrior = Query()
    db.remove(Warrior.name == name)
