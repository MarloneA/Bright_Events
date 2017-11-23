
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique = True)
    name = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(30))
    admin = db.column(db.Boolean)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(50))
    category = db.Column(db.String(50))
    location = db.Column(db.String(50))
    description = db.Column(db.String)
    date_added = db.Column(db.Integer)
