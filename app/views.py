from app import app, db
from app.models import Location
from app.survey import Question, Response
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib
from flask_cors import CORS, cross_origin
from math import cos, asin, sqrt

GEO_API_KEY = 'ff8f4b0a5a464a27827c362ee3b64ae0'
GEO_BASE_URL = 'https://api.opencagedata.com/geocode/v1/json?'
PMMC_LAT = 33.5729488
PMMC_LONG = -117.7624671

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
    if "county" in response["results"][0]["components"] and not city:
        city = response["results"][0]["components"]["county"]
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

# This is an implementation of the Haversine formula for distances on a globe
# Distance returned is in miles, as a crow flies
def calculate_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) * 0.621371


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

# GETs all pin location data
# POST a new location to the pin location database table
@app.route('/api/locations', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
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

        distance = calculate_distance(PMMC_LAT, PMMC_LONG, lat_data, long_data)
        return jsonify(success=True, city=city_data, state=state_data, country=country_data,
                       city_count = city_count, state_count = state_count, country_count = country_count,
                       message="Added to database", distance = distance)
                       

    if request.method == "GET":
        # This is like querying the database for all pinned locations
        all_locations = []
        for location in Location.query.all():
            location_json = {"coordinates": {"latitude": location.lat, "longitude": location.long}, "city": location.city,
                              "state": location.state, "country": location.country, "visit_date": location.visit_date}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations})
    return "No request sent"

# GETs location based on country name
@app.route('/api/locations/country/<country_name>', methods=['GET'])
@cross_origin(supports_credentials=True)
def country(country_name):
    if request.method == "GET":
        # This is like querying the database
        # Equivalent to SELECT * FROM Location WHERE country = country_name
        all_locations = []
        for location in Location.query.filter_by(country=country_name).all():
            location_json = {"coordinates": {"latitude": location.lat, "longitude": location.long}, "city": location.city,
                              "state": location.state, "country": location.country, "visit_date": location.visit_date}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations})

@app.route('/api/locations/city/<city_name>', methods=['GET'])
def city(city_name):
    if request.method == "GET":
        all_locations = []
        for location in Location.query.filter_by(city=city_name).all():
            location_json = {"coordinates": {"latitude": location.lat, "longitude": location.long}, "city": location.city,
                              "state": location.state, "country": location.country, "visit_date": location.visit_date}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations})

@app.route('/api/locations/state/<state_name>', methods=['GET'])
@cross_origin(supports_credentials=True)
def state(state_name):
    if request.method == "GET":
        all_locations = []
        for location in Location.query.filter_by(state=state_name).all():
            location_json = {"coordinates": {"latitude": location.lat, "longitude": location.long}, "city": location.city,
                              "state": location.state, "country": location.country, "visit_date": location.visit_date}
            all_locations.append(location_json)
        return jsonify({'locations': all_locations})


# GETs all questions in questions database table
@app.route('/api/questions', methods=['GET'])
@cross_origin(supports_credentials=True)
def all_questions():
    if request.method == "GET":
        all_questions = []
        for question in Question.query.all():
            question_json = {"qid": question.qid, "text": question.text}
            all_questions.append(question_json)
        return jsonify({'questions': all_questions})


# GET question based on question_id, return json of question
# POST to question by adding a Response associated with that question_id
# TODO: Should this POST be in /questions or /responses? In both for now
@app.route('/api/questions/<qid>', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def question(qid):
    if request.method == "GET":
        all_questions = []
        # This should only have one response, but displaying all for debugging
        for question in Question.query.filter_by(qid=qid):
            question_json = {"qid": question.qid, "text": question.text}
            all_questions.append(question_json)
        return jsonify({'question': all_questions})
    if request.method == "POST":
        response_text = request.json["text"]
        response = Response(text = response_text, qid=qid)
        db.session.add(response)
        db.session.commit()
        return jsonify(success=True)

# GET responses associated with a question_id
# POST response associated with a question_id
# TODO: Again, decide where this POST should live
@app.route('/api/responses/<qid>', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def response(qid):
    if request.method == "GET":
        all_responses = []
        # This should only have one response, but displaying all for debugging
        for response in Response.query.filter_by(qid=qid):
            response_json = {"rid": response.rid, "qid": response.qid, "text": response.text}
            all_responses.append(response_json)
        return jsonify({'response': all_responses})
    if request.method == "POST":
        response_text = request.json["text"]
        response = Response(text = response_text, qid=qid)
        db.session.add(response)
        db.session.commit()
        return jsonify(success=True)

# Note: other routes involve GETting the analytics about each
# location. /api/responses/count? Not sure how this should be setup..

@app.route('/')
def index():
    return 'Working!'
