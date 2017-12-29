from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import datetime

db = SQLAlchemy()

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from .models import User, Event


from config import app_config

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
                current_user = User.query.filter_by(public_id=data['public_id']).first()
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

        Events = Event.query.all()

        output = []

        for event in Events:
            event_data = {}
            event_data['id'] = event.id
            event_data['title'] = event.title
            event_data['category'] = event.category
            event_data['location'] = event.location
            event_data['description'] = event.description
            output.append(event_data)


        return jsonify({"Events":output}), 200

    #search and retrieve a single event
    @app.route('/api/v2/events/<searchQuery>', methods=['GET'])
    def get_one_event(searchQuery):

    	results = Event.query.filter(Event.title.like('%'+searchQuery+'%')).all()

    	if not results:
    		return jsonify({'message' : 'The requested events were not found!'}), 400

    	items = []

    	for evnt in results:

    		search_data = {}
    		search_data['id'] = evnt.id
    		search_data['title'] = evnt.title
    		search_data['category'] = evnt.category
    		search_data['location'] = evnt.location
    		search_data['description'] = evnt.description
    		items.append(search_data)

    	return jsonify(items)

    #Checks a user to the reserved events
    @app.route('/api/v2/event/<eventId>/rsvp', methods=['PUT'])
    @token_required
    def rsvp_event(current_user, eventId):
        """
        Allows a user to RSVP to an event
        """

        user = User.query.filter_by(name=eventId).first()

        if not user:
            return jsonify({'message' : 'No user found!'}),401

        print Event.user

        #db.session.commit()

        return jsonify({'message' : 'The user has reserved for the event!'})

    #Retrieves a list of users who have reserved for an event
    @app.route('/api/v2/events/rsvp', methods=['GET'])
    @token_required
    def rsvp_guests(current_user):
        """
        Retrieves a list of users who have event reservations
        """

        return ""


    #filter by category
    @app.route('/api/v2/events/category/<category>', methods=['GET'])
    def filter_all_categories(category):

    	event = Event.query.filter_by(category=category).all()

    	if event != []:

    		categories = []
    		for evnt in event:

    			filter_category = {}
    			filter_category['id'] = evnt.id
    			filter_category['title'] = evnt.title
    			filter_category['category'] = evnt.category
    			filter_category['location'] = evnt.location
    			filter_category['description'] = evnt.description
    			categories.append(filter_category)

    		return jsonify(categories), 200
    	else:
    		return jsonify({"message":"no events found for the category"}), 401

    #filter by location
    @app.route('/api/v2/events/location/<location>', methods=['GET'])
    def filter_all_locations(location):

    	event = Event.query.filter_by(location=location).all()

    	if event != []:

    		locations = []
    		for evnt in event:

    			filter_location = {}
    			filter_location['id'] = evnt.id
    			filter_location['title'] = evnt.title
    			filter_location['category'] = evnt.category
    			filter_location['location'] = evnt.location
    			filter_location['description'] = evnt.description
    			locations.append(filter_location)

    		return jsonify(locations), 200
    	else:
    		return jsonify({"message":"no events found for the chosen location"}), 401

    return app
