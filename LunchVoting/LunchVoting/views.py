"""
Routes and views for the flask application.
"""

import os
import LunchVoting.presenters as p

from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template
from LunchVoting import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

app.config.update(dict(
    USERNAME='admin',
    PASSWORD='pass'
))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if p.check_auth(request.form['username'], request.form['password']):
            session['logged_in'] = True
            flash('You were logged in')
    
            return render_template(
             'voting.html',
             title='Contact',
             year=datetime.now().year,
             message='Your contact page.'
            )
    # GET
    return render_template(
        'login.html', 
        title='Login',
        year=datetime.now().year,
        message='Login page.',
        error=error)
