# -*- coding: utf-8 -*-
"""
initial flask app
"""
# to solve ImportError:No module named 'MySQLdb'
import pymysql

pymysql.install_as_MySQLdb()

import redis
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from configs import config
from flask_cors import CORS


# 1 mysql_db
db = SQLAlchemy()  # mysql_db
redis_db = redis.StrictRedis()


def create_app(opt):
    """
    Factory mode
    :config opt:
    :return: app
    """
    # 1 init app
    app = Flask(__name__)

    # 2 config
    app.config.from_object(config[opt])

    # 3 mysql
    db.init_app(app)

    # 4 CORS
    CORS(app, resources=r'/*')

    # 6 redis
    global redis_db
    redis_db = redis.StrictRedis(host=config[opt].REDIS_HOST, port=config[opt].REDIS_PORT)

    return app
