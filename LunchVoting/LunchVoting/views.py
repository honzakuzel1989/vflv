"""
Routes and views for the flask application.
"""

import os
import re
import dal
import helpers as h
import database as d
import verificators as v

from LunchVoting import app
from datetime import datetime
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, redirect, \
    url_for, abort, render_template, flash, g

def __get_logged_user():
    return session.get('logged_user')

#
# Databaze
#

def check_auth(username, password):
    """Check authorization"""
    entries = dal.get_user_by_username(username)

    if len(entries) != 1:
        return (False, 'Invalid username')

    pass_h = entries[0]['pass']
    verif = pass_h == h.compute_hash_in_hex(password)

    return (True, None) if verif else (False, 'Invalid password')

def __update_password(new_pass):
    db = d.get_db()
    cur = db.execute('update users set pass=? where name=?', 
        [h.compute_hash_in_hex(new_pass), __get_logged_user()])
    db.commit()

def __delete_voting():
    db = d.get_db()
    db.execute('delete from votings where date=? and user=?', 
        [h.get_current_time_in_s(), __get_logged_user()])
    db.commit()
    flash('Old voting was successfully inserted')

def __insert_voting(pub_id, rating):
    db = d.get_db()
    cur = db.execute('select * from pubs where id = ?', [pub_id])
    pubs = cur.fetchall()

    db.execute('insert into votings (date, user, pub, rating) values (?, ?, ?, ?)', 
        [h.get_current_time_in_s(), __get_logged_user(), pubs[0]['title'], rating])
    db.commit()
    flash('New voting was successfully inserted')

def get_pubs_items(pubs, day_votings, day_sums):
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

def vote(day_voting, form_voting_items):
    retval, error = v.verify_voting_values(form_voting_items)
    if not retval:
        return (False, error)

    if day_voting:
        __delete_voting()
        
    for (pub_id, rating) in form_voting_items:
        if rating:
            __insert_voting(pub_id, int(rating))

    return (True, None)

#
# App metody
#

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#
# Routovani html stranek
#

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
    if __get_logged_user():
        return redirect(url_for('voting'))

    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        logged_user=__get_logged_user(),
        error=error)

@app.route('/passwd', methods=['GET', 'POST'])
def passwd():
    if not __get_logged_user():
        abort(401)

    error = None
    if request.method == 'POST':
        pass
        retval, error = check_auth(__get_logged_user(), request.form['oldpassword'])
        if retval:
            new_pass = request.form['newpassword']
            retval, error = __v.verify_password(new_pass)
            if retval:
                __update_password(new_pass)
                flash('You password was changed')
                return redirect(url_for('voting'))
    # GET
    return render_template(
        'passwd.html',
        title='Change Password',
        year=datetime.now().year,
        logged_user=__get_logged_user(),
        error=error)

@app.route('/voting', methods=['GET', 'POST'])
def voting():
    if not __get_logged_user():
        abort(401)

    error = None
    pubs = dal.get_pubs()
    day_votings = dal.get_actual_voting_for_user(__get_logged_user())
    day_sums = {p['id']: dal.get_actual_sum(p['title']) for p in pubs}
    pubs_items = get_pubs_items(pubs, day_votings, day_sums)

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

@app.route('/detail')
def detail():
    if not __get_logged_user():
        abort(401)

    error = None
    votings = dal.get_actual_voting_for_all_user()
    detail_items = {}
    for v in votings:
        detail_items.setdefault(v['pub'], []).append((v['user'], v['rating']))
    detail_items = sorted(detail_items.items())

    # GET
    return render_template(
             'detail.html',
             title='Voting Detail',
             year=datetime.now().year,
             logged_user=__get_logged_user(),
             detail_items=detail_items,
             error=error
            )

@app.route('/logout')
def logout():
    session.pop('logged_user', None)
    flash('You were logged out')
    return redirect(url_for('login'))

