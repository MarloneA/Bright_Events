from flask import Flask, jsonify, request

app = Flask(__name__)

users = [{"name":"Marlone","email":"marlone911@gmail.com"},{"name":"Prestone","email":"pres911@gmail.com"},{"name":"Daltone","email":"dalt911@gmail.com"}]
events = [{"title":"Rumba","category":"dance"},{"title":"Flamenco","category":"mariachi"},{"title":"Picado","category":"tango"}]
logged_in = []
logged_out = []
updated_passwords = []
RSVP = [{"name":"Uno"},{"name":"miho"},{"name":"punto"}]


#create a new user
@app.route('/api/auth/register', methods = ['POST'])
def create_user():

    #creates a new user and adds them to the list of users
    user = {'name':request.json['name'],'email':request.json['email']}
    users.append(user)

    return jsonify({"users":users})

#login a user
@app.route('/api/auth/login', methods = ['POST'])
def login_user():

    #confirm if a user is in the list of users

    login_user = {'username':request.json['username']}
    logged_in.append(login_user)

    return jsonify({"logged_in":logged_in})


#logs out a user
@app.route('/api/auth/logout', methods = ['POST'])
def logout_user():

    #confirm whether a user has been logged out from login
    logout_user = {'username':request.json['username']}
    logged_out.append(logout_user)

    return jsonify({"logged_out":logged_out})

#resets password
@app.route('/api/auth/reset-password', methods = ['POST'])
def reset_password():

    #update the existing password
    password_reset = {'password':request.json['password']}
    updated_passwords.append(password_reset)

    return jsonify({"updated_passwords":updated_passwords})

#creates an event
@app.route('/api/events', methods = ['POST'])
def create_event():

    event = {'title':request.json['title'],'category':request.json['category']}
    events.append(event)

    return jsonify({"events":events})

#updates an event
@app.route('/api/events/<categoryId>', methods = ['PUT'])
def update_event(categoryId):

    event = [event for event in events if event["title"] == categoryId]
    event[0]["title"] = request.json["title"]

    return jsonify({"events":event[0]})

#deletes an event
@app.route('/api/events/<eventId>', methods = ['DELETE'])
def delete_event(eventId):

    event = [event for event in events if event["title"] == eventId]
    events.remove(event[0])

    return jsonify({"events":events})




#retrieves all events
@app.route('/api/events', methods = ['GET'])
def retrieve_all_events():
    return jsonify({"events":events})

#retrieves one event
@app.route('/api/events/<string:eventId>', methods = ['GET'])
def retrieve_one_event(eventId):

    event = [event for event in events if event["title"] == eventId]

    return jsonify({"events":event[0]})

#allows user to RSVP
@app.route('/api/event/<eventId>/rsvp', methods = ['POST'])
def rsvp_event(eventId):

    reserved_guests = {'name':request.json['name'],'event':request.json['event']}
    RSVP.append(reserved_guests)

    return jsonify({"RSVP":RSVP})

#retrieves all guests
@app.route('/api/event/<eventId>/rsvp', methods = ['GET'])
def retrieve_all_guests(eventId):
    return jsonify({"RSVP":RSVP})

if __name__ == "__main__":
    app.run(debug=True)
