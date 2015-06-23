#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from flask import session

from journey.models import User


SESSION_USER_ID = 'session_user_id'  # session 中保存的用户 uid key
SESSION_USER_TOKEN = 'session_user_token'  # session 中保存的用户 token


def get_current_user():
    if SESSION_USER_ID in session and SESSION_USER_TOKEN in session:
        user = User.query.get(session[SESSION_USER_ID])
        if not user.is_active:
            logout_user()
            return None
        if user and user.token == session[SESSION_USER_TOKEN]:
            return user
    return None


def logout_user():
    if SESSION_USER_ID not in session:
        return
    session.pop(SESSION_USER_ID)
    session.pop(SESSION_USER_TOKEN)
    session.clear()


def login_user(user, permanent=False):
    if not user:
        return None
    session[SESSION_USER_ID] = user.id
    session[SESSION_USER_TOKEN] = user.token
    if permanent:
        session.permanent = True
    return user


def get_user(user_name):
    return User.query.filter(User.user_name == user_name).first()


def get_encrypted_password(password):
    return hashlib.new("md5", password).hexdigest().lower()[:-2]


def validate_user(user_name, password):
    print user_name, password
    user = get_user(user_name)
    print user.user_name
    print get_encrypted_password(password)
    print user.password
    valid = user and get_encrypted_password(password) == user.password

    return user if valid else None


def reg(user_name, password, active=True, is_admin=False):
    password = get_encrypted_password(password)
    new_user = User(user_name=user_name, password=password, active=active)
    new_user.is_admin = is_admin
    new_user.save()
    return new_user
