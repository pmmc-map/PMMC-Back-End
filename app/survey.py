from app import db

class Question(db.Model):
    qid = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    #response = db.relationship('Response', backref='question')
    option = db.relationship('Option', backref='question')

class Option(db.Model):
    oid = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, db.ForeignKey('question.qid'), nullable=False)    
    text = db.Column(db.String, nullable=False)
    vr = db.relationship('VisitorResponse', backref='option')

class Response(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, db.ForeignKey('question.qid'), nullable=False)    
    text = db.Column(db.String, nullable=False)

class VisitorResponse(db.Model):
    vr_timestamp = db.Column(db.DateTime, primary_key=True)
    oid = db.Column(db.Integer, db.ForeignKey('option.oid'))
