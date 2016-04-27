"""
Database.
"""

import os

from flask import g
from sqlite3 import dbapi2 as sqlite3
from LunchVoting import app

def __connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
    
def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = __connect_db()
        if not os.path.getsize(app.config['DATABASE']):
            __init_db(g.sqlite_db)
        __try_update_db(g.sqlite_db)
    return g.sqlite_db
    
def __init_db(db):
    """Initializes the database."""
    with app.open_resource('sql/vflv.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print(' * Initialising the database')

def __try_update_db(db):
    """Updates the database."""
    required_version = app.config['DATABASE_VERSION']
    # v1 is default (initial version) created by vflv.sql
    # u1 updates database from v1 to v2
    for v in range(2, required_version + 1):
        sql_file_name = 'sql/vflv.u%d.sql' % (v-1)
        if os.path.exists('LunchVoting/%s' % sql_file_name):
            with app.open_resource(sql_file_name, mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
            print(' * Updating the database to v%d' % v)



