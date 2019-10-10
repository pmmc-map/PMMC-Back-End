from flask import Flask, jsonify, make_response, request, url_for
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# This is just a test, we will need to separate the models into classes
# so it isnt too messy
class Location(db.Model):
	# Primary key will auto increment
    lid = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    state = db.Column(db.String(128), nullable=True)
    country = db.Column(db.String(128), nullable=False)
    # Might need to filter visitors by month eventually
    visit_date = db.Column(db.DateTime)
    # Add lon/lat, String?

class Response(db.Model):
    # I have no idea what the fields will be

# REST API will be in format like...
@app.route('/api/locations')
def add_location():
    # Maybe location data will be given in the POST
    # Parse json POST data into location object
    # Create connection to db, db.session.add(new location)
    pass

@app.route('/api/responses')
def add_response():
    # Similar to add_location
    pass

# Note: other routes involve GETting the analytics about each
# location. /api/responses/count? Not sure how this should be setup..

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__=="__main__":
	app.run()
