#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from app.api import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task')
def task():
    return render_template('task.html')

@app.route('/login')
def login():
    return render_template('login.html')