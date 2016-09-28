#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask
from app.api import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp)


@app.route('/')
def index():
    return 'Naber'