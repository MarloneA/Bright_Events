"""Simple Flask API"""

from flask import Flask, jsonify, request, session
from data import users, events, logged_users
from models import User, Event
import os



app = Flask(__name__)

app.secret_key = os.urandom(24)


#create a new user
@app.route('/api/auth/register', methods=['POST'])
def create_user():
    """
    Creates a user account
    """

    user_id = request.json['id']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    rsvp = request.json['rsvp']

    user = User(user_id, name, email, password, rsvp )

    new = {"user":user.name, "email":user.email, "password":user.password,"rsvp": user.rsvp}


    users.append(new)

    return jsonify({"message":"new user has been created","user":new})

#login a user
@app.route('/api/auth/login', methods=['GET', 'POST'])
def login_user():
    """
    Logs in a user
    """

    if request.method == 'POST':

        for user in users:
            if user['email'] == request.json['email'] and user['password'] == request.json['password']:

                session['user'] = request.json['email']

                return jsonify({"message":"user has been logged in"})

            return jsonify({"message":"Please verify email/password credentials are correct"})



#logs out a user
@app.route('/api/auth/logout', methods=['GET', 'POST'])
def logout_user():
    """
    Logs out a user
    """

    try:
        if session['user'] is not None:
            session.pop('user')
            print session

    except KeyError:
        return jsonify({"message":"no user in session"})

    return jsonify({"message":"User has been logged out"})

#resets password
@app.route('/api/auth/reset-password', methods=['PUT'])
def reset_password():
    """
    Resets password
    """

    user = [usr for usr in users if usr["email"] == request.json["email"]]

    if user == []:
        return jsonify({"message":"The user does not exist"}), 404

    user[0]["password"] = request.json["password"]

    return jsonify({"message":"password updated"})


#creates an event
@app.route('/api/events', methods=['POST'])
def create_event():
    """
    Creates an Event
    """

    event_id = request.json['id']
    title = request.json['title']
    category = request.json['category']
    location = request.json['location']
    description = request.json['description']

    event = Event(event_id, title, category, location, description)

    events.append(event)

    return jsonify({"message ":"new event has been created"})

#updates an event
@app.route('/api/events/<string:eventId>', methods=['PUT'])
def update_event(eventId):
    """
    Updates an Event
    """

    event = [evnt for evnt in events if evnt["id"] == eventId]

    if event == []:
        return jsonify({"message":"No such event found"}), 404

    event[0]["title"] = request.json["title"]
    event[0]["location"] = request.json["location"]
    event[0]["category"] = request.json["category"]
    event[0]["description"] = request.json["description"]

    return jsonify({"message":"event has been succesfully updated"})

#deletes an event
@app.route('/api/events/<eventId>', methods=['DELETE'])
def delete_event(eventId):
    """
    Deletes an event
    """


    event = [event for event in events if event["id"] == eventId]

    if event == []:
        return jsonify({"message":"No such event found"}), 404

    events.remove(event[0])

    return jsonify({"message":"event successfully removed"})


#retrieves all events
@app.route('/api/events', methods=['GET'])
def retrieve_events():
    """
    Retrieves all events
    """

    return jsonify({"events":events})

#allows a user to RSVP
@app.route('/api/event/<eventId>/rsvp', methods=['POST'])
def rsvp_event(eventId):
    """
    Allows a user to RSVP to an event
    """

    check_usr = [usr for usr in users if usr["name"] == eventId]

    if check_usr == []:
        return jsonify({"message":"user not found"}), 404

    check_usr[0]["rsvp"] = True

    return jsonify({"message":"your reservations have been approved"})

#Retrieves a list of users who have reserved for an event
@app.route('/api/events/rsvp', methods=['GET'])
def rsvp_guests():
    """
    Retrieves a list of users who have event reservations
    """
    reserved = [rsvp for rsvp in users if rsvp['rsvp'] == True]

    if reserved == []:
        return jsonify({'message' : 'No reservations found for the user'}), 404


    return jsonify({"Guests":reserved})


if __name__ == "__main__":
    app.run(debug=True)
