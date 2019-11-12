
from app import app, db
from app.models import Location, AnimalLocations, Count, DonationVisit
from app.survey import Question, Response, Option, VisitorResponse
from app.gmail import send_email
from flask import jsonify, make_response, request, url_for, redirect
import requests, datetime, urllib
from flask_cors import CORS, cross_origin
from math import cos, asin, sqrt

GEO_API_KEY = 'ff8f4b0a5a464a27827c362ee3b64ae0'
GEO_BASE_URL = 'https://api.opencagedata.com/geocode/v1/json?'
PMMC_LAT = 33.5729488
PMMC_LONG = -117.7624671

IMAGE_API_CX = "006863879937283909592:yqzj4vzeazr"
IMAGE_API_KEY = 'AIzaSyBD8SsoOb7ZbeKM-_4D1dPvXRQggTqLoR8'
IMAGE_API_URL = 'https://www.googleapis.com/customsearch/v1'
FULL_URL = IMAGE_API_URL + "?key=" + IMAGE_API_KEY + "&cx=" + IMAGE_API_CX + "&q="

DONATION_URL = "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=6K7QH9UVKF924"

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

@app.route('/api/locations/counts', methods=['GET'])
@cross_origin(supports_credentials=True)
def location_counts():
    total_visitors = Location.query.count()
    country_count = Location.query.with_entities(Location.country).distinct().count()
    state_count = Location.query.filter_by(country="USA").with_entities(Location.state).distinct().count()
    # Confirm that these are equivalent
    # states = set()
    # for l in Location.query.all():
    #     if l.country == "USA":
    #         states.add(l.state)
    # state_count = len(states)
    return jsonify(success=True, total_visitors=total_visitors, unique_states = state_count, unqiue_countries=country_count)

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

@app.route('/api/images/city', methods=['POST'])
@cross_origin(supports_credentials=True)
def city_image():
    if request.method == "POST":
        if request.headers['Content-Type'] == 'application/json':
            city = request.json['city']
            search_type = "&searchType=image"
            img_size = "&imgSize=large"
            req_url = FULL_URL + city + " landmark" + search_type + img_size
        response = {"city": requests.get(req_url).json()['items'][0]['link']}
        return jsonify(response), 200

# GETs all questions in questions database table
# POST a new question with provided text
# DELETE an existing question by sending qid
@app.route('/api/questions', methods=['GET', 'POST', 'DELETE'])
@cross_origin(supports_credentials=True)
def all_questions():
    if request.method == "GET":
        all_questions = []
        for question in Question.query.filter_by(active=True).all():
            question_json = {"qid": question.qid, "text": question.text}
            all_questions.append(question_json)
        return jsonify({'questions': all_questions})
    if request.method == "POST":
        # Add new question (at new qid)
        question_text = request.json["text"]
        question = Question(text=question_text, active=True)
        db.session.add(question)
        db.session.commit()
        return jsonify(success=True, message="New question added")  
    if request.method == "DELETE":
        qid = request.json["qid"]
        question = Question.query.filter_by(qid=qid).first()
        question.active = False
        db.session.commit()
        return jsonify(success=True, message="Question deleted (set to inactive)")           

# GET question based on question_id, return json of question
# POST to question by adding a Response associated with that question_id
# DELETE a question by qid (makes question inactive)
@app.route('/api/questions/qid/<qid>', methods=['GET', 'POST', 'DELETE'])
@cross_origin(supports_credentials=True)
def question(qid):
    if request.method == "GET":
        question = Question.query.filter_by(qid=qid).first()
        question_json = {"qid": question.qid, "text": question.text}
        return jsonify({'question': question_json})
    if request.method == "POST":
        # For now, just an updated question
        if "updated_text" in request.json:
            updated_text = request.json["updated_text"]
            question = Question.query.filter_by(qid = qid).first()
            question.text = updated_text
        else:
            return jsonify(success=False, message = "No updated question sent")
        db.session.commit()
        return jsonify(success=True, message="Question text changed")
    if request.method == "DELETE":
        question = Question.query.filter_by(qid=qid).first()
        question.active = False
        db.session.commit()
        return jsonify(success=True, message="Question deleted (set to inactive)")


# GET all options, mainly for debugging
# DELETE a option by oid
@app.route('/api/options', methods=['GET', 'POST', 'DELETE'])
@cross_origin(supports_credentials=True)
def all_options():
    if request.method == "GET":
        all_options = []
        for option in Option.query.all():
            option_json = {"oid": option.oid, "qid": option.qid, "text": option.text}
            all_options.append(option_json)
        return jsonify({'options': all_options})      
    if request.method == "DELETE":
        oid = request.json["oid"]
        option = option.query.filter_by(oid=oid).first()
        db.session.delete(option)
        db.session.commit()
        return jsonify(success=True, message="option oid " + str(oid) + " deleted")

# GET a single option by oid
# POST to edit a option, send updated_text
# DELETE to delete a option by oid
@app.route('/api/options/oid/<oid>', methods=['GET', 'POST', 'DELETE'])
@cross_origin(supports_credentials=True)
def single_option(oid):
    if request.method == "GET":
        option = option.query.filter_by(oid=oid).first()
        option_json = {"oid": option.oid, "qid": option.qid, "text": option.text}
        return jsonify({'option': option_json})      
    if request.method == "POST":
        option = Option.query.filter_by(oid=oid).first()
        updated_text = request.json["updated_text"]
        option.text = updated_text
        db.session.commit()
        return jsonify(success=True, message="option text updated")
    if request.method == "DELETE":
        option = Option.query.filter_by(oid=oid).first()
        db.session.delete(option)
        db.session.commit()
        return jsonify(success=True, message="option oid " + str(oid) + " deleted")


# GET options associated with a question_id
# POST option associated with a question_id
@app.route('/api/options/qid/<qid>', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def question_options(qid):
    if request.method == "GET":
        all_options = []
        for option in Option.query.filter_by(qid=qid):
            option_json = {"oid": option.oid, "qid": option.qid, "text": option.text}
            all_options.append(option_json)
        return jsonify({'options': all_options})
    if request.method == "POST":
        option_text = request.json["text"]
        option = Option(text = option_text, qid=qid)
        db.session.add(option)
        db.session.commit()
        return jsonify(success=True)

@app.route('/api/visitor_response', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def visitor_response():
    if request.method == "GET":
        all_responses = []
        for response in VisitorResponse.query.all():
            response_json = {"oid": response.oid, "vr_timestamp": response.vr_timestamp}
            all_responses.append(response_json)
        return jsonify({'responses': all_responses})    
    if request.method == "POST":
        oid = request.json["oid"]
        visitor_response = VisitorResponse(oid = oid, vr_timestamp = datetime.datetime.now())
        db.session.add(visitor_response)
        db.session.commit()
        return jsonify(success=True, message="Visitor response added to database")

@app.route('/admin/email', methods=["POST"])
@cross_origin(supports_credentials=True)
def email():
    ## TODO: email that attaches CSV files
    if request.method == "POST":
        if "email_address" in request.json:
            to_email = request.json["email_address"]
        else:
            return jsonify(success=False, message="No address sent")
        subject = "Map Application Data " + str(datetime.datetime.now().strftime("%Y-%m-%d"))
        body = "Hello!\n\nAttached are the analytics spreadsheet files." \
                " These files report survey responses, new pin information, and visits to the donation site.\n\n" \
                " Have a great day!"
        # files = tablesToCsv() ... 
        files = []
        try:
            send_email(to_email, subject, body, files)
        except Exception as e:
            return jsonify(success=False, message="Could not send email. Error: " + str(e))
        return jsonify(success=True, message="Email sent to " + to_email + " successfully")

# Generic Count database used for storing incrementing values.
# For now, we are keeping a Count of the rescued animal total 
# to display on the main page.
# POST to create a new count
# GET to view all existing counts
@app.route('/admin/count', methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
def count():
    if request.method == "GET":
        all_counts = []
        for count in Count.query.all():
            count_json = {"name": count.name, "total": count.total}
            all_counts.append(count_json)
        return jsonify({'counts': all_counts})
    if request.method == "POST":
        # Add a new running counter to the Count database 
        new_total = 0
        if "total" in request.json:
            new_total = request.json["total"]
        if "name" in request.json:
            new_name = request.json["name"]
        else:
            return jsonify(success=False, message="'name' not specified in attempt to create new Count")
        count = Count(name=new_name, total=new_total)
        db.session.add(count)
        db.session.commit()
        return jsonify(success=True, message=name + " count added to table with a count of " + str(new_total))

# Endpoint to update count entries
# Specifically, updating the "rescues" for the PMMC admins
# POST a "new_total" to the count to change the total.
# Note: This is in replacement of the old "Rescues" table.
@app.route('/admin/count/<name>', methods=["POST"])
@cross_origin(supports_credentials=True)
def update_count(name):
    if request.method == "POST":
        new_total = 0
        if "new_total" in request.json:
            new_total = request.json["new_total"]
        else:
            return jsonify(success=False, message="'new_total' not specified in attempt to update the " + name + " count")
        count = Count.query.filter_by(name=name).first()
        if count == None:
            return jsonify(success=False, message="No count named " + name + " exists in this database")
        count.total = new_total
        db.session.commit()
        return jsonify(success=True, message=name + " count updated to " + str(new_total))

@app.route('/api/donation_redirect', methods=["GET"])
@cross_origin(supports_credentials=True)
def donation_redirect():
    if request.method == "GET":
        visit = DonationVisit(dv_timestamp=datetime.datetime.now())
        db.session.add(visit)
        db.session.commit()
        return redirect(DONATION_URL)

@app.route('/api/donation_visits', methods=["GET"])
@cross_origin(supports_credentials=True)
def donation_visits():
    if request.method == "GET":
        all_donation_visits = []
        for dv in DonationVisit.query.all():
            dv_json = {"id": dv.dvid, "timestamp": dv.dv_timestamp}
            all_donation_visits.append(dv_json)
        return jsonify({'donation_visits': all_donation_visits})

# TODO: It might be a good idea to have separate files for the /api/ endpoints and the /admin/ endpoints
# admin endpoints are tools that are specific will be used by the PMMC folks rather than us.
# Should Count be an admin tool because they are specifically changing it? 
# This would make the survey responses admin too...
# Thinking

@app.route('/')
def index():
    return 'Working!'
