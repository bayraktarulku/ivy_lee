from flask import request, Blueprint
from flask_restful import Api, Resource
from app.storage.model import User, Task, DBSession, Token
from sqlalchemy.exc import IntegrityError
from app.helpers import generate_token
from app.data_schemas import (USER_SCHEMA, TASK_SCHEMA,
                              TASK_CHECK_SCHEMA, TASK_DELETE_SCHEMA)
from time import time
from sqlalchemy import desc
from schema import SchemaError

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

TOKEN_EXPIRE_TIME = 36000


def get_user_from_token():
    token_data = request.headers.get('X-Token', None)
    session = DBSession()
    token = session.query(Token).filter(Token.token == token_data).first()

    if not token:
        return {'status': 'error',
                'message': 'NOT_AUTHORIZED'}
    last_token = session.query(Token).filter(
        Token.user_id == token.user_id).order_by(desc(Token.date_time)).first()

    if last_token.token != token.token:
        return {'status': 'error',
                'message': 'TOKEN_REVOKED'}

    if time() - token.date_time >= TOKEN_EXPIRE_TIME:
        return {'status': 'error',
                'message': 'TOKEN_EXPIRED'}

    return {'status': 'OK',
            'user_id': token.user_id}


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
            return {'status': 'error',
                    'message': 'Missing or incorrect parameters'}

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
                           'date_time': t.date_time,
                           'checked': t.checked, }
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

    def post(self):
        try:
            data = TASK_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'error',
                    'message': 'Missing or incorrect parameters.'}
        response = get_user_from_token()

        if response['status'] != 'OK':
            return response

        session = DBSession()
        new_task = Task(description=data['description'],
                        date_time=data['date_time'],
                        user_id=response['user_id'])

        session.add(new_task)
        session.commit()

        return {'status': 'OK',
                'id': new_task.id,
                'description': new_task.description,
                'date_time': new_task.date_time, }

    def put(self):
        try:
            data = TASK_CHECK_SCHEMA.validate(request.json)
        except:
            return {'status': 'error',
                    'message': 'Missing or incorrect parameters.'}
        response = get_user_from_token()
        if response['status'] != 'OK':
            return response

        session = DBSession()
        tasks_query = session.query(Task).filter(Task.id == data['id'])
        task = tasks_query.first()
        if not task:
            return {'status': 'error',
                    'message': 'No such task.'}

        elif task.user_id != response['user_id']:
            return {'status': 'error',
                    'message': 'It\'s not that user\'s task.'}
        tasks_query.update({'checked': data['checked']})
        session.commit()

        return {'status': 'OK',
                'checked': data['checked']}

    def delete(self):
        response = get_user_from_token()
        if response['status'] != 'OK':
            return response

        try:
            data = TASK_DELETE_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'error',
                    'message': 'Missing or incorrect parameters.'}
        session = DBSession()
        task = session.query(Task).filter(
            Task.id == data['id'], Task.user_id == response['user_id']).first()
        if not task:
            return {'status': 'error',
                    'message': 'Task with such id does not exists.'}
        session.delete(task)
        session.commit()
        return {'status': 'OK'}

api.add_resource(UserResource, '/api/user')
api.add_resource(AuthResource, '/api/auth')
api.add_resource(TaskResource, '/api/task')
