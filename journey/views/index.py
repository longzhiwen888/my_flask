#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, request, current_app, session,
    redirect, jsonify
)

from flask.ext.babelex import gettext as _
from journey.views.permisson import require_login

bp = Blueprint('journey', __name__)


@bp.route('/')
def hello():
    day = _("Saturday")
    return render_template('web_index.html', day=day)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next', '/')
    if request.method == 'POST':
        account = request.form.get('account', '')
        password = request.form.get('password', '')
        c_config = current_app.config
        username = c_config.get('USERNAME').strip()
        user_password = str(c_config.get('USER_PASSWORD')).strip()
        if account == username and password == user_password:
            print 'success'
            token = '%s|%s' % (username, user_password)
            session['login_token'] = token
            session.permanent = True
            return redirect(next_url)
        else:
            return jsonify(dict(a=2))
    else:
        return render_template('login.html')


@bp.route('/login_out/')
def login_out():
    if 'login_token' in session:
        del session['login_token']
    return redirect('/login/')