from app import app, db
from app.models import AnimalLocations
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib

def addAnimals():
    animal_file = open("AnimalLocations.txt", 'r')
    for line in animal_file:
        list = line.strip().split('/')
        animal = AnimalLocations(animal_name=list[2], lat=list[5], long=list[6], location_name=list[0], placement_year=list[1], animal_type=list[3], animal_notes=list[4] )
        db.session.add(animal)
        db.session.commit()
    animal_file.close()
    