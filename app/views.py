from app import app, db
from app.models import Location
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib

API_KEY = 'ff8f4b0a5a464a27827c362ee3b64ae0'
BASE_URL = 'https://api.opencagedata.com/geocode/v1/json?'

class InvalidLocationError(Exception):
    pass

class InWaterError(Exception):
    pass

def get_location_data(lat, long):
    vars = {"key": API_KEY, "q": str(lat) + " " + str(long), "pretty": 1}
    req_url = BASE_URL + urllib.parse.urlencode(vars)
    response = requests.get(req_url).json()

    if len(response["results"]) == 0:
        raise InvalidLocationError
        
    if "city" in response["results"][0]["components"]:
        city = response["results"][0]["components"]["city"]
    if "state" in response["results"][0]["components"]:
        state = response["results"][0]["components"]["state"]
    if "country" in response["results"][0]["components"]:
        country = response["results"][0]["components"]["country"]
    if "body_of_water" in response["results"][0]["components"]:
        raise InWaterError
    if "unknown" in response["results"][0]["components"]:
        # Check if this is actually invalid
        pass
    return city,state,country


# Sends city, state, location data for a pending pin
@app.route('/api/geocoder', methods=['POST'])
def pending_pin():
    if request.method == "POST":
        lat_data = request.json["lat"]
        long_data = request.json["long"]
        try:
            city_data,state_data,country_data = get_location_data(lat_data,long_data)
        except InvalidLocationError:
            return jsonify(success=False, city="", state="", country="", message="Invalid location")
        except InWaterError:
            return jsonify(success=False, city="", state="", country="", message="Cannot add pin in body of water")

        return jsonify(success=True, city=city_data, state=state_data, country=country_data)

# REST API will be in format like...
@app.route('/api/locations', methods=['GET', 'POST'])
def locations():
    # Still need to account for nullable locations
    # Probably a sequence of statements like "if 'city' in request.json..." etc
    # Some locations might not have associated city, state, county (in the ocean, in another country...)
    if request.method == "POST":
        lat_data = request.json["lat"]
        long_data = request.json["long"]
        city_data, state_data, country_data = get_location_data(lat_data, long_data)

        # By default, the lid will auto-increment (when not specified in the constructor)
        location_db = Location(lat = lat_data, long = long_data, city = city_data,
                                state = state_data, country = country_data,
                                visit_date = datetime.datetime.now())
        db.session.add(location_db)
        db.session.commit()
        return jsonify(success=True, message="Added to database")

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
def responses():
    # Similar to add_location
    return "Responses endpoint"

# Note: other routes involve GETting the analytics about each
# location. /api/responses/count? Not sure how this should be setup..

@app.route('/')
def index():
    return 'Working!'