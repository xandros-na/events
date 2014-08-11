from . import events
from flask import render_template, request, current_app, redirect, url_for, flash, session
from .forms import LoginForm

@events.route('/')
def index():
    return render_template('events/index.html')

@events.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.username.data != current_app.config['ADMIN'] or \
                form.password.data != current_app.config['ADMIN_PASS']:
                flash('invalid credentials')
        else:
            session['logged_in'] = True
            flash('Login successful')
            return redirect(url_for('events.index'))
    return render_template('events/login.html', form=form)

@events.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('events.index'))
