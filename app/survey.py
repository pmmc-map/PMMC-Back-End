from app import db

class Question(db.Model):
	# Primary key will auto increment
    qid = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    response = db.relationship('Response', backref='question')

class Response(db.Model):
    # I have no idea what the fields will be
    rid = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, db.ForeignKey('question.qid'), nullable=False)    
    text = db.Column(db.String, nullable=False)