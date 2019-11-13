from app import app, db
from app.survey import Question

def addQuestions():
    question_file = open("questions.txt", "r")
    for question in question_file:
        question = question.strip("\n")
        question = Question(text=question,active=True)
        db.session.add(question)
        db.session.commit()
    question_file.close()