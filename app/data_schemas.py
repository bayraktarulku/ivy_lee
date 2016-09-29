from schema import Schema, Optional, Use, And, Or, SchemaError


USER_SCHEMA = Schema({
    'username': Use(str),
    'password': Use(str),
    Optional('limit'): int,
})

TASK_SCHEMA = Schema({
    'description': Use(str),
    'date_time': int,
})

TASK_CHECK_SCHEMA = Schema({
    'id': int,
    'checked': bool,
})

TASK_DELETE_SCHEMA = Schema({
    'id': int,
})