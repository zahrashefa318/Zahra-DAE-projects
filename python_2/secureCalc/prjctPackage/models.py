from .dbExtension import db
class userInfo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    lastname=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), nullable=False, unique=True)
    password=db.Column(db.String(100), nullable=False)