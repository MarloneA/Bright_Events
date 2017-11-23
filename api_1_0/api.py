from flask import Flask, jsonify, request

app = Flask(__name__)

users = []
user = {}
events = []
event = {}


#create a new user
@app.route('/api/auth/register', methods = ['POST'])
def create_user():

    #creates a new user and adds them to the list of users

    user = request.get_json()
    users.append(user)
    return jsonify(users)


#login a user
@app.route('/api/auth/login', methods = ['POST'])
def login_user():

    #confirm if a user is in the list of users
    return ""


#logs out a user
@app.route('/api/auth/login', methods = ['POST'])
def logout_user():

    #confirm whether a user has been deleted from login
    return ""

#resets password
@app.route('/api/auth/reset-password', methods = ['POST'])
def reset_password():

    #update the existing password
    return ""

#creates an event
@app.route('/api/events', methods = ['POST'])
def create_event():

    event = request.get_json()
    events.append(event)
    return jsonify(events)

#updates an event
@app.route('/api/events/<eventId>', methods = ['PUT'])
def update_event(eventId):

    data = request.get_json()
    #update an existing event
    for event in events:
        if event["name"] == eventId:

            event = data
            events.append(event)
            return jsonify(event)


#deletes an event
@app.route('/api/events/<eventId>', methods = ['DELETE'])
def delete_event(eventId):
    return jsonify({'message':'event deleted'})

#retrieves an event
@app.route('/api/events', methods = ['GET'])
def retrieve_event():
    return jsonify({"message":"retrieved event"})

#allows user to RSVP
@app.route('/api/event/<eventId>/rsvp', methods = ['POST'])
def rsvp_event(eventId):
    return jsonify({"message":"Reserved event"})

#retrieves an event
@app.route('/api/event/<eventId>/rsvp', methods = ['GET'])
def retrieve_all_guests(eventId):
    return jsonify({"message":"retrieved guests in attendance"})

if __name__ == "__main__":
    app.run(debug=True)
