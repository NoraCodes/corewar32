# Database operations for CoreStore
from corestore import app
from tinydb import TinyDB, where


def add_warrior(warrior):
    'Add a warrior to the database, returning an ID'
    db = TinyDB(app.config['DB_PATH'])
    return db.insert(warrior)

def get_warrior_from_data(name, author, source):
        warrior = { 'name': name,
                    'author': author,
                    'source': source}
        return warrior

def list_warriors():
    db = TinyDB(app.config['DB_PATH'])
    return db.all()
