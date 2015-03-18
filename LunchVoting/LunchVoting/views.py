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

def check_auth(username, password):
    """Check authorization"""
    db = get_db()
    cur = db.execute('select pass from users where name=?', [username])
    entries = cur.fetchall()

    if len(entries) != 1:
        return (False, 'Invalid username')

    pass_h = entries[0]['pass']
    verif = pass_h == __compute_hash_in_hex(password)

    return (True, None) if verif else (False, 'Invalid password')

def get_pubs():
    db = get_db()
    cur = db.execute('select * from pubs')
    entries = cur.fetchall()
    return entries

def get_actual_voting():
    db = get_db()
    cur = db.execute('select * from votings where date=? and user=?', 
        [__get_current_time_in_s(), __get_logged_user()])
    entries = cur.fetchall()
    return entries
    
def get_actual_sum(pub_id):
    db = get_db()
    cur = db.execute('select sum(rating) as psum from votings where date=? and pub=?', 
        [__get_current_time_in_s(), pub_id])
    psum = cur.fetchall()[0]['psum']
    return psum if psum else 0

def __verify_voting_values(form_voting_items):
    # max 3 hlasovani
    # min hodnota 1
    # max hodnota 3
    # zadne stejne hodnoty
    cnt = 0
    ivals = []
    for (_, val) in form_voting_items:
        if val:
            cnt += 1
            ival = 0
            
            try:
                ival = int(val)
            except ValueError:
                return (False, 'Invalid input of voting (values=1,2,3,4)')
            if not 0 < ival < 4:
                return (False, 'Invalid value of voting (min=1, max=3)')
            if ival in ivals:
                return (False, 'Invalid value of voting (values must be unique)')
            ivals.append(ival)
    retval = 0 < cnt < 4
    return (True, None) if 0 < cnt < 4 else (False, 'Invalid number of votings (min=1, max=3)')

def __delete_voting():
    db = get_db()
    db.execute('delete from votings where date=? and user=?', 
        [__get_current_time_in_s(), __get_logged_user()])
    db.commit()
    flash('Old voting was successfully inserted')

def __insert_voting(pub_id, rating):
    db = get_db()
    cur = db.execute('select * from pubs where id = ?', [pub_id])
    pubs = cur.fetchall()

    db.execute('insert into votings (date, user, pub, rating) values (?, ?, ?, ?)', 
        [__get_current_time_in_s(), __get_logged_user(), pubs[0]['title'], rating])
    db.commit()
    flash('New voting was successfully inserted')

def vote(day_voting, form_voting_items):
    retval, error = __verify_voting_values(form_voting_items)
    if not retval:
        return (False, error)

    # formular spravne vyplnen - rozdeleni zda uz dnes hlasoval
    if day_voting:
        __delete_voting()
        
    for (pub_id, rating) in form_voting_items:
        if rating:
            __insert_voting(pub_id, int(rating))

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
        _user=__get_logged_user(),
        error=error)

def __get_pubs_items(pubs, day_votings, day_sums):
    pubs_items = []
    for p in pubs:
        has_voting = False
        for dv in day_votings:
            if p['title'] == dv['pub']:
                pubs_items.append((p, dv, day_sums[p['id']]))
                has_voting = True
                break
        if not has_voting:
            pubs_items.append((p, None, day_sums[p['id']]))
    return pubs_items

@app.route('/voting', methods=['GET', 'POST'])
def voting():
    if not session.get('logged_user'):
        abort(401)

    error = None
    pubs = get_pubs()
    day_votings = get_actual_voting()
    day_sums = {p['id']: get_actual_sum(p['title']) for p in pubs}
    pubs_items = __get_pubs_items(pubs, day_votings, day_sums)

    if request.method == 'POST':
        pass

        form_voting_items = [(p['id'], request.form[str(p['id'])]) for p in pubs]
                    
        retval, error = vote(day_votings, form_voting_items)
        if retval:
            flash('You voted')
            return redirect(url_for('voting'))
    # GET
    return render_template(
             'voting.html',
             title='Voting',
             year=datetime.now().year,
             logged_user=__get_logged_user(),
             pubs_items=pubs_items,
             error=error
            )

@app.route('/logout')
def logout():
    session.pop('logged_user', None)
    flash('You were logged out')
    return redirect(url_for('login'))

