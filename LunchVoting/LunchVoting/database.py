"""
Database.
"""

import os
from flask import g
from sqlite3 import dbapi2 as sqlite3
from LunchVoting import app

def __connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(os.path.join(app.root_path, 'vflv.db'))
    rv.row_factory = sqlite3.Row
    return rv
    
def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = __connect_db()
    return g.sqlite_db
    
def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('sql/vflv.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
