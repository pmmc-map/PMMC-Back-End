from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from app import views, models, animalLocatorView

db.create_all()

try:
    db.session.add(AdminLogin(googleID='109305513013129297314',name='Map Account', email='mapanalyticspmmc@gmail.com'))
    db.session.commit()

    db.session.add(AdminLogin(googleID='113684858932238811485',name='Pacific Marine Mammal Center', email='pacificmmceducation@gmail.com'))
    db.session.commit()

    # db.session.add(AdminLogin(googleID='109305513013129297314',name='Map Account', email='educationpmmc@gmail.com'))
    db.session.commit()
    
except:
    pass