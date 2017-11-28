"""Simple Flask API"""

from flask import Flask, jsonify, request
from models import users, events, logged_in, logged_out, updated_passwords, RSVP

app = Flask(__name__)

#create a new user
@app.route('/api/auth/register', methods=['POST'])
def create_user():
    """
    Creates a user account
    """
    user = {'id':request.json['id'], 'name':request.json['name'], 'email':request.json['email'], 'password':request.json['password']}
    users.append(user)

    return jsonify({"users":users})

#login a user
@app.route('/api/auth/login', methods=['POST'])
def login_user():
    """
    Logs in a user
    """

    log = {'email':request.json['email']}

    current_users = [user for user in users if user['email'] == request.json['email']]
     
    if current_users == []:
        return jsonify({"message":"No user found with the given email"})
    logged_in.append(log)

    return jsonify({"logged_in":logged_in})


#logs out a user
@app.route('/api/auth/logout', methods=['POST'])
def logout_user():
    """
    Logs out a user
    """

    logout = {'username':request.json['username']}
    logged_out.append(logout)

    return jsonify({"logged_out":logged_out})

#resets password
@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """
    Resets password
    """

    password_reset = {'password':request.json['password']}
    updated_passwords.append(password_reset)

    return jsonify({"updated_passwords":updated_passwords})

#creates an event
@app.route('/api/events', methods=['POST'])
def create_event():
    """
    Creates an Event
    """

    event = {'id':35, 'title':request.json['title'], 'category':request.json['category']}
    events.append(event)

    return jsonify({"events":events})

#updates an event
@app.route('/api/events/<string:eventId>', methods=['PUT'])
def update_event(eventId):
    """
    Updates an Event
    """

    event = [evnt for evnt in events if evnt["title"] == eventId]

    if event == []:
        return jsonify({"message":"No such event found"})

    event[0]["title"] = request.json["title"]

    return jsonify({"events":event[0]})

#deletes an event
@app.route('/api/events/<eventId>', methods=['DELETE'])
def delete_event(eventId):
    """
    Deletes an event
    """


    event = [event for event in events if event["title"] == eventId]

    if event == []:
        return jsonify({"message":"No such event found"})

    events.remove(event[0])

    return jsonify({"events":events})


#retrieves all events
@app.route('/api/events', methods=['GET'])
def retrieve_events():
    """
    Retrieves events
    """

    return jsonify({"events":events})

#allows user to RSVP
@app.route('/api/event/<eventId>/rsvp', methods=['POST'])
def rsvp_event(eventId):
    """
    Allows a user to RSVP to an event
    """

    for user in users:
        if user['name'] == eventId:
            reserved_guests = {'name':eventId, 'event':request.json['event']}
            RSVP.append(reserved_guests)
    return jsonify({"RSVP":RSVP})



if __name__ == "__main__":
    app.run(debug=True)
