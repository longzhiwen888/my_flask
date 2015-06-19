#!/usr/bin/env python
# -*- coding: utf-8 -*-


import functools

from flask import (
    url_for, redirect,
    request, session,
    current_app
)


class RequireLogin(object):

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            url = url_for('journey.login')
            if '?' not in url:
                url += '?next=' + request.url
            login_token = session.get('login_token', '')
            if not login_token:
                return redirect(url)
            else:
                c_config = current_app.config
                username = c_config.get('USERNAME')
                user_password = c_config.get('USER_PASSWORD')
                try:
                    _username, _user_password = login_token.split('|')
                except:
                    return redirect(url)
                else:
                    if _username != username or _user_password != user_password:
                        return redirect(url)
            return method(*args, **kwargs)

        return wrapper


require_login = RequireLogin()
