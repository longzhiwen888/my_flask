#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, session

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