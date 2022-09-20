from static.repository import add_user, add_order, add_withdrawal
from static.models import User, Order, Withdrawal
from werkzeug.security import generate_password_hash, check_password_hash
from static.session import cookies
from static.utils import luhn_checksum
import json
from flask import jsonify
import random
from static.repository import db


def registration(login, password):
    hashed_password = generate_password_hash(password)
    user = User(login=login, password=hashed_password)
    if add_user(user):
        return '200'
    else:
        return '409'


def authentication(login, password):
    query = User.query.filter_by(login=login).first()
    try:
        log, pas = query.login, query.password
    except:
        return '401'
    if login == log and check_password_hash(pas, password):
        return '200'
    else:
        return '401'


def auth_check(cookie):
    try:
        login = cookies[cookie]
    except KeyError:
        return 'no'
    query = User.query.filter_by(login=login).first()
    if query:
        return 'yes'
    else:
        return 'no'


def order_load(data, login):
    if not luhn_checksum(data):
        return '422'
    else:
        query = Order.query.filter_by(order_id=data).first()
        try:
            if query.user_login == login:
                return '200'
            else:
                return '409'
        except:
            score = score_counter(data, login)
            order = Order(user_login=login, order_id=data, score=score)
            if add_order(order):
                return '202'
            else:
                return '500'


def ords_list(user):
    query = Order.query.filter(Order.date and Order.user_login == user)
    query = list(query)
    if len(query) == 0:
        return '204'
    orders = []
    for i in range(len(query)):
        order = {'number': str(query[i].order_id), 'accrual': str(query[i].score), 'uploaded_at': str(query[i].date)}
        json.dumps(order)
        orders.append(order)
    return jsonify(orders)


def score_counter(order, login):
    score = random.randrange(5000)
    query = User.query.filter_by(login=login).first()
    try:
        query.balance += score
        db.session.commit()
    except:
        db.session.rollback()
        return score


def balance(login):
    query = User.query.filter_by(login=login).first()
    res = {'balance': str(query.balance), 'withdrawn': str(query.withdrawn)}
    return jsonify(res)


def withdraw(order, sum, login):
    if not luhn_checksum(order):
        return '422'
    query = User.query.filter_by(login=login).first()
    if sum <= query.balance:
        withdrawal = Withdrawal(user_login=login, order_id=order, withdrawal=sum)
        add_withdrawal(withdrawal)
        try:
            query.balance -= sum
            query.withdrawn += sum
            db.session.commit()
            return '200'
        except:
            db.session.rollback()
            return '500'
    else:
        return '402'


def withdrawals(login):
    query = Withdrawal.query.filter_by(user_login=login)
    query = list(query)
    withdrawal_list = []
    if len(query) == 0:
        return '204'
    for i in range(len(query)):
        withdrawal = {'order': str(query[i].order_id), 'sum': str(query[i].withdrawal), 'processed_at': str(query[i].date)}
        json.dumps(withdrawal)
        withdrawal_list.append(withdrawal)
        return jsonify(withdrawal_list)








