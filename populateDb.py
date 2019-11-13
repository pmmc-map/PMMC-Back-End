from app import app, db
from app.survey import Question, Option
from app.models import AnimalLocations
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

if __name__=="__main__":
    verboseAddQuestions()
    verboseAddOptions()
    verboseAddAnimals()
    #addQuestions()
    #addOptions()
    #addAnimals()
