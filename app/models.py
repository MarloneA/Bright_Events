#MODELs
from flask import jsonify
from . import db
import datetime
import re


class User(db.Model):
    """
    User Table Schema
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

    events = db.relationship('Event', secondary='reservations',  backref='user', lazy='dynamic')


class Event(db.Model):
	"""
	Event Table Schema
	"""

	__tablename__ = "event"

	id = db.Column(db.Integer, primary_key=True)
	event_id = db.Column(db.String(50), unique=True)
	title = db.Column(db.String(50))
	category = db.Column(db.String(50))
	location = db.Column(db.String(50))
	description = db.Column(db.String)

db.Table('reservations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')))
