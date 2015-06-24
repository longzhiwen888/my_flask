#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseConfig(object):
    APP_NAME = "my_flask"
    DEBUG = False
    TESTING = False
    SITE_URL = '/'
    PROPAGATE_EXCEPTIONS = True

    #: session
    SESSION_COOKIE_NAME = 'journey_session_id'

    #: account
    SECRET_KEY = 'MY_FLASK_JOURNEY_SECRET_KEY'
    PASSWORD_SECRET = 'PASSWORD_SECRET_!)!%'

    LOGGERS = {
        'my_flask_journey': {
            'level': 'INFO',
        },
    }
