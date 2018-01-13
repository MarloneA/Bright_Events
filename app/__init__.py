from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import datetime
import re

db = SQLAlchemy()

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from .models import User, Event


from instance.config import app_config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'message' : 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = User.query.filter_by(public_id=data["public_id"]).first()
            except:
                return jsonify({'message' : 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated

    #Render documentation as root of the api
    @app.route('/')
    def index():
        return render_template('api_doc.html')

    #create a new user
    @app.route('/api/v2/auth/register', methods=['POST'])
    def create_user():
    	"""
    	Creates a user account
    	"""

    	data = request.get_json()

    	if "name" not in data or "email" not in data or "password" not in data:
    		return jsonify({"message":"All fields are required"})

    	hashed_password = generate_password_hash(data['password'], method='sha256')

    	user = User.query.filter_by(email=data["email"]).first()

    	if user:
    		return jsonify({"message":"Email has already been registered"}), 400

    	if data['name'] == "" or data['email'] == "" or data['password'] == "":

    		return jsonify({"message":"Empty field detected please fill all fields"}), 400

    	if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):

    		return jsonify({"message":"Enter a valid email address"}), 400

    	if len(data['password']) < 4:

    		return jsonify({"message":"password should be at least 4 characters"}), 400
    	else:

    		new_user = User(name=data['name'], email=data["email"], password=hashed_password)

    		new_user.save()

    		return jsonify({"message":"registration succesfull"})


    #login a user
    @app.route('/api/v2/auth/login', methods=['POST'])
    def login():
    	auth = request.get_json()

    	if not auth or auth['email'] == "" or auth['password'] == "":
    		return jsonify({"message":"Could not verify"}), 400
    	user = User.query.filter_by(email=auth["email"]).first()

    	if not user:
    		return jsonify({"message":"Could not verify"}), 400

    	if check_password_hash(user.password, auth['password']):
    		token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

    		return jsonify({'token' : token.decode('UTF-8')}), 200

    	return jsonify({"message":"Could not verify"}), 400


    #logout a user
    @app.route('/api/v2/auth/logout', methods=["POST"])
    @token_required
    def logout(current_user):
    	"""
    	Logs out a user
    	"""

    	auth = request.get_json()

    	if not auth or auth['email'] == "" or auth['password'] == "":
    		return jsonify({"message":"You need to be logged in"}), 400
    	user = User.query.filter_by(email=auth["email"]).first()

    	if not user:
    		return jsonify({"message":"You need to be logged in"}), 400

    	if check_password_hash(user.password, auth['password']):
    		token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

    		return jsonify({'message' : "logout succesfull"}), 200

    	return jsonify({"message":"You need to be logged in"}), 400

    #reset-password
    @app.route('/api/v2/auth/reset-password', methods=["POST"])
    def reset_password():
        """
        Resets password
        """
        reset = request.get_json()

        if "email" not in reset or "oldPassword" not in reset or "newPassword" not in reset:
            return jsonify({"message":"All fields are required"})

        user = User.query.filter_by(email=reset["email"]).first()

        if not user:
        	return jsonify({"message":"email address could not be found"}), 400

        if check_password_hash(user.password, reset['oldPassword']):

    		new_hashed_password = generate_password_hash(reset['newPassword'], method='sha256')
    		user.password = new_hashed_password

    		db.session.commit()

    		return jsonify({"message":"password has been updated succesfully"}), 200

        return jsonify({"message":"old-password is invalid"}), 400

    #Retrireves all users
    @app.route('/api/v2/users', methods=['GET'])
    def retrieve_users():
        """
        Retrieves all users from the database
        """

        Users = User.query.all()

        output = []

        for usr in Users:
            usr_data = {}
            usr_data['id'] = usr.id
            usr_data['name'] = usr.name
            usr_data['email'] = usr.email
            usr_data['password'] = usr.password
            output.append(usr_data)


        return jsonify({"Users":output}), 200



    #create a new event

    @app.route('/api/v2/events', methods=['POST'])
    @token_required
    def create_event(current_user):
    	"""
    	Creates an event
    	"""

    	events = request.get_json()
    	evnt = Event.query.filter_by(title=events["title"]).first()

    	if evnt:
    		return jsonify({"message":"An event with a similar title already exists"}), 400
        if events['title'] == "" or events['category'] == "" or events['location'] == "" or events['description'] == "":
            return jsonify({"message":"Empty field set detected"})

    	new_event = Event(
    	                    title=events['title'],
    	                    category=events['category'],
    	                    location=events['location'],
    	                    description=events['description']
    	                    )
    	new_event.save()

    	return jsonify({"message":"new event has been created"}), 200

    #Updates an event
    @app.route('/api/v2/events/<string:eventId>', methods=['PUT'])
    @token_required
    def update_event(current_user, eventId):
        """
        Updates an Event
        """

        event = Event.query.filter_by(id=eventId).first()

        if not event:
            return jsonify({'message' : 'The requested event was not found!'}), 400

        event.title = request.json['title']
        event.category = request.json['category']
        event.location = request.json['location']
        event.description = request.json['description']
        db.session.commit()

        return jsonify({'message' : 'The event has been updated!'}), 200

    #deletes an event
    @app.route('/api/v2/events/<eventId>', methods=['DELETE'])
    @token_required
    def delete_event(current_user, eventId):
        """
        Deletes an event
        """

        event = Event.query.filter_by(id=eventId).first()

        if not event:
            return jsonify({'message' : 'The requested event was not found!'}), 400

        event.delete()

        return jsonify({'message' : 'The event has been deleted!'}), 200

    #retrieves all events
    @app.route('/api/v2/events', methods=['GET'])
    @token_required
    def retrieve_events(current_user):
        """
        Retrieves events
        """

        Events = Event.query.paginate(page=None, per_page=2)

        evnts = Events.items
        num_results = Events.total
        total_pages = Events.pages
        current_page = Events.page

        output = []
        for event in evnts:
            output.append(event.json())

        return jsonify({"num_results": num_results, "total_pages": total_pages, "page": current_page,"Events":output}), 200

    #search and retrieve a single event
    @app.route('/api/v2/events/<searchQuery>', methods=['GET'])
    def get_one_event(searchQuery):

    	results = Event.query.filter(Event.title.like('%'+searchQuery+'%')).paginate(page=None, per_page=2)

        search_results = results.items
        num_results = results.total
        total_pages = results.pages
        current_page = results.page

    	if not results:
    		return jsonify({'message' : 'event not found!'}), 400

    	items = []
    	for evnt in search_results:
    		items.append(evnt.json())

    	return jsonify({"num_results": num_results, "total_pages": total_pages, "page": current_page,"1search_results":items})

    #Reserves an event
    @app.route('/api/v2/event/<eventId>/rsvp', methods=['POST'])
    @token_required
    def rsvp_event(current_user, eventId):
        """
        Allows a user to RSVP for an event
        """

        usr = User.query.filter_by(name=current_user.name).first()

        event = Event.query.filter_by(title=eventId).first()

        guests = event.user
        guests.append(usr)

        output = []
        for guest in guests:
            rsv = {}
            rsv['name'] = guest.name
            output.append(rsv)

        return jsonify({'message':'reservation approved', 'guests':output})

    #Retrieves a list of users who have reserved for an event
    @app.route('/api/v2/event/<eventId>/rsvp', methods=['GET'])
    @token_required
    def rsvp_guests(current_user, eventId):
        """
        Retrieves a list of users who have event reservations
        """

        event = Event.query.filter_by(title=eventId).first()

        guests = event.user

        output = []
        for guest in guests:
            rsv = {}
            rsv['name'] = guest.name
            output.append(rsv)

        return jsonify({'message':output})


    #filter by category
    @app.route('/api/v2/events/category/<category>', methods=['GET'])
    def filter_all_categories(category):

    	event = Event.query.filter_by(category=category).paginate(page=None, per_page=2)

        filter_results = event.items
        num_results = event.total
        total_pages = event.pages
        current_page = event.page

    	if not event:
            return jsonify({"message":"no events found for the selected category"}), 401


        categories = []

        for evnt in filter_results:
        	categories.append(evnt.json())

        return jsonify({"num_results": num_results, "total_pages": total_pages, "page": current_page,"1filter_results":categories}), 200



    #filter by location
    @app.route('/api/v2/events/location/<location>', methods=['GET'])
    def filter_all_locations(location):

    	event = Event.query.filter_by(location=location).paginate(page=None, per_page=2)

        filter_results = event.items
        num_results = event.total
        total_pages = event.pages
        current_page = event.page

    	if not event:
            return jsonify({"message":"no events found for the selected location"}), 401


        locations = []

        for evnt in filter_results:
        	locations.append(evnt.json())

        return jsonify({"num_results": num_results, "total_pages": total_pages, "page": current_page,"1filter_results":locations}), 200


    return app
