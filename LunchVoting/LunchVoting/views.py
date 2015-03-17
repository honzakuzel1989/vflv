"""
Routes and views for the flask application.
"""

import os
import LunchVoting.presenters as p

from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from LunchVoting import app

app.config.update(dict(
    USERNAME='admin',
    PASSWORD='pass'
))

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if p.check_auth(request.form['username'], request.form['password']):
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
