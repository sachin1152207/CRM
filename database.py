import sqlite3
from flask import g
from config import DATABASE

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # for dict-like access
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
