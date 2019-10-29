
from app import app, db
from app.models import Location
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib

GEO_API_KEY = 'ff8f4b0a5a464a27827c362ee3b64ae0'
GEO_BASE_URL = 'https://api.opencagedata.com/geocode/v1/json?'

IMAGE_API_CX = "006863879937283909592:yqzj4vzeazr"
IMAGE_API_KEY = 'AIzaSyBD8SsoOb7ZbeKM-_4D1dPvXRQggTqLoR8'
IMAGE_API_URL = 'https://www.googleapis.com/customsearch/v1'
FULL_URL = IMAGE_API_URL + "?key=" + IMAGE_API_KEY + "&cx=" + IMAGE_API_CX + "&q="


class InvalidLocationError(Exception):
    pass

class InWaterError(Exception):
    pass

def get_location_data(lat, long):
    vars = {"key": GEO_API_KEY, "q": str(lat) + " " + str(long), "pretty": 1}
    req_url = GEO_BASE_URL + urllib.parse.urlencode(vars)
    response = requests.get(req_url).json()
    city,state,country = None,None,None

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
        # This is actually not invalid but we need to check for
        # parts of the ocean that aren't a "body of water"
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

        # Calculate counts of city/state/country for front end analytics
        city_count, state_count, country_count = 0,0,0
        if city_data:
            city_count = Location.query.filter_by(city=city_data).count()
        if state_data:
            state_count = Location.query.filter_by(state=state_data).count()
        if country_data:
            country_count = Location.query.filter_by(country=country_data).count()
        return jsonify(success=True, city=city_data, state=state_data, country=country_data, 
                       city_count = city_count, state_count = state_count, country_count = country_count,
                       message="Added to database")

    if request.method == "GET":
        # This is like querying the database for all pinned locations
        all_locations = []
        for location in Location.query.all():
            location_json = {"lat": location.lat, "long": location.long, "city": location.city,
                              "state": location.state, "country": location.country, "visit_date": location.visit_date}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations})
    return "No request sent"

@app.route('/api/locations/country/<country_name>', methods=['GET'])
def country(country_name):
    if request.method == "GET":
        # This is like querying the database
        # Equivalent to SELECT * FROM Location WHERE country = country_name
        all_locations = []
        for location in Location.query.filter_by(country=country_name).all():
            location_json = {"lat": location.lat, "long": location.long, "city": location.city,
                              "state": location.state, "country": location.country, "visit_date": location.visit_date}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations}) 

@app.route('/api/locations/city/<city_name>', methods=['GET'])
def city(city_name):
    if request.method == "GET":
        all_locations = []
        for location in Location.query.filter_by(city=city_name).all():
            location_json = {"lat": location.lat, "long": location.long, "city": location.city,
                              "state": location.state, "country": location.country, "visit_date": location.visit_date}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations})

@app.route('/api/locations/state/<state_name>', methods=['GET'])
def state(state_name):
    if request.method == "GET":
        all_locations = []
        for location in Location.query.filter_by(state=state_name).all():
            location_json = {"lat": location.lat, "long": location.long, "city": location.city,
                              "state": location.state, "country": location.country, "visit_date": location.visit_date}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations})

@app.route('/api/locations/city', methods=['POST'])
def city_image():
	if request.method == "POST":
		if request.headers['Content-Type'] == 'application/json':
			city = request.json['city']
			search_type = "&searchType=image"
			img_size = "&imgSize=large"
			req_url = FULL_URL + city + search_type + img_size
			response = {"city": requests.get(req_url).json()['items'][0]['link']}
			return jsonify(response), 200

@app.route('/api/responses')
def responses():
    # Similar to add_location
    return "Responses endpoint"

# Note: other routes involve GETting the analytics about each
# location. /api/responses/count? Not sure how this should be setup..

@app.route('/')
def index():
    return 'Working!'
