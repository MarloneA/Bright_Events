@api.route('/api/auth/register', methods = ['POST'])
def create_user():
    return jsonify({'message':'registration succesful'})

#login a user
@api.route('/api/auth/login', methods = ['POST'])
def login_user():
    return jsonify({'message':'user logged in'})

#logs out a user
@api.route('/api/auth/login', methods = ['POST'])
def logout_user():
    return jsonify({'message':'user logged out'})

#resets password
@api.route('/api/auth/reset-password', methods = ['POST'])
def reset_password():
    return jsonify({'message':'password reset'})


#creates an event
@api.route('/api/events', methods = ['POST'])
def create_event():
    return jsonify({'message':'event created'})

#updates an event
@api.route('/api/events/<eventId>', methods = ['PUT'])
def update_event(user_id):
    return jsonify({'message':'event updated'})

#deletes an event
@api.route('/api/events/<eventId>', methods = ['DELETE'])
def delete_event(user_id):
    return jsonify({'message':'event deleted'})

#retrieves an event
@api.route('/api/events', methods = ['GET'])
def retrieve_event():
    return jsonify({"message":"retrieved event"})

#allows user to RSVP
@api.route('/api/event/<eventId>/rsvp', methods = ['POST'])
def rsvp_event(user_id):
    return jsonify({"message":"Reserved event"})

#retrieves an event
@api.route('/api/event/<eventId>/rsvp', methods = ['GET'])
def retrieve_all_guests():
    return jsonify({"message":"retrieved guests in attendance"})
