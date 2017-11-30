from data import users, events

class User():

    def __init__(self, id, name, email, password, rsvp):
        self.id=id
        self.name=name
        self.email=email
        self.password=password
        self.rsvp=rsvp

class Event():

    def __init__(self, id, title, category, location, description):
        self.id=id
        self.title=title
        self.category=category
        self.location=location
        self.description=description
