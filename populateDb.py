from app import app, db
from app.survey import Question, Option
from questionsParser import addQuestions
from optionsParser import addOptions

if __name__=="__main__":
    print("Emptying current Question table...\n")
    Question.__table__.drop(db.engine)
    db.create_all()
    addQuestions()
    for question in Question.query.all():
        print(str(question.qid) + " " + question.text)

    print("\nEmptying current Option table...\n")
    Option.__table__.drop(db.engine)
    db.create_all()
    addOptions()
    print("Showing current d")
    for option in Option.query.all():
        print("Option oid: " + str(option.oid) + "\n\tText: " + option.text + "\n\tAssociated with qid: " + str(option.qid) + "\n")
