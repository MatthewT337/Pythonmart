from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from static.config import app

db = SQLAlchemy(app)


def add_user(user):
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False


def add_order(order):
    try:
        db.session.add(order)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def add_withdrawal(withdrawal):
    try:
        db.session.add(withdrawal)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False




