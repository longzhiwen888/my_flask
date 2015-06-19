#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from journey.flask_init import app
from journey.models import db

manager = Manager(app)

if __name__ == '__main__':
    migrate = Migrate(manager.app, db)
    manager.add_command('db', MigrateCommand)

    manager.run()
