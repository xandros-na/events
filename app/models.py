from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    student_num = db.Column(db.Integer(), nullable=False)

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    room = db.Column(db.String(12), nullable=False)
    thedate = db.Column(db.DateTime())
    posted_date = db.Column(db.String(128), nullable=False)
    replaced_id = db.Column(db.Integer)
    deleted = db.Column(db.Boolean, default=False)
