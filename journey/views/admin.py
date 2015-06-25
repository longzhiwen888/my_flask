#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import redirect
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.base import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla.filters import (
    FilterEqual, FilterNotEqual, FilterLike, FilterNotLike,
    FilterGreater, FilterSmaller, FilterEmpty, FilterInList,
    FilterNotInList
)
from sqlalchemy.orm.attributes import QueryableAttribute
from journey.flask_init import app, db, gettext as _, web_root
from journey.utils.user import logout_user, get_current_user
import journey.models


class HomePageView(AdminIndexView):
    def is_accessible(self):
        user = get_current_user()
        return user and user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect('/login/')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin_index.html',  text=_("Hello, world!"))


class LoginOutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login/')


class BaseModelView(ModelView):
    column_display_pk = True
    # column_list = []

    def __init__(self, *args, **kwargs):
        super(BaseModelView, self).__init__(*args, **kwargs)
        self.column_filters = []
        self.column_labels = dict()
        for filter_class in [FilterEqual, FilterNotEqual, FilterLike,
                             FilterNotLike, FilterGreater, FilterSmaller,
                             FilterEmpty, FilterInList, FilterNotInList]:

            for name, attribute in self.model.__dict__.items():
                if isinstance(attribute, QueryableAttribute):
                    label = "%s_%s" % (self.model.__name__, name)
                    self.column_filters.append(
                        filter_class(attribute, _(label)))
                    self.column_labels[name] = _(label)
        self._refresh_cache()

    @classmethod
    def create_sub_class(cls, model_class):
        admin_class_name = model_class.__name__ + 'ModelView'
        exec 'class %s(BaseModelView): pass' % admin_class_name
        sub_class = locals().get(admin_class_name)
        return sub_class


class UserModelView(BaseModelView):
    column_labels = {"token": _("User_token"),
                     "create_time": _("User_create_time"),
                     "is_admin": _("User_is_admin"),
                     "active": _("User_active"),
                     "password": _("User_password"),
                     "user_name": _("User_user_name"),
                     "id": _("User_id")}
    column_list = ["id", "user_name", "active", "is_admin", "create_time"]
    form_columns = ["user_name", "password", "active", "is_admin",
                    "create_time"]
    # form_extra_fields = {
    #     "password": PasswordField(_("User_password"))
    # }
    column_display_pk = True

    def _on_model_change(self, form, model, is_created):
        """
            Compatibility helper.
        """
        if is_created:
            model.token = model.create_token()

        password = model.password.strip()
        if password:
            if not password.startswith('pbkdf2:sha1:'):
                model.password = model.create_password(password)
        try:
            self.on_model_change(form, model, is_created)
        except TypeError:
            self.on_model_change(form, model)


def register_admin():
    inventory_category = _('InventoryManagement')
    admin = Admin(app, name=_("Dashbord"), template_mode='bootstrap3',
                  index_view=HomePageView())
    admin.add_view(UserModelView(
        journey.models.User, db.session, name=_("User"),
        category=inventory_category
    ))

    reg_model_views(admin, inventory_category)

    file_path = os.path.join(web_root, 'static')
    admin.add_view(FileAdmin(file_path, '/static/', name=_('Static Files')))
    admin.add_link(MenuLink(name=_('Login Out'), url='/login_out/'))


def reg_model_views(admin, category):
    for model_name, model_class in journey.models.__dict__.items():
        if model_name == 'User':
            continue
        try:
            if issubclass(model_class, journey.models.BaseModel):
                model_view_class = BaseModelView.create_sub_class(model_class)
                admin.add_view(model_view_class(
                    model_class, db.session, name=_(model_name),
                    category=category
                ))
        except:
            pass
