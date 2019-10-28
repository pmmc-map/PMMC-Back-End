from app import db

class Location(db.Model):
	# Primary key will auto increment
    lid = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(128), nullable=True)
    state = db.Column(db.String(128), nullable=True)
    country = db.Column(db.String(128), nullable=True)
    # Might need to filter visitors by month eventually
    visit_date = db.Column(db.DateTime, nullable=True)

class AnimalLocations(db.Model):
        #Primary key will auto increment
    alid = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(128), nullable=False)
    long = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    location_name = db.Column(db.String(128), nullable=False) # name of the place animal was placed
    placement_year = db.Column(db.Integer, nullable=True) # Year the animal was placed
    animal_type = db.Column(db.String(128), nullable=True) # Type of animal (eg. seal, sea lion, harbor seal)
    animal_notes = db.Column(b.String(128), nullable=True) # Any notes or facts about animal

class Response(db.Model):
    # I have no idea what the fields will be
    rid = db.Column(db.Integer, primary_key=True)
