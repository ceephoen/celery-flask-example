# -*- coding: utf-8 -*-
"""
project config
"""
import base64
import os


class Configure(object):
    """base config"""

    # 1.1 SECRET_KEY
    SECRET_KEY = base64.b64encode(os.urandom(24)).decode('utf-8')

    # 1.2 SALT
    SALT = base64.b64encode(os.urandom(16)).decode('utf-8')

    # 2 mysql
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:pwd@ip:3306/db_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3 redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379

    # 4 celery
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_TASK_RESULT_EXPIRES = 60  # successful
    CELERYD_MAX_TASKS_PER_CHILD = 50
    CELERYD_CONCURRENCY = 50

    # 5 file limit
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # 6 json
    JSON_AS_ASCII = False

    # 7 TOKEN_EXPIRE
    REFRESH_TOKEN_EXPIRE = 60 * 60 * 24 * 30
    ACCESS_TOKEN_EXPIRE = 60 * 60


class DevelopConfig(Configure):
    """DevelopConfig"""
    DEBUG = True

    ENV = 'development'


class ProduceConfig(Configure):
    """ProduceConfig"""
    DEBUG = False

    ENV = 'production'

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:pwd@ip:3306/db_name'

    # db pool
    SQLALCHEMY_POOL_SIZE = 10

    # pool timeout
    SQLALCHEMY_POOL_TIMEOUT = 20

    # pool recycle
    SQLALCHEMY_POOL_RECYCLE = 60 * 60


config = {
    'develop': DevelopConfig,
    'produce': ProduceConfig
}
