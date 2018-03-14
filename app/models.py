#MODELs
from flask import jsonify
from app import db
import datetime
import re
import jwt
import os

class BlackListToken(db.Model):
    """
    Table to store blacklisted/invalid auth tokens
    """
    __tablename__ = 'blacklist_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def blacklist(self):
        """
        Persist Blacklisted token in the database
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_blacklist(token):
        """
        Check to find out whether a token has already been blacklisted.
        """
        response = BlackListToken.query.filter_by(token=token).first()
        if response:
            return True
        return False

class User(db.Model):
    """
    User Table Schema
    """
    __tablename__ = "user"

    public_id = db.Column(db.Integer,primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

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

    @staticmethod
    def decode_auth_token(token):
        """
        Decoding the token to get the payload and then return the user Id in the payload['public_id']
        """
        secret = os.getenv('SECRET_KEY')

        try:
            payload = jwt.decode(token, secret)
            is_token_blacklisted = BlackListToken.check_blacklist(token)
            if is_token_blacklisted:
                return 'Token was Blacklisted, Please login In'
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Event(db.Model):
    """
    Event Table Schema
    """

    __tablename__ = "event"

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    category = db.Column(db.String(50))
    location = db.Column(db.String(50))
    description = db.Column(db.String)
    created_on = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    modified_on = db.Column(db.DateTime)
    date_of_event = db.Column(db.String(255))


    def __init__(self, title, category, location, description, created_by, date_of_event):

        """
        Initialise event details
        """
        self.title = title
        self.category = category
        self.location = location
        self.description = description
        self.created_on = datetime.datetime.now()
        self.modified_on = None
        self.created_by = created_by
        self.date_of_event = date_of_event


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

    def json(self):
        """
        Returns a json representation of the model
        """
        return {
            'id':self.event_id,
            'title':self.title,
            'location':self.location,
            'category':self.category,
            'description':self.description,
            'created_on':self.created_on,
            'created_by':self.created_by,
            'modified_on':self.modified_on,
            'date_of_event':self.date_of_event
        }

    def __repr__(self):
        return "<Event: {}>".format(self.title)


db.Table('reservations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.public_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id')))
