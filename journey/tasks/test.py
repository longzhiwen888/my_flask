# -*- coding: utf8 -*-

from celery import task


@task(bind=True, max_retries=5, default_retry_delay=1 * 6)
def add_together(self, a, b):
    try:
        print a
        print b
        return a + b
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)
