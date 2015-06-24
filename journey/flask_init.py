#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
from flask import Flask, g, request, url_for
from flask.ext.babelex import Babel, Domain
from sqlalchemy.exc import InternalError
from babel import support
from journey.configs import CONFIG_MAPPING
from journey.models import db

__all__ = ['app', 'db']


def gettext(string, **variables):
    t = my_domain.cache.get(locale)
    return t.ugettext(string) % variables


class MyAPP(Flask):

    def register_app_config(self, config_str):
        c = CONFIG_MAPPING.get(config_str)
        self.config.from_object(c())
        self.config.from_object(c())

    def register_app_database(self):
        db.init_app(self)
        db.app = self

    def register_app_routes(self):
        from journey.routes import register_routes
        register_routes(self)

    def register_hooks(self):

        @self.before_request
        def load_current_user():
            g.user = None

    def register_error_handlers(self):

        def sqlalchemy_internalerror_handler(error):
            db.session.remove()
            raise error

        self.register_error_handler(InternalError,
                                    sqlalchemy_internalerror_handler)

    def register_resources(self):
        app = self
        if not hasattr(app, '_static_hash'):
            app._static_hash = {}

        def static_file(filename):
            c = app.config
            prefix = c.get('SITE_STATIC_PREFIX', '/static/')
            if filename in app._static_hash:
                return app._static_hash[filename]
            try:
                with open(os.path.join(app.static_folder, filename), 'r') as f:
                    content = f.read()
                    hsh = hashlib.md5(content).hexdigest()
                value = '%s%s?v=%s' % (prefix, filename, hsh[:5])
            except:
                value = '%s%s' % (prefix, filename)
            app._static_hash[filename] = value
            return value

        def url_for_page(page):
            args = dict(request.args.copy())
            args['page'] = page
            args.update(request.view_args)
            return url_for(request.endpoint, **args)

        def url_for_args(**kwargs):
            args = request.args.copy()
            for k, v in kwargs.iteritems():
                args[k] = v
            return url_for(request.endpoint, **args)

        @app.context_processor
        def register_context():
            return dict(
                static_file=static_file,
                url_for_args=url_for_args,
                getattr=getattr,
            )

        app.jinja_env.globals['url_for_page'] = url_for_page

    def init_loggers(self):
        pass

config = os.environ.get('RUN_ENV', '')
if not config:
    config = 'local'
if config not in CONFIG_MAPPING:
    raise Exception("CONFIG ERROR")

app = MyAPP(__name__)
app.register_app_config(config)
app.init_loggers()
app.register_app_database()
app.register_app_routes()
app.register_hooks()
app.register_resources()
app.register_error_handlers()

_ = gettext

locale = 'zh_Hans_CN'
app.config['BABEL_DEFAULT_LOCALE'] = locale
my_domain = Domain()
babel = Babel(app, default_domain=my_domain)
web_root = os.path.dirname(__file__)

translations_dir_name = os.path.join(web_root, 'translations')
translations = support.Translations.load(translations_dir_name, locale)
my_domain.cache[str(locale)] = translations
