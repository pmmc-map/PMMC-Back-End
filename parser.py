from app import app, db
from app.models import AnimalLocations
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib
from base64 import b64encode

if __name__=="__main__":
    animal_file = open("AnimalLocations.txt", 'r')
    for line in animal_file:
        list = line.strip().split('*')
        json = {}

        b64_image = None
        image = None

        if(list[7] != ""):
            file = open(list[7], "rb")
            image = file.read()
            
        animal = AnimalLocations(animal_name=list[2], lat=list[5], long=list[6], location_name=list[0], placement_year=list[1], animal_type=list[3], animal_notes=list[4], animal_images=image)
        db.session.add(animal)
        db.session.commit()
        
    animal_file.close()
    
    
