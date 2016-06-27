# Database operations for CoreStore
from corestore import app
from tinydb import TinyDB, where

def add_warrior(warrior):
    'Add a warrior to the database, returning an ID'
    db = TinyDB(app.config['DB_PATH'])
    return db.insert(warrior)

def list_warriors():
    db=TinyDB(app.config['DB_PATH'])
    return db.all()
