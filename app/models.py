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
    # Add lon/lat, String?

#class Response(db.Model):
    # I have no idea what the fields will be
 #   pass