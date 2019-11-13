from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#Test
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:secret@192.111.1.253:3307/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from app import views, models, animalLocatorView

db.create_all()

