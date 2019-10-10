from flask import Flask, jsonify, make_response, request, url_for
import requests
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# This is just a test, we will need to separate the models into classes
# so it isnt too messy
class Location(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    state = db.Column(db.String(128), nullable=True)
    country = db.Column(db.String(128), nullable=False)
    # Add lon/lat, String?

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__=="__main__":
	app.run()
