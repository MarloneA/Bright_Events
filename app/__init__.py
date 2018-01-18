from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

import jwt
import datetime
import re
import os

db = SQLAlchemy()

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from .models import User, Event, BlackListToken



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
            secret = os.getenv('SECRET_KEY')

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'message' : 'Token is missing!'}), 401

            try:
                data = User.decode_auth_token(token)
                current_user = User.query.filter_by(public_id=data["public_id"]).first()
            except:
                return jsonify({'message' : 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated

    #Render documentation as root of the api
    @app.route('/')
    def index():
        return render_template('api_doc.html')

    #User registration
    @app.route('/api/v2/auth/register', methods=['POST'])
    def create_user():
    	"""
    	Creates a user account
    	"""

    	data = request.get_json(force=True)

    	if "name" not in data or "email" not in data or "password" not in data:
    		return jsonify({"message":"All fields are required"}), 400

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

    		return jsonify({"message":"registration succesfull"}), 201


    #User login
    @app.route('/api/v2/auth/login', methods=['POST'])
    def login():
    	auth = request.get_json(force=True)

    	if not auth or auth['email'] == "" or auth['password'] == "":
    		return jsonify({"message":"Invalid email/password"}), 401
    	user = User.query.filter_by(email=auth["email"]).first()

    	if not user:
    		return jsonify({"message":"Could not verify"}), 401

    	if check_password_hash(user.password, auth['password']):

            payload = {
                'public_id' : user.public_id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }
            secret = os.getenv('SECRET_KEY')
            token = jwt.encode(payload, secret)
            if token:
                response = {
                    "message":"Login succesfull",
                    "x-access-token":token.decode()
                }
            return make_response(jsonify(response)), 200

    	return jsonify({"message":"Incorrect password"}), 401

    #User logout
    @app.route('/api/v2/auth/logout', methods=["POST"])
    @token_required
    def logout(current_user):
    	"""
    	Logs out a user
    	"""

    	auth_header = request.headers.get('x-access-token')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[0]
            except IndexError:
                return jsonify({'message':'failed Provide a valid auth token'}), 401
            else:
                decoded_token_response = User.decode_auth_token(auth_token)
                if not isinstance(decoded_token_response, str):
                    token = BlackListToken(auth_token)
                    token.blacklist()
                    return jsonify({'message':'Successfully logged out'}), 200
                return jsonify({'message':'failed'}), decoded_token_response, 401
        return 'failed Provide an authorization header', 403

    #Password Reset
    @app.route('/api/v2/auth/reset-password', methods=["POST"])
    def reset_password():
        """
        Resets password
        """
        reset = request.get_json(force=True)

        if "email" not in reset or "oldPassword" not in reset or "newPassword" not in reset:
            return jsonify({"message":"All fields are required"}), 400

        user = User.query.filter_by(email=reset["email"]).first()

        if not user:
        	return jsonify({"message":"email address could not be found"}), 401

        if check_password_hash(user.password, reset['oldPassword']):

    		new_hashed_password = generate_password_hash(reset['newPassword'], method='sha256')
    		user.password = new_hashed_password

    		db.session.commit()

    		return jsonify({"message":"password has been updated succesfully"}), 200

        return jsonify({"message":"old-password is invalid"}), 401


    #Create Event
    @app.route('/api/v2/events', methods=['POST'])
    @token_required
    def create_event(current_user):
    	"""
    	Creates an event
    	"""

    	events = request.get_json(force=True)
    	evnt = Event.query.filter_by(title=events["title"]).first()

    	if evnt:
    		return jsonify({"message":"An event with a similar title already exists"}), 400
        if events['title'] == "" or events['category'] == "" or events['location'] == "" or events['description'] == "":
            return jsonify({"message":"Empty field set detected"}), 400

    	new_event = Event(
    	                    title=events['title'],
    	                    category=events['category'],
    	                    location=events['location'],
    	                    description=events['description']
    	                    )
    	new_event.save()

        response = jsonify({"message":"new event has been created"})
        response.status_code = 201

    	return response

    #Retrieve Events
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

    #Update Event
    @app.route('/api/v2/events/<string:eventTitle>', methods=['PUT'])
    @token_required
    def update_event(current_user, eventTitle):
        """
        Updates an Event
        """

        update_data = request.get_json(force=True)
        event = Event.query.filter_by(title=eventTitle).first()


        if not event:
            return jsonify({'message' : 'The requested event was not found!'}), 400

        event.title = update_data['title']
        event.category = update_data['category']
        event.location = update_data['location']
        event.description = update_data['description']
        db.session.commit()

        return jsonify({'message' : 'The event has been updated!'}), 200

    #Delete Event
    @app.route('/api/v2/events/<eventTitle>', methods=['DELETE'])
    @token_required
    def delete_event(current_user, eventTitle):
        """
        Deletes an event
        """

        event = Event.query.filter_by(title=eventTitle).first()

        if not event:
            return jsonify({'message' : 'The requested event was not found!'}), 400

        event.delete()

        return jsonify({'message' : 'The event has been deleted!'}), 200

    #Create Reservation
    @app.route('/api/v2/event/<eventId>/rsvp', methods=['POST'])
    @token_required
    def rsvp_event(current_user, eventId):
        """
        Allows a user to RSVP for an event
        """

        usr = User.query.filter_by(name=current_user.name).first()

        event = Event.query.filter_by(title=eventId).first()

        guests = event.user
        if usr in guests:
            return jsonify({"message":"you have already reserved for "+event.title}), 403
        else:
            guests.append(usr)
            db.session.commit()

        return jsonify({'message':'Welcome ' + current_user.name +', your reservation has been approved'}), 200

    #Retrieves Reservations
    @app.route('/api/v2/event/<eventId>/rsvp', methods=['GET'])
    @token_required
    def rsvp_guests(current_user, eventId):
        """
        Retrieves a list of users who have event reservations
        """

        event = Event.query.filter_by(title=eventId).first()

        if not event:
            return jsonify({"message":"Please Enter a valid event title"}), 403

        guests = event.user

        output = []
        for guest in guests:
            attendees = {}
            attendees['name'] = guest.name
            attendees['email'] = guest.email
            output.append(attendees)

        return jsonify({'message':"Guests attending "+event.title, "guests":output}), 200

    #Search Event
    @app.route('/api/v2/events/<searchQuery>', methods=['GET'])
    def get_one_event(searchQuery):

    	results = Event.query.filter(Event.title.like('%'+searchQuery+'%')).paginate(page=None, per_page=2)

        search_results = results.items
        num_results = results.total
        total_pages = results.pages
        current_page = results.page

    	if not results.items:
    		return jsonify({'message' : 'event not found!'}), 400

        else:

        	items = []
        	for evnt in search_results:
        		items.append(evnt.json())

        	return jsonify({"num_results": num_results, "total_pages": total_pages, "page": current_page,"1search_results":items}), 200

    #Filter Events by Category
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

    #Filter Events by Location
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
