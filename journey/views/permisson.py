#!/usr/bin/env python
# -*- coding: utf-8 -*-


import functools

from flask import (
    url_for, redirect,
    request, session,
    current_app
)
from journey.utils.user import get_current_user


class RequireLogin(object):

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            url = url_for('journey.login')
            if '?' not in url:
                url += '?next=' + request.url

            user = get_current_user()
            if not user:
                return redirect(url)
            return method(*args, **kwargs)

        return wrapper


require_login = RequireLogin()
