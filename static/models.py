from static.repository import db
import datetime


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    balance = db.Column(db.INTEGER, default=0)
    withdrawn = db.Column(db.INTEGER, default=0)


class Order(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    order_id = db.Column(db.String(100), nullable=False, unique=True)
    user_login = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    score = db.Column(db.INTEGER)


class Withdrawal(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    order_id = db.Column(db.String(100), nullable=False, unique=True)
    user_login = db.Column(db.String(100), nullable=False)
    withdrawal = db.Column(db.INTEGER)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

