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

from .config import app_config

version = os.getenv('URL_PREFIX')

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
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
        return render_template('api.html')

    #User registration
    @app.route('/api/v2/auth/register', methods=['POST'])
    def create_user():
        """
        Creates a user account
        """

        valid_email = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

        data = request.get_json(force=True)

        if "name" not in data or "email" not in data or "password" not in data:
        	return jsonify({"message":"All fields are required"}), 400

        hashed_password = generate_password_hash(data['password'])

        user = User.query.filter_by(email=data["email"]).first()

        if user:
        	return jsonify({"message":"Email has already been registered"}), 400

        if type(data["name"]) == int:

            return jsonify({"message":"name cannot be an integer"}), 400

        if data['name'] == "" or data['email'] == "" or data['password'] == "":

        	return jsonify({"message":"Empty field detected please fill all fields"}), 400

        if data['name'].split() == [] or data['email'].split() == [] or data['password'].split() == []:

        	return jsonify({"message":"name/email/password fields cannot be empty"}), 400

        if not re.match(valid_email, data["email"]):

        	return jsonify({"message":"Enter a valid email address"}), 400

        if len(data['password'].split()[0]) < 4:

        	return jsonify({"message":"password should be at least 4 characters"}), 400

        else:

        	new_user = User(name=data['name'], email=data["email"], password=hashed_password)

        	new_user.save()

        	return jsonify({"message":"registration succesfull"}), 201


    #User login
    @app.route('/'+version+'/auth/login', methods=['POST'])
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
    @app.route('/'+version+'/auth/logout', methods=["POST"])
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
    @app.route('/'+version+'/auth/reset-password', methods=["POST"])
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
    @app.route('/'+version+'/events', methods=['POST'])
    @token_required
    def create_event(current_user):
        """
        Creates an event
        """

        events = request.get_json(force=True)

        if type(events["title"]) == int:

            return jsonify({"message":"title cannot be an integer"}), 400

        if events['title'] == "" or events['category'] == "" or events['location'] == "" or events['description'] == "":
            return jsonify({"message":"Empty field set detected"}), 400

        if events['title'].split() == []:

        	return jsonify({"message":"Please provide a valid title"}), 400


        evnt = Event.query.filter_by(title=events["title"].lower()).first()

        if evnt:
        	return jsonify({"message":"An event with a similar title already exists"}), 400

        new_event = Event(
                            title=events['title'].lower(),
                            category=events['category'],
                            location=events['location'],
                            description=events['description'],
                            date_of_event=events['date_of_event'],
                            created_by=current_user.email
                            )
        new_event.save()

        response = jsonify({"message":"new event has been created"})
        response.status_code = 201

        return response

    #Retrieve all Events
    @app.route('/api/v2/events/<int:results>/<int:page_num>', methods=['GET'])
    def retrieve_events(results, page_num):
        """
        Retrieves events
        """

        Events = Event.query.paginate(page=page_num, per_page=results)

        evnts = Events.items
        num_results = Events.total
        total_pages = Events.pages
        current_page = Events.page
        has_next_page = Events.has_next
        has_prev_page = Events.has_prev
        prev_num = Events.prev_num
        next_num = Events.next_num

        output = []
        for event in evnts:
            output.append(event.json())

        return jsonify({
                            "total results": num_results,
                            "total pages": total_pages,
                            "cur page": current_page,
                            "Events":output,
                            "prev page":prev_num,
                            "next page":next_num

                            }), 200

    #Retrieve my Events
    @app.route('/'+version+'/events/myevents/<int:results>/<int:page_num>', methods=['GET'])
    @token_required
    def retrieve_my_events(current_user, results, page_num):
        """
        Retrieves events
        """

        Events = Event.query.filter_by(created_by=current_user.email).paginate(page=page_num, per_page=results)

        evnts = Events.items
        num_results = Events.total
        total_pages = Events.pages
        current_page = Events.page
        has_next_page = Events.has_next
        has_prev_page = Events.has_prev
        prev_num = Events.prev_num
        next_num = Events.next_num

        output = []
        for event in evnts:
            output.append(event.json())

        return jsonify({
                            "Message":"Events created by "+current_user.name,
                            "total results": num_results,
                            "total pages": total_pages,
                            "cur page": current_page,
                            "events":output,
                            "prev page":prev_num,
                            "next page":next_num

                            }), 200

    #Update Event
    @app.route('/'+version+'/events/<eventId>', methods=['PUT'])
    @token_required
    def update_event(current_user, eventId):
        """
        Updates an Event
        """

        update_data = request.get_json(force=True)
        event = Event.query.filter_by(event_id=eventId).first()


        if not event:
            return jsonify({'message' : 'The requested event was not found!'}), 400

        if event.created_by != current_user.email:

            return jsonify({'message':'You do not have enough permissions to edit this event'}), 401

        event.title = update_data['title']
        event.category = update_data['category']
        event.location = update_data['location']
        event.description = update_data['description']
        event.modified_on = datetime.datetime.now()
        db.session.commit()

        return jsonify({'message' : 'The event has been updated!'}), 200

    #Delete Event
    @app.route('/'+version+'/events/<eventId>', methods=['DELETE'])
    @token_required
    def delete_event(current_user, eventId):
        """
        Deletes an event
        """

        event = Event.query.filter_by(event_id=eventId).first()

        if not event:
            return jsonify({'message' : 'The requested event was not found!'}), 400

        if event.created_by != current_user.email:

            return jsonify({'message':'You do not have enough permissions to delete this event'}), 401

        event.delete()

        return jsonify({'message' : 'The event has been deleted!'}), 200

    #Create Reservation
    @app.route('/'+version+'/event/<eventId>/rsvp', methods=['POST'])
    def rsvp_event(eventId):
        """
        Allows a user to RSVP for an event
        """

        valid_email = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

        #Get request data from user
        data = request.get_json(force=True)

        #Check if the user has entered a valid email address
        if not re.match(valid_email, data["email"]):

        	return jsonify({"message":"Enter a valid email address"}), 400

        #Check if the user is registered
        usr = User.query.filter_by(email=data["email"]).first()

        #if the user is not registered, register the email and send a temp pass
        if not usr:

            hashed_password = generate_password_hash("12345", method='sha256')

            new_user = User(name=data['email'].split("@")[0], email=data["email"], password=hashed_password)

            new_user.save()

            new_usr = User.query.filter_by(email=data["email"]).first()

            #Check for the event in question
            event = Event.query.filter_by(event_id=eventId).first()

            if not event:
                return jsonify({"message":"event could not be found"}), 404

            guests = event.user

            if new_usr in guests:
                return jsonify({"message":"you have already reserved for "+event.title}), 403
            else:
                guests.append(new_usr)
                db.session.commit()

            return jsonify({
                                "Message":'Welcome ' + data["email"].split("@")[0] +', your reservation for the event '+event.title+' has been approved',
                                "important":"Your temporary password is 12345, use it to login and set a safer password"
                                }), 200

        else:

            event = Event.query.filter_by(event_id=eventId).first()

            if not event:
                return jsonify({"message":"event could not be found"}), 404

            guests = event.user
            if usr in guests:
                return jsonify({"message":"you have already reserved for "+event.title}), 403
            else:
                guests.append(usr)
                db.session.commit()

            return jsonify({'message':'Welcome ' + data["email"] +', your reservation for the event '+event.title+' has been approved'}), 200

    #Retrieves Reservations
    @app.route('/'+version+'/event/<eventId>/rsvp', methods=['GET'])
    @token_required
    def rsvp_guests(current_user, eventId):
        """
        Retrieves a list of users who have event reservations
        """

        event = Event.query.filter_by(event_id=eventId).first()

        if not event:
            return jsonify({"message":"Please Enter a valid event title"}), 403

        if event.created_by != current_user.email:

            return jsonify({"message":"You do not have enough permissions to view this information"}), 401

        guests = event.user

        output = []
        for guest in guests:
            attendees = {}
            attendees['name'] = guest.name
            attendees['email'] = guest.email
            output.append(attendees)

        return jsonify({'message':"Guests attending "+event.title, "guest_list":output}), 200

    #Search Event
    @app.route('/'+version+'/events/<q>/<int:results>/<int:page_num>', methods=['GET'])
    def get_one_event(q, results, page_num):

        results = Event.query.filter(Event.title.like('%'+ q.lower() +'%')).paginate(page=page_num, per_page=results)

        search_results = results.items
        num_results = results.total
        total_pages = results.pages
        current_page = results.page
        has_next_page = results.has_next
        has_prev_page = results.has_prev
        prev_num = results.prev_num
        next_num = results.next_num


        if not results.items:
        	return jsonify({'message' : 'event not found!'}), 400

        else:

        	items = []
        	for evnt in search_results:
        		items.append(evnt.json())

        	return jsonify({
                                "total results": num_results,
                                "total pages": total_pages,
                                "cur page": current_page,
                                "Search_Results":items,
                                "prev page":prev_num,
                                "next page":next_num,

                                }), 200

    #Filter Events by Category
    @app.route('/'+version+'/events/category/<category>/<int:results>/<int:page_num>', methods=['GET'])
    def filter_all_categories(category, results, page_num):

        event = Event.query.filter_by(category=category.lower()).paginate(page=page_num, per_page=results)

        filter_results = event.items
        num_results = event.total
        total_pages = event.pages
        current_page = event.page
        has_next_page = event.has_next
        has_prev_page = event.has_prev
        prev_num = event.prev_num
        next_num = event.next_num

        if not event:
            return jsonify({"message":"no events found for the selected category"}), 401


        categories = []

        for evnt in filter_results:
        	categories.append(evnt.json())

        return jsonify({
                            "total results": num_results,
                            "total pages": total_pages,
                            "cur page": current_page,
                            "prev page":prev_num,
                            "next page":next_num,
                            "Filter_Results":categories

                            }), 200

    #Filter Events by Location
    @app.route('/'+version+'/events/location/<location>/<int:results>/<int:page_num>', methods=['GET'])
    def filter_all_locations(location, results, page_num):

        event = Event.query.filter_by(location=location.lower()).paginate(page=page_num, per_page=results)

        filter_results = event.items
        num_results = event.total
        total_pages = event.pages
        current_page = event.page
        has_next_page = event.has_next
        has_prev_page = event.has_prev
        prev_num = event.prev_num
        next_num = event.next_num

        if not event:
            return jsonify({"message":"no events found for the selected location"}), 401


        locations = []

        for evnt in filter_results:
        	locations.append(evnt.json())

        return jsonify({
                            "total results": num_results,
                            "total pages": total_pages,
                            "cur page": current_page,
                            "prev page":prev_num,
                            "next page":next_num,
                            "Filter_Results":locations

                            }), 200

    @app.errorhandler(400)
    def bad_request_type(e):
        """
        Response message for a request sent with the wrong syntax
        """

        return jsonify({"message":"request sent with invalid syntax"}), 400

    @app.errorhandler(404)
    def route_not_found(e):
        """
        Response message for missing or not found resource endpoints.
        """

        return jsonify({"message":"resource not found"}), 404


    @app.errorhandler(405)
    def method_not_found(e):
        """
        Response for methods not allowed for the requested URLs
        """

        return jsonify({"message":"method not allowed for the requested resource"}), 405


    @app.errorhandler(500)
    def internal_server_error(e):
        """
        Response for 500 internal error
        """

        return jsonify({"message":"Internal server error"}), 500

    return app
