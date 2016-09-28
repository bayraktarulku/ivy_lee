from flask import Blueprint, request
from flask_restful import Api, Resource
from app.storage.model import User, Task, DBSession
from schema import Schema, Optional, Use, And, Or, SchemaError
from sqlalchemy.exc import IntegrityError


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

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


api.add_resource(UserResource, '/api/user')
