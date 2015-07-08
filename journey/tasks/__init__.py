#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import Celery
from celery.utils.log import get_task_logger
from journey.flask_init import app as application
logger = get_task_logger(__name__)


def make_celery(app):
    c = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    c.conf.update(app.config)
    TaskBase = c.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    c.Task = ContextTask
    return c


celery = make_celery(application)
from journey.tasks.test import add_together

if __name__ == '__main__':
    add_together.delay()
