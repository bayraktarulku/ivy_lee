#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
run.py
~~~~~~
'''
from app import app

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, threaded=True)