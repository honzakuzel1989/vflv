"""
Routes and views for the flask application.
"""

import os

from hashlib import sha256 as sha
from sqlite3 import dbapi2 as sqlite3
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, g
from LunchVoting import app, proxy

def __compute_hash_in_hex(password):
    hash_object = sha(password)
    hex_dig = hash_object.hexdigest()
    return hex_dig

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

def __insert_users():
    db = get_db()
    users_data = app.config['USERS']
    for (user, pwd) in users_data:
        db.execute('insert into users (name, pass) values (?, ?)', [user, __compute_hash_in_hex(pwd)])
    db.commit()
    flash('New users was successfully inserted')

def __insert_pubs():
    db = get_db()
    pubs_data = app.config['PUBS']
    for pub in pubs_data:
        db.execute('insert into pubs (title) values (?)', [pub])
    db.commit()
    flash('New pubs was successfully inserted')

def __get_logged_user():
    return session.get('logged_user')

def __get_current_time_in_s():
    dt_now = datetime.now()
    dt_now_trunc = dt_now.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_now_in_s = int((dt_now_trunc - datetime(1970,1,1)).total_seconds())
    return dt_now_in_s

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('sql/vflv.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

    __insert_users()
    __insert_pubs()

def check_auth(username, password):
    """Check authorization."""
    db = get_db()
    cur = db.execute('select pass from users where name = ?', [username])
    entries = cur.fetchall()

    if len(entries) != 1:
        return (False, 'Invalid username.')

    pass_h = entries[0]['pass']
    verif = pass_h == __compute_hash_in_hex(password)

    return (True, None) if verif else (False, 'Invalid password.')

def get_pubs():
    db = get_db()
    cur = db.execute('select * from pubs')
    entries = cur.fetchall()
    return entries

def get_actual_voting():
    db = get_db()
    cur = db.execute('select * from votings where date=? and user=?', [__get_current_time_in_s(), __get_logged_user()])
    entries = cur.fetchall()
    return entries

def vote(user, voting_items):

    return (True, None)

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
        retval, error = check_auth(request.form['username'], request.form['password'])
        if retval:
            session['logged_user'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('voting'))
    # GET
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        logged_in=False,
        error=error)

@app.route('/voting', methods=['GET', 'POST'])
def voting():
    if not session.get('logged_user'):
        abort(401)
    error = None
    actual_voting = get_actual_voting()

    if request.method == 'POST':
        pass

        pubs = get_pubs()
        voting_items = [(p['id'], request.form[str(p['id'])]) for p in pubs]

        retval, error = vote(session['logged_user'], voting_items)
        if retval:
            flash('You voted')
            return redirect(url_for('voting'))
    # GET
    # TODO: musi se overovat zda uz nehlasoval
    return render_template(
             'voting.html',
             title='Voting',
             year=datetime.now().year,
             logged_in=True,
             pubs=get_pubs(),
             error=error,
             actual_voting=actual_voting
            )

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
