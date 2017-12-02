from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://marlone911:bev@localhost:5432/brightevents'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#MODELs

class User(db.Model):
    """
    Table Schema
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))


class Event(db.Model):
    """
    Table Schema
    """

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    category = db.Column(db.String(50))
    location = db.Column(db.String(50))
    description = db.Column(db.String)



db.create_all()
#API Routes

#create a new user
@app.route('/api/auth/register', methods=['POST'])
def create_user():
    """
    Creates a user account
    """

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(name=data['name'], email=data['email'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({"message":output})


#login a user
@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Login a User
    """

    return ""

#logout a user
@app.route('/api/auth/logout')
def logout():
    """
    Logs out a user
    """

    return ""

#reset-password
@app.route('/api/auth/reset-password')
def reset_password():
    """
    Resets password
    """

    return ""

#create a new event

@app.route('/api/events', methods=['POST'])
def create_event():
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
def update_event(eventId):
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
def delete_event(eventId):
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
def retrieve_events():
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
@app.route('/api/events/<eventId>', methods=['GET'])
def get_one_event(eventId):

    event = Event.query.filter_by(title=eventId).first()

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
def rsvp_event(eventId):
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
def rsvp_guests():
    """
    Retrieves a list of users who have event reservations
    """

    return ""


if __name__ == '__main__':
    app.run(debug=True)
