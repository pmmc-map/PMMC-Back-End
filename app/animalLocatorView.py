from app import app, db
from app.models import AnimalLocations
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib

@app.route('api/animal_locations', methods=['Get', 'POST'])
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

        animals_db = AnimalLocations(lat = lat_data, long = long_data, animal_name = name, location_name = location, placement_year = year, animal_type = animal_type, animal_notes = animal_notes)

        db.session.add(animals_db)
        db.session.commit()

        return jsonify(success=True, lat = lat_data, long = long_data, animal_name = name, location_name = location, placement_year = year, animal_type = type, animal_notes = animal_notes, message = "Added to database")

    return "No request sent"
    
