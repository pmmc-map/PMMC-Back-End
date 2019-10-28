from app import db

class Question(db.Model):
    qid = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    response = db.relationship('Response', backref='question')

class Response(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, db.ForeignKey('question.qid'), nullable=False)    
    text = db.Column(db.String, nullable=False)