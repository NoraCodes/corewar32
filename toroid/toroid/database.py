from tinydb import TinyDB, Query
from toroid import app, warrior


def get_warrior_db():
    ' Get the DB table in which warriors are stored '
    return TinyDB(app.config['DB_PATH']).table(app.config['DB_WARRIOR_TABLE'])


def dbwarrior_to_warrior(dbwarrior):
    ' Convert the data returned by TinyDB into a Warrior object '
    return warrior.Warrior(
        dbwarrior.get("name", ""),
        dbwarrior.get("author", ""),
        dbwarrior.get("source", "")
    )


def warrior_to_dbwarrior(warrior):
    ' Convert a Warrior object into data that TinyDB can store '
    return {
        'name': warrior.name,
        'author': warrior.author,
        'source': warrior.source
    }


def get_warrior_by_name(name):
    ' Return the warrior with the given name, or False if none exists. '
    db = get_warrior_db()
    Warrior = Query()
    try:
        return dbwarrior_to_warrior(db.search(Warrior.name == name)[0])
    except KeyError:
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
