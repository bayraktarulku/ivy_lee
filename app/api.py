from flask import request, Blueprint
from flask_restful import Api, Resource
from app.storage.model import User, Task, DBSession, Token
from schema import Schema, Optional, Use, And, Or, SchemaError
from sqlalchemy.exc import IntegrityError
from app.helpers import generate_token
from time import time
from functools import wraps

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

TOKEN_EXPIRE_TIME = 120

USER_SCHEMA = Schema({
    'username': Use(str),
    'password': Use(str),
    Optional('limit'): int,
})

TASK_SCHEMA = Schema({
    'id': int,
    'description': Use(str),
    'date_time': Use(str),
})

def authenticate(f):
    @wraps
    def wrapped():
        token_data = request.headers.get('X-Token', None)
        session = DBSession()
        token = session.query(Token).filter(Token.token == token_data)
        if not token:
            return {'status': 'error'}
        last_token = session.query(Token).filter(Token.user_id == token.user_id).last()
        if last_token.token != token.token:
            return {'status': 'error'}

        if time() - token.date_time >= TOKEN_EXPIRE_TIME:
            return {'status': 'error'}
        return f()
    return wrapped

class AuthResource(Resource):

    def post(self):
        data = USER_SCHEMA.validate(request.json)
        session = DBSession()
        user = session.query(User).filter(
            User.username == data['username'],
            User.password == data['password']).first()
        if not user:
            return {'status': 'error'}

        token = generate_token(data['username'], data['password'])
        new_token = Token(token=token, date_time=time(), user_id=user.id)
        session.add(new_token)
        session.commit()

        return {'status': 'OK',
                'token': token}


class UserResource(Resource):

    def post(self):
        try:
            data = USER_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'error'}
        session = DBSession()
        user = session.query(User).filter(
            User.username == data['username'],
            User.password == data['password']).first()
        if not user:
            return {'status': 'error'}

        tasks = session.query(Task).filter(Task.user_id == user.id).all()
        return {'status': 'OK',
                'limit': user.limit,
                'tasks': [{'id': t.id,
                           'description': t.description,
                           'date_time': t.date_time, }
                          for t in tasks]}

    def put(self):
        try:
            data = USER_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'error'}

        session = DBSession()
        new_user = User(username=data['username'],
                        password=data['password'],
                        limit=data.get('limit', 6))
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return {'status': 'error'}

        return {'status': 'OK',
                'uid': new_user.id}

    def delete(self):
        try:
            data = USER_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'error'}

        session = DBSession()
        user = session.query(User).filter(
            User.username == data['username'],
            User.password == data['password']).first()
        if not user:
            return {'status': 'error'}

        session.delete(user)
        session.commit()

        return {'status': 'OK'}


class TaskResource(Resource):

    def get():

        return {}

    def post():
        return {}

    def put():
        return {}

api.add_resource(UserResource, '/api/user')
api.add_resource(AuthResource, '/api/auth')
api.add_resource(TaskResource, '/api/task')
