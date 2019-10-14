from app import app, db
from app.models import Location
from flask import jsonify, make_response, request, url_for
import requests

# REST API will be in format like...
@app.route('/api/locations', methods=['GET', 'POST'])
def add_location():
    # Still need to account for nullable locations
    # Some locations might not have associated city, state, county (in the ocean, in another country...)
    if request.method == "POST":
        # The data is sent as json
        lat_data = request.json["lat"]
        long_data = request.json["long"]
        city_data = request.json["city"]
        state_data = request.json["state"]
        country_data = request.json["country"]
        #visit_date = request.json["visit"]
        location_db = Location(lat = lat_data, long = long_data, city = city_data,
                                state = state_data, country = country_data)
        db.session.add(location_db)
        db.session.commit()
        return jsonify(success=True)    
    if request.method == "GET":
        # This is like querying the database
        all_locations = []
        for location in Location.query.all():
            location_json = {"lat": location.lat, "long": location.long, "city": location.city,
                              "state": location.state, "country": location.country}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations})
    return "No request sent"

@app.route('/api/responses')
def add_response():
    # Similar to add_location
    return "Test"
    #pass

# Note: other routes involve GETting the analytics about each
# location. /api/responses/count? Not sure how this should be setup..

@app.route('/')
def hello_world():
    return 'Hello, World!'