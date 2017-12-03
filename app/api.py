from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from functools import wraps
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://marlone911:bev@localhost:5432/brightevents'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#MODELs

class User(db.Model):
	"""
	User Table Schema
	"""
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))
	email = db.Column(db.String(50))
	password = db.Column(db.String(50))


class Event(db.Model):
	"""
	Event Table Schema
	"""

	__tablename__ = "events"

	id = db.Column(db.Integer, primary_key=True)
	event_id = db.Column(db.String(50), unique=True)
	title = db.Column(db.String(50))
	category = db.Column(db.String(50))
	location = db.Column(db.String(50))
	description = db.Column(db.String)



db.create_all()
#API Routes

#auth token
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
#create a new user
@app.route('/api/auth/register', methods=['POST'])
def create_user():
	"""
	Creates a user account
	"""

	data = request.get_json()
	hashed_password = generate_password_hash(data['password'], method='sha256')


	if data['name'] == "" or data['email'] == "" or data['password'] == "":

		return jsonify({"message":"Empty field detected please fill all fields"})

	if "@" in data["email"] == False:

		return jsonify({"message":"Enter a valid email address"})

	if type(data['name']) == 'int':

		return jsonify({"message":"Enter a valid Name"})

	if len(data['password']) < 4:

		return jsonify({"message":"password should be at least 4 characters"})
	else:

		new_user = User(name=data['name'], email=data["email"], password=hashed_password)

		db.session.add(new_user)
		db.session.commit()

		users = User.query.all()

		output = []

		for user in users:
			user_data = {}
			user_data['id'] = user.id
			user_data['name'] = user.name
			user_data['email'] = user.email
			user_data['password'] = user.password
			output.append(user_data)

		return jsonify({"message":output})


#login a user
@app.route('/api/auth/login', methods=['POST'])
def login():
	auth = request.get_json()

	if not auth or auth['email'] == "" or auth['password'] == "":
		return jsonify({"message":"Could not verify"})
	user = User.query.filter_by(email=auth["email"]).first()

	if not user:
		return jsonify({"message":"Could not verify"})

	if check_password_hash(user.password, auth['password']):
		token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

		return jsonify({'token' : token.decode('UTF-8')})

	return jsonify({"message":"Could not verify"})


#logout a user
@app.route('/api/auth/logout', methods=["POST"])
def logout():
    """
    Logs out a user
    """

    auth_header = request.headers.get('x-access-token')

    if auth_header:

        return jsonify({"message":"logout succesfull"})

    return jsonify({"message":"you need to be logged in"})

#reset-password
@app.route('/api/auth/reset-password', methods=["POST"])
def reset_password():
    """
    Resets password
    """
	reset = request.get_json()
    user = User.query.filter_by(email=reset["email"]).first()

    if not user:
		return jsonify({"message":"email address could not be found"})

    if check_password_hash(user.password, reset['oldPassword']):

        new_hashed_password = generate_password_hash(reset['newPassword'], method='sha256')
        user.password = new_hashed_password

        db.session.commit()

        return jsonify({"message":"password has been updated succesfully"})

    return jsonify({"message":"old-password is invalid"})

#create a new event

@app.route('/api/events', methods=['POST'])
@token_required
def create_event(current_user):
    """
    Creates an event
    """

    events = request.get_json()

    new_event = Event(
                        title=events['title'],
                        category=events['category'],
                        location=events['location'],
                        description=events['description']
                        )
    db.session.add(new_event)
    db.session.commit()

    return jsonify({"message":"new event has been created"})

#Updates an event
@app.route('/api/events/<string:eventId>', methods=['PUT'])
@token_required
def update_event(current_user, eventId):
    """
    Updates an Event
    """

    event = Event.query.filter_by(id=eventId).first()

    if not event:
        return jsonify({'message' : 'The requested event was not found!'}), 404

    event.title = request.json['title']
    event.category = request.json['category']
    event.location = request.json['location']
    event.description = request.json['description']
    db.session.commit()

    return jsonify({'message' : 'The event has been updated!'})

#deletes an event
@app.route('/api/events/<eventId>', methods=['DELETE'])
@token_required
def delete_event(current_user, eventId):
    """
    Deletes an event
    """

    event = Event.query.filter_by(id=eventId).first()

    if not event:
        return jsonify({'message' : 'The requested event was not found!'}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

#retrieves all events
@app.route('/api/events', methods=['GET'])
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


    return jsonify({"Events":output})

#search and retrieve a single event
@app.route('/api/events/<searchQuery>', methods=['GET'])
def get_one_event(searchQuery):

    event = Event.query.filter_by(title=searchQuery).first()

    if not event:
        return jsonify({'message' : 'The requested event was not found!'}), 404

    search_data = {}
    search_data['id'] = event.id
    search_data['title'] = event.title
    search_data['category'] = event.category
    search_data['location'] = event.location
    search_data['description'] = event.description

    return jsonify(search_data)

#Checks a user to the reserved events
@app.route('/api/event/<eventId>/rsvp', methods=['PUT'])
@token_required
def rsvp_event(current_user, eventId):
    """
    Allows a user to RSVP to an event
    """

    user = User.query.filter_by(name=eventId).first()

    if not user:
        return jsonify({'message' : 'No user found!'}),404

    user.rsvp = True
    db.session.commit()

    return jsonify({'message' : 'The user has reserved for the event!'})

#Retrieves a list of users who have reserved for an event
@app.route('/api/events/rsvp', methods=['GET'])
@token_required
def rsvp_guests(current_user):
    """
    Retrieves a list of users who have event reservations
    """

    return ""

#filter by category
@app.route('/api/events/category/<category>', methods=['GET'])
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

		return jsonify(categories)
	else:
		return jsonify({"message":"no events found for the category"})

#filter by location
@app.route('/api/events/location/<location>', methods=['GET'])
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

		return jsonify(locations)
	else:
		return jsonify({"message":"no events found for the chosen location"})

if __name__ == '__main__':
    app.run(debug=True)
