#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ._base import BaseConfig


all = ['ProdConfig']


class ProdConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = ""
    RUN_ENV = 'prod'
    LOG_FLODER = ''

    def __init__(self):
        self.LOGGERS['my_flask_journey']['level'] = 'INFO'
