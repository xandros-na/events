from datetime import datetime
from . import events
from ..models import Events
from .. import db
from flask import render_template, request, current_app, redirect, url_for, flash, session, jsonify, Response
from .forms import LoginForm, EventForm, UserForm

@events.route('/test')
def test():
    new_event = Events.query.order_by(Events.posted_date.desc()).first()
    if new_event is None:
        return jsonify(id=-1, title=None, room=None, date=None)
    else:
        return jsonify(id=new_event.id, title=new_event.title, room=new_event.room, thedate=new_event.thedate)

@events.route('/')
def index():
    event_list = Events.query.order_by(Events.thedate.desc())
    return render_template('events/index.html', event_list=event_list)

@events.route('/register')
def register():
    form = UserForm()
    return render_template('events/register.html', form=form)

@events.route('/login', methods=['GET', 'POST'])
def login():
    accounts = {
            current_app.config['ADMIN'] : current_app.config['ADMIN_PASS'],
            current_app.config['USER'] : current_app.config['USER_PASS']
            }
    usernames = [current_app.config['ADMIN'], current_app.config['USER']]
    passwords = [current_app.config['ADMIN_PASS'], current_app.config['USER_PASS']]
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.username.data not in usernames or form.password.data not in passwords:
            flash('invalid credentials')
        else:
            flash('Login successful')
            if form.username.data == usernames[0]:
                session['admin'] = True
                return redirect(url_for('events.index'))
            else:
                session['user'] = True
                return redirect(url_for('events.register'))
    return render_template('events/login.html', form=form)

@events.route('/new', methods=['GET', 'POST'])
def new_event():
    if not session.get('admin'):
        flash('You must login as admin to add an event')
        return redirect(url_for('events.login'))
    else:
        form = EventForm()
        if form.validate_on_submit():
            posted_date = datetime.now()
            posted_date = str(posted_date.strftime('%Y-%m-%d %H:%M:%S'))
            event = Events(title=form.title.data,
                room=form.room.data,
                thedate=form.date.data,
                posted_date=posted_date)
            db.session.add(event)
            db.session.commit()
            flash('Event added')
            return redirect(url_for('events.index'))
    return render_template('events/new_event.html', form=form)

@events.route('/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    if not session.get('admin'):
        flash('You must login as admin to edit an event')
        return redirect(url_for('events.login'))
    else:
        event = Events.query.get_or_404(id)
        form = EventForm(title=event.title, room=event.room, date=event.thedate)
        if form.validate_on_submit():
            posted_date = datetime.now()
            posted_date = str(posted_date.strftime('%Y-%m-%d %H:%M:%S'))
            form.to_model(event, posted_date)
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('events.index'))
        form.from_model(event)
        return render_template('events/edit_event.html', form=form)

@events.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('user', None)
    flash('You are now logged out')
    return redirect(url_for('events.index'))
