#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ._base import BaseConfig


all = ['LocalConfig']


class LocalConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://dev:123456@127.0.0.1:3306/test_flask"
    SQLALCHEMY_BINDS = {
        'huati': 'mysql+pymysql://dev:123456@127.0.0.1:3306/test_flask'
    }
    RUN_ENV = 'local'
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    LOG_FLODER = '/Users/chenhailong/Downloads/log/'

    def __init__(self):
        self.LOGGERS['my_flask_journey']['level'] = 'DEBUG'
