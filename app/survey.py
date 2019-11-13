from app import db

class Question(db.Model):
    qid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    text = db.Column(db.String(128), nullable=False)
    response = db.relationship('Response', backref='Question')
    option = db.relationship('Option', backref='Question')

class Option(db.Model):
    qid = db.Column(db.Integer, db.ForeignKey(Question.qid), primary_key=True, nullable=False)    
    text = db.Column(db.String(128), nullable=False)

class Response(db.Model):
    qid = db.Column(db.Integer, db.ForeignKey(Question.qid), primary_key=True, nullable=False)    
    text = db.Column(db.String(128), nullable=False)