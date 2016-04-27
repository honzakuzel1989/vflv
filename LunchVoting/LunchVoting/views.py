"""
Routes and views for the flask application.
"""

import os
import re
import dal
import helpers as h
import verificators as v
import presenters as p
import database as db

from LunchVoting import app
from flask import Flask, request, session, redirect, \
    url_for, abort, render_template, flash, g

#
# Privatni metody
#

def __get_logged_user():
    return session.get('logged_user')

#
# App metody
#

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
        retval, error = p.check_auth(request.form['username'], request.form['password'])
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
        year=h.get_current_year(),
        logged_user=__get_logged_user(),
        error=error)

@app.route('/passwd', methods=['GET', 'POST'])
def passwd():
    if not __get_logged_user():
        abort(401)

    error = None
    if request.method == 'POST':
        pass
        retval, error = p.check_auth(__get_logged_user(), request.form['oldpassword'])
        if retval:
            new_pass = request.form['newpassword']
            retval, error = v.verify_password(new_pass)
            if retval:
                dal.update_password(__get_logged_user(), new_pass)
                flash('You password was changed')
                return redirect(url_for('voting'))
    # GET
    return render_template(
        'passwd.html',
        title='Change Password',
        year=h.get_current_year(),
        logged_user=__get_logged_user(),
        error=error)

@app.route('/voting', methods=['GET', 'POST'])
def voting():
    if not __get_logged_user():
        abort(401)

    error = None
    pubs = dal.get_pubs()
    day_votings = dal.get_actual_voting_for_user(__get_logged_user())
    day_sums = {pub['id']: dal.get_actual_sum(pub['title']) for pub in pubs}
    pubs_items = p.get_pubs_items(pubs, day_votings, day_sums)

    # sort pubs_items by pubs day_sums and reverse list
    pubs_items.sort(key=lambda tup: (tup[2]))
    pubs_items.reverse()

    if request.method == 'POST':
        pass

        form_voting_items = {pub['id']:request.form[str(pub['id'])] for pub in pubs}
                    
        retval, error = p.vote(__get_logged_user(), day_votings, form_voting_items)
        if retval:
            flash('You voted')
            return redirect(url_for('voting'))
    # GET
    return render_template(
             'voting.html',
             title='Voting',
             year=h.get_current_year(),
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
             title='Voting - detail',
             year=h.get_current_year(),
             logged_user=__get_logged_user(),
             detail_items=detail_items,
             error=error
            )

@app.route('/logout')
def logout():
    session.pop('logged_user', None)
    flash('You were logged out')
    return redirect(url_for('login'))
