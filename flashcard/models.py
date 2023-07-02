from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    front = db.Column(db.String(100),nullable = False)
    back = db.Column(db.String(100),nullable = False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.d_id'))


class Deck(db.Model):
    d_id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50),nullable = False)
    title = db.Column(db.String(20))
    Score = db.Column(db.Integer,default = 0)
    last_rev = db.Column(db.DateTime(timezone = True),default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    note = db.relationship("Note",backref = "Deck")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    deck = db.relationship('Deck',backref = "User")
