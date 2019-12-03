from app import app, db
from app.survey import Question, Option
from app.models import AnimalLocations, CityImages, Count
from questionsParser import addQuestions
from optionsParser import addOptions
from animalsParser import addAnimals

def verboseAddQuestions():
    print("\n----------ADDING QUESTIONS----------\nEmptying current Question table...")
    try:
        Question.__table__.drop(db.engine)
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
        Option.__table__.drop(db.engine)
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
        AnimalLocations.__table__.drop(db.engine)
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
        CityImages.__table__.drop(db.engine)
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
        Count.__table__.drop(db.engine)
    except:
        pass
    db.create_all()
    db.session.add(Count(name='num_rescues', total=0))
    db.session.commit()

    print(Count.query.all())

if __name__=="__main__":
    verboseAddQuestions()
    verboseAddOptions()
    verboseAddAnimals()
    addDefaultImage()
    addCount()
