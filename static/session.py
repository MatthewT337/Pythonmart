import uuid

cookies = {}


def create_cookie(login):
    token = uuid.uuid4()
    cookies[str(token)] = login
    return str(token)
