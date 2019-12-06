from app import app, db
from app.models import AnimalLocations
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib
from base64 import b64encode
from flask_cors import CORS, cross_origin

GEO_API_KEY = 'ff8f4b0a5a464a27827c362ee3b64ae0'
REV_GEO_BASE_URL = 'https://api.opencagedata.com/geocode/v1/json?'

class InvalidLocationError(Exception):
    pass

# function call to opencagedata API to reverse geocode
def get_lat_long(address):
    vars = {"q": address, "key": GEO_API_KEY, "pretty": 1}
    req_url = REV_GEO_BASE_URL + urllib.parse.urlencode(vars)
    response = requests.get(req_url).json()
    lat, long = None, None

    if len(response["results"]) == 0:
        raise InvalidLocationError

    if "lat" in response["results"][0]["geometry"]:
        lat = response["results"][0]["geometry"]["lat"]
    if "lng" in response["results"][0]["geometry"]:
        long = response["results"][0]["geometry"]["lng"]

    return lat,long

# endpoint used if the latitude, longitude of the location is unknown
@app.route('/api/animal_locations/address', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def animalLocationsAddress():
    if request.method == "POST":
        address = request.json["address"]

        lat, long = get_lat_long(address)
        name = request.json["animal_name"]
        location = request.json["location_name"]
        year = request.json["placement_year"]
        animal_type = request.json["animal_type"]
        animal_notes = request.json["animal_notes"]
            

        animals_db = AnimalLocations(lat = lat, long = long, animal_name = name, location_name = location, placement_year = year, animal_type = animal_type, animal_notes = animal_notes)

        db.session.add(animals_db)
        db.session.commit()

        return jsonify(success=True, lat = lat, long = long, animal_name = name, location_name = location, placement_year = year, animal_type = animal_type, animal_notes = animal_notes, message = "Added to database")

    if request.method == "GET":
        all_animals = []
        for location in AnimalLocations.query.all():
            image = ""
            if location.animal_images != None:
                image = b64encode(location.animal_images).decode('utf-8')
                
            animals_json = {"coordinates": {"latitude" : location.lat, "longitude": location.long}, "animal_name": location.animal_name, "location_name": location.location_name, "placement_year": location.placement_year, "animal_type": location.animal_type, "animal_notes": location.animal_notes, "animal_images": image}
            all_animals.append(animals_json)
        return jsonify({'animal_locations': all_animals})

    return "No request sent"


# general endpoint used when latitude, longitude known
@app.route('/api/animal_locations', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def animalLocations():
    if request.method == "POST":
        lat_data = request.json["lat"]
        long_data = request.json["long"]
        name = request.json["animal_name"]
        location = request.json["location_name"]
        year = request.json["placement_year"]
        animal_type = request.json["animal_type"]
        animal_notes = request.json["animal_notes"]
        animal_image = request.json["animal_images"]


        image = None
        if animal_image != "":
            file = open(animal_image, "rb")
            image = file.read()
            
        animals_db = AnimalLocations(lat = lat_data, long = long_data, animal_name = name, location_name = location, placement_year = year, animal_type = animal_type, animal_notes = animal_notes, animal_images = image)

        db.session.add(animals_db)
        db.session.commit()
        
        
        return jsonify(success=True, lat = lat_data, long = long_data, animal_name = name, location_name = location, placement_year = year, animal_type = animal_type, animal_notes = animal_notes, animal_images = b64encode(image).decode('utf-8'), message = "Added to database")

    if request.method == "GET":
        all_animals = []
        for location in AnimalLocations.query.all():        
            image = ""
            if location.animal_images != None:
                image = b64encode(location.animal_images).decode('utf-8')

            animals_json = {"coordinates": {"latitude" : location.lat, "longitude": location.long}, "animal_name": location.animal_name, "location_name": location.location_name, "placement_year": location.placement_year, "animal_type": location.animal_type, "animal_notes": location.animal_notes, "animal_images": image}
            all_animals.append(animals_json)
        return jsonify({'animal_locations': all_animals})

    return "No request sent"


# end point used to retrieve all animals at a particular latitude/longitude
@app.route('/api/animal_locations/lat_long', methods=['GET'])
@cross_origin(supports_credentials=True)
def lat_long():
    if request.method == "GET":
        lat_data = request.args.get('latitude')
        long_data = request.args.get('longitude')

        all_animals = []
        for location in AnimalLocations.query.filter(AnimalLocations.lat==lat_data, AnimalLocations.long==long_data).all():
            animals_json = {"coordinates": {"latitude": location.lat, "longitude": location.long}, "animal_name": location.animal_name, "location_name": location.location_name, "placement_year": location.placement_year, "animal_type": location.animal_type, "animal_notes": location.animal_notes, "animal_images": b64encode(location.animal_images).decode('utf-8')}
            all_animals.append(animals_json)
        return jsonify({"animal_locations": all_animals})

    return "No request sent"
