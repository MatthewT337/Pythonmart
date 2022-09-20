from flask import Blueprint, request
from static.service import registration, authentication, auth_check, order_load, ords_list, balance, withdraw, withdrawals
from static.config import app
from static.session import cookies, create_cookie

COOKIE_EXPIRE_TIME = 3000

main = Blueprint('main', __name__)


@main.route("/api/user/register", methods=['POST'])
def reg_route():
    try:
        if request.method != 'POST' or request.headers.get('Content-Type') != 'application/json':
            return '400'
        try:
            data = request.get_json()
            login, password = data['login'].upper(), data['password']
        except:
            return '400'
        if registration(login, password) == '200':
            token = create_cookie(login)
            res = app.make_response('200')
            res.set_cookie('pythonmart_session', token, COOKIE_EXPIRE_TIME)
            return res
        else:
            return '409'
    except:
        return '500'


@main.route("/api/user/login", methods=['POST'])
def log_route():
    try:
        if request.method != 'POST' or request.headers.get('Content-Type') != 'application/json':
            return '400'
        try:
            data = request.get_json()
            login, password = data['login'].upper(), data['password']
        except:
            return '400'
        if authentication(login, password) == '200':
            token = create_cookie(login)
            res = app.make_response('200')
            res.set_cookie('pythonmart_session', str(token), COOKIE_EXPIRE_TIME)
            return res
        else:
            return '401'
    except:
        return '500'


@main.route("/api/user/orders", methods=['POST', 'GET'])
def ord_route():
    try:
        cookie = request.cookies.get('pythonmart_session')
        if auth_check(cookie) != 'yes':
            return '401'
        if request.method == 'POST' and request.headers.get('Content-Type') == 'text/plain':
            login = cookies[cookie]
            try:
                data = request.get_data(as_text=True)
                data = data.replace('\r', '')
                data = data.replace('\n', '')
                return order_load(data, login)
            except:
                return '400'
        elif request.method == 'GET':
            login = cookies[cookie]
            res = ords_list(login)
            return res
        else:
            return '400'
    except:
        return '500'


@main.route("/api/user/balance", methods=['GET'])
def bal():
    cookie = request.cookies.get('pythonmart_session')
    if auth_check(cookie) != 'yes':
        return '401'
    else:
        if request.method == 'GET':
            login = cookies[cookie]
            return balance(login)
        else:
            return '400'


@main.route("/api/user/withdraw", methods=['POST'])
def withdrawal():
    cookie = request.cookies.get('pythonmart_session')
    if auth_check(cookie) != 'yes':
        return '401'
    login = cookies[cookie]
    if request.method != 'POST' or request.headers.get('Content-Type') != 'application/json':
        return '400'
    try:
        data = request.get_json()
        order = data['order']
        sum = data['sum']
        return withdraw(order, sum, login)
    except:
        return '400'


@main.route('/api/user/withdrawals', methods=['GET'])
def withdrawals_list():
    if request.method != 'GET':
        return '400'
    cookie = request.cookies.get('pythonmart_session')
    if auth_check(cookie) != 'yes':
        return '401'
    if request.method != 'GET':
        return '400'
    login = cookies[cookie]
    return withdrawals(login)
