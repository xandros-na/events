from datetime import datetime
from . import events
from ..models import Events, User
from .. import db
from flask import render_template, request, current_app, redirect, url_for, flash, session, jsonify, Response
from .forms import LoginForm, EventForm, UserForm
from time import sleep
from sqlalchemy import select, text

@events.route('/update')
def update():
    new_event = Events.query.order_by(Events.posted_date.desc()).first()
    if new_event is None:
        return jsonify(id=-1, title=None, room=None, date=None, replaced_id=None)
    else:
        return jsonify(id=new_event.id, title=new_event.title, room=new_event.room, thedate=new_event.thedate, replaced_id=new_event.replaced_id, deleted=new_event.deleted)

@events.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if not session.get('admin'):
        flash('You must login as admin to delete an event')
        return redirect(url_for('events.login'))
    else:
        event = Events.query.get_or_404(id)
        posted_date = datetime.now()
        posted_date = str(posted_date.strftime('%Y-%m-%d %H:%M:%S'))
        if not event.deleted:
            event.deleted = True
            event.posted_date = posted_date
            db.session.add(event)
            db.session.commit()
        flash('Event successfully deleted')
    return redirect(url_for('events.index'))

@events.route('/')
def index():
    event_list = Events.query.order_by(Events.thedate.desc())
    return render_template('events/index.html', event_list=event_list)

@events.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('user'):
        flash('You must log in as user to register')
        return redirect(url_for('events.login'))
    else:
        form = UserForm(payment='1')
        if form.validate_on_submit():
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, student_num=form.student_num.data, payment=form.payment.data)
            form.first_name.data=""
            form.last_name.data=""
            form.student_num.data=""
            form.payment.data="1"
            db.session.add(user)
            db.session.commit()
            flash('success')
            return render_template('events/register.html', form=form)
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
    if form.validate_on_submit():
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

@events.route('/new_event', methods=['GET', 'POST'])
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
                posted_date=posted_date,
                replaced_id=-1)
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
            replaced_id = event.id
            db.session.delete(event)
            edited_event = Events(title=form.title.data,
                room=form.room.data,
                thedate=form.date.data,
                posted_date=posted_date,
                replaced_id=replaced_id)
            db.session.add(edited_event)
            db.session.commit()
            flash('Successfully updated event')
            return redirect(url_for('events.index'))
        return render_template('events/edit_event.html', form=form)

@events.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('user', None)
    flash('You are now logged out')
    return redirect(url_for('events.index'))
