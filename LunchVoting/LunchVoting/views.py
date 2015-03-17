"""
Routes and views for the flask application.
"""

import os

from sqlite3 import dbapi2 as sqlite3
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, g
from LunchVoting import app, proxy

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('sql/vflv.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def check_auth():
    """Check authorization."""
    return True

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if check_auth(request.form['username'], request.form['password']):
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('voting'))
    # GET
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        logged_in=False,
        error=error)

@app.route('/voting')
def voting():
    if not session.get('logged_in'):
        abort(401)
    return render_template(
             'voting.html',
             title='Voting',
             year=datetime.now().year,
             logged_in=True
            )

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
