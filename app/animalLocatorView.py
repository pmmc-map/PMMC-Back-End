from app import app, db
from app.models import AnimalLocations
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib


@app.route('/api/animal_locations', methods=['GET', 'POST'])
def animalLocations():
    print("request ", request)
    if request.method == "POST":
        print("JSON ", request.json)
        lat_data = request.json["lat"]
        long_data = request.json["long"]
        name = request.json["animal_name"]
        location = request.json["location_name"]
        year = request.json["placement_year"]
        animal_type = request.json["animal_type"]
        animal_notes = request.json["animal_notes"]

        animals_db = AnimalLocations(lat = lat_data, long = long_data, animal_name = name, location_name = location, placement_year = year, animal_type = animal_type, animal_notes = animal_notes)

        db.session.add(animals_db)
        db.session.commit()

        return jsonify(success=True, lat = lat_data, long = long_data, animal_name = name, location_name = location, placement_year = year, animal_type = animal_type, animal_notes = animal_notes, message = "Added to database")

    if request.method == "GET":
        all_animals = []
        for location in AnimalLocations.query.all():
            animals_json = {"coordinates": {"latitude" : location.lat, "longitude": location.long}, "animal_name": location.animal_name, "location_name": location.location_name, "placement_year": location.placement_year, "animal_type": location.animal_type, "animal_notes": location.animal_notes}
            all_animals.append(animals_json)
        return jsonify({'animal_locations': all_animals})

    return "No request sent"



@app.route('/api/animal_locations/lat_long', methods=['GET'])
def lat_long():
    if request.method == "GET":
        lat_data = request.args.get('latitude')
        long_data = request.args.get('longitude')

        all_animals = []
        for location in AnimalLocations.query.filter(AnimalLocations.lat==lat_data, AnimalLocations.long==long_data).all():
            animals_json = {"coordinates": {"latitude": location.lat, "longitude": location.long}, "animal_name": location.animal_name, "location_name": location.location_name, "placement_year": location.placement_year, "animal_type": location.animal_type, "animal_notes": location.animal_notes}
            all_animals.append(animals_json)
        return jsonify({"animal_locations": all_animals})

    return "No request sent"
    
