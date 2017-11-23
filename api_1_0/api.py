from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/auth/register', methods = ['POST'])
def create_user():
    return jsonify({'message':'registration succesful'})

#login a user
@app.route('/api/auth/login', methods = ['POST'])
def login_user():
    return jsonify({'message':'user logged in'})

#logs out a user
@app.route('/api/auth/login', methods = ['POST'])
def logout_user():
    return jsonify({'message':'user logged out'})

#resets password
@app.route('/api/auth/reset-password', methods = ['POST'])
def reset_password():
    return jsonify({'message':'password reset'})


#creates an event
@app.route('/api/events', methods = ['POST'])
def create_event():
    return jsonify({'message':'event created'})

#updates an event
@app.route('/api/events/<eventId>', methods = ['PUT'])
def update_event(eventId):
    return jsonify({'message':'event updated'})

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
