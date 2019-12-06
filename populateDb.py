from app import app, db
from app.survey import Question, Option
from app.models import AnimalLocations, CityImages, Count, AdminLogin
from questionsParser import addQuestions
from optionsParser import addOptions
from animalsParser import addAnimals

def verboseAddQuestions():
    print("\n----------ADDING QUESTIONS----------\nEmptying current Question table...")
    try:
        #Question.__table__.drop(db.engine)
        db.session.query(Question).delete()
        db.session.commit()
    except:
        pass
    db.create_all()
    addQuestions()
    print("Showing updated Question database table")
    for question in Question.query.all():
        print("Question qid: " + str(question.qid) + "\n\tText:" + question.text)

def verboseAddOptions():
    print("\n----------ADDING OPTIONS----------\nEmptying current Option table...")
    try:
        db.session.query(Option).delete()
        db.session.commit()    
    except:
        pass
    db.create_all()
    addOptions()
    print("Showing updated Option database table")
    for option in Option.query.all():
        print("Option oid: " + str(option.oid) + "\n\tText: " + option.text + "\n\tAssociated with qid: " + str(option.qid))

def verboseAddAnimals():
    print("\n----------ADDING ANIMALS----------\nEmptying current AnimalLocation table...\n")
    try:
        db.session.query(AnimalLocations).delete()
        db.session.commit()    
    except:
        pass

    db.create_all()
    addAnimals()
    print("Showing updated Option database table")
    for animal in AnimalLocations.query.all():
        print("Animal(s): " + animal.animal_name + "\n\tLocation: " + str(animal.location_name) + "\n\t...")

def addDefaultImage():
    print("\n----------ADDING DEFAULT IMAGE TO DATABASE----\nEmptying current CityImages table...\n")
    try:
        db.session.query(CityImages).delete()
        db.session.commit()          
    except:
        pass

    db.create_all()
    f = open("static/default_city.jpg", 'rb')
    image_data = f.read()
    db.session.add(CityImages(query="default_city", image=image_data))
    db.session.commit()

    print(db.session.query(CityImages).all())

def addCount():
    print("\n----------ADDING 0 'num_rescues' COUNT TO DATABASE----\nEmptying current Count table...\n")
    try:
        db.session.query(Count).delete()
        db.session.commit()            
    except:
        pass
    db.create_all()
    db.session.add(Count(name='num_rescues', total=0))
    db.session.commit()

    print(Count.query.all())

def addAdmin():
    print("\n----------ADDING ADMIN LOGIN INFO TO DB----------\nEmptying current AdminLogin table...\n")
    try:
        db.session.query(AdminLogin).delete()
        db.session.commit()                   
    except:
        pass
    db.create_all()

    db.session.add(AdminLogin(googleID='109305513013129297314',name='Map Account', email='mapanalyticspmmc@gmail.com'))
    db.session.commit()

    db.session.add(AdminLogin(googleID='113684858932238811485',name='Pacific Marine Mammal Center', email='pacificmmceducation@gmail.com'))
    db.session.commit()

    # db.session.add(AdminLogin(googleID='109305513013129297314',name='Map Account', email='educationpmmc@gmail.com'))
    db.session.commit()


if __name__=="__main__":
    verboseAddQuestions()
    verboseAddOptions()
    verboseAddAnimals()
    addDefaultImage()
    addCount()
    addAdmin()
