from app import app, db
from app.models import AnimalLocations
from flask import jsonify, make_response, request, url_for
import requests, datetime, urllib
import csv

def addAnimals():
    animal_file = open("AnimalLocations.csv", 'r')
    animal_reader = csv.reader(animal_file, delimiter=',', quotechar='"')
    next(animal_reader)
    for row in animal_reader:
        b64_image = None
        image = ''

        if(row[7] != ""):
            file = open(row[7].replace('\n','').strip(), "rb")
            image = file.read()

        animal = AnimalLocations(animal_name=row[0], lat=row[5], long=row[6], location_name=row[2], placement_year=row[3], animal_type=row[1], animal_notes=row[4], animal_images=image)
        db.session.add(animal)
        db.session.commit()
    animal_file.close()

