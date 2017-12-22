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

    def __init__(self, name, email, password):
        """
        Inittialise User credentials
        """

        self.name = name
        self.email = email
        self.password = password

    def save(self):
        """
        Saves a user to the databse
        """

        db.session.add(self)
        db.session.commit()


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

    def __init__(self, title, category, location, description):

        """
        Initialise event details
        """
        self.title = title
        self.category = category
        self.location = location
        self.description = description

    def save(self):
        """
        Saves an event to the database
        """

        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an event in the database
        """

        db.session.commit()

    def delete(self):
        """
        Deletes an event from the database
        """

        db.session.delete(self)
        db.session.commit()


db.Table('reservations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')))
