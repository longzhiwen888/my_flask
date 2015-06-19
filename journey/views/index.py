#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, request, current_app, session,
    redirect, jsonify
)

from flask.ext.babelex import gettext as _
from journey.utils.user import (
    login_user, logout_user, reg, validate_user
)
from journey.views.permisson import require_login

bp = Blueprint('journey', __name__)


@bp.route('/')
def hello():
    day = _("Saturday")
    return render_template('web_index.html', day=day)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next', '/admin/')
    if request.method == 'POST':
        account = request.form.get('account', '')
        password = request.form.get('password', '')
        user = validate_user(account, password)
        if user:
            login_user(user, permanent=True)
            return redirect(next_url)
        else:
            return jsonify(dict(a=2))
    else:
        return render_template('login.html')


@bp.route('/login_out/')
def login_out():
    logout_user()
    return redirect('/login/')


@bp.route('/user_reg/')
def user_reg():
    if 'login_token' in session:
        del session['login_token']
    return redirect('/login/')