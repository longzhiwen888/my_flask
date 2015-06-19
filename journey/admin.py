#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import redirect, request, url_for, g
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask_init import admin, db, gettext as _
from models import User


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html',  text=_("Hello, world!"))

    # def is_accessible(self):
    #     return get_current_user()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))


class UserModelView(ModelView):
    column_labels = {"id": _("user_model_id"),
                     "user_name": _("user_model_name"),
                     "password": _("user_model_password"),
                     "active": _("user_model_active"),
                     "is_admin": _("user_model_is_admin"),
                     "create_time": _("user_model_create_time")
                     }

test_category = _('Test')
admin.add_view(MyView(name='Hello1', endpoint='test1', category=test_category))
admin.add_view(MyView(name='Hello2', endpoint='test2', category=test_category))
admin.add_view(MyView(name='Hello3', endpoint='test3', category=test_category))

admin.add_view(UserModelView(User, db.session, name=_("User")))

path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name=_('Static Files')))
