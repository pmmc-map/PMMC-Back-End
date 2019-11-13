from app import app, db
from app.survey import Option

def addOptions():
    option_file = open("options.txt", "r")
    for option in option_file:
        option = option.strip("\n").split(",", 1)
        option_qid = option[0]
        option_text = option[1]
        option = Option(text=option_text,qid=option_qid)
        db.session.add(option)
        db.session.commit()
    option_file.close()