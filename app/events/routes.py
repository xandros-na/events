from . import events
from ..models import Events
from .. import db
from flask import render_template, request, current_app, redirect, url_for, flash, session
from .forms import LoginForm, EventForm

@events.route('/')
def index():
    event_list = Events.query.order_by(Events.date.desc())
    return render_template('events/index.html', event_list=event_list)

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

@events.route('/new', methods=['GET', 'POST'])
def new_event():
    if not session.get('logged_in'):
        flash('You must login as admin to add an event')
        return redirect(url_for('events.login'))
    else:
        form = EventForm()
        if form.validate_on_submit():
            event = Events(title=form.title.data,
                room=form.room.data,
                date=form.date.data)
            db.session.add(event)
            db.session.commit()
            flash('Event added')
            return redirect(url_for('events.index'))
    return render_template('events/new_event.html', form=form)

@events.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('events.index'))
