#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import redirect, request, url_for
from flask_admin.consts import ICON_TYPE_FONT_AWESOME, ICON_TYPE_GLYPH
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.base import MenuLink, MenuView
from flask_admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla.filters import (
    FilterEqual, FilterNotEqual, FilterLike, FilterNotLike,
    FilterGreater, FilterSmaller
)
from sqlalchemy.orm.attributes import QueryableAttribute
from wtforms import PasswordField
from journey.flask_init import app, db, gettext as _, web_root
from journey.utils.user import logout_user, get_current_user
import journey.models


class HomePageView(AdminIndexView):
    def is_accessible(self):
        user = get_current_user()
        return user and user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            # return redirect(url_for('login', next=request.url))
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
    # def is_accessible(self):
    #     return get_current_user()
    column_filters = []

    def __init__(self, *args, **kwargs):
        super(BaseModelView, self).__init__(*args, **kwargs)
        column_filters = []
        for filter_class in [FilterEqual, FilterNotEqual, FilterLike,
                             FilterNotLike, FilterGreater, FilterSmaller]:

            for name, attribute in self.model.__dict__.items():
                if isinstance(attribute, QueryableAttribute):
                    label = "%s_%s" % (self.model.__name__, name)
                    column_filters.append(filter_class(attribute, _(label)))
        self.column_filters = column_filters
        self._refresh_cache()


class OutboundOrderModelView(BaseModelView):
    column_labels = {"order_no": _("OutboundOrder_order_no"),
                     "goods_num": _("OutboundOrder_goods_num"),
                     "id": _("OutboundOrder_id"),
                     "create_time": _("OutboundOrder_create_time"),
                     "goods_no": _("OutboundOrder_goods_no"),
                     "warehouse_no": _("OutboundOrder_warehouse_no")}
    column_searchable_list = ["order_no", "goods_num", "create_time"]


class WarehouseModelView(BaseModelView):
    column_labels = {"address": _("Warehouse_address"),
                     "id": _("Warehouse_id"), 'name': _("Warehouse_name"),
                     "admin_id": _("Warehouse_admin_id")}


class GoodsModelView(BaseModelView):
    column_labels = {"category": _("Goods_category"),
                     "measurement_unit": _("Goods_measurement_unit"),
                     "goods_no": _("Goods_goods_no"),
                     "id": _("Goods_id"),
                     "name": _("Goods_name")}


class InventoryModelView(BaseModelView):
    column_labels = {"goods_no": _("Inventory_goods_no"),
                     "id": _("Inventory_id"),
                     "goods_num": _("Inventory_goods_num"),
                     "warehouse_no": _("Inventory_warehouse_no")}


class InboundOrderModelView(BaseModelView):
    column_labels = {"order_no": _("InboundOrder_order_no"),
                     "supplier_no": _("InboundOrder_supplier_no"),
                     "goods_num": _("InboundOrder_goods_num"),
                     "warehouse_no": _("InboundOrder_warehouse_no"),
                     "create_time": _("InboundOrder_create_time"),
                     "goods_price": _("InboundOrder_goods_price"),
                     "goods_no": _("InboundOrder_goods_no"),
                     "id": _("InboundOrder_id")}


class SupplierModelView(BaseModelView):
    column_labels = {"contact_name": _("Supplier_contact_name"),
                     "contact_phone": _("Supplier_contact_phone"),
                     "id": _("Supplier_id"),
                     "name": _("Supplier_name"),
                     "address": _("Supplier_address")}


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


class ManagerModelView(BaseModelView):
    column_labels = {"contact_phone": _("Manager_contact_phone"),
                     "name": _("Manager_name"),
                     "id": _("Manager_id")}


def register_admin():
    test_category = _('Test')
    inventory_category = _('InventoryManagement')
    admin = Admin(app, name=_("Dashbord"), template_mode='bootstrap3',
                  index_view=HomePageView())
    admin.add_view(MyView(name='Hello1', endpoint='test1',
                          category=test_category))
    admin.add_view(MyView(name='Hello2', endpoint='test2',
                          category=test_category))
    admin.add_view(MyView(name='Hello3', endpoint='test3',
                          category=test_category))

    admin.add_view(OutboundOrderModelView(
        journey.models.OutboundOrder, db.session, name=_("OutboundOrder"),
        category=inventory_category
    ))
    admin.add_view(WarehouseModelView(
        journey.models.Warehouse, db.session, name=_("Warehouse"),
        category=inventory_category
    ))
    admin.add_view(GoodsModelView(
        journey.models.Goods, db.session, name=_("Goods"),
        category=inventory_category
    ))
    admin.add_view(InventoryModelView(
        journey.models.Inventory, db.session, name=_("Inventory"),
        category=inventory_category
    ))
    admin.add_view(InboundOrderModelView(
        journey.models.InboundOrder, db.session, name=_("InboundOrder"),
        category=inventory_category
    ))
    admin.add_view(SupplierModelView(
        journey.models.Supplier, db.session, name=_("Supplier"),
        category=inventory_category
    ))
    admin.add_view(UserModelView(
        journey.models.User, db.session, name=_("User"),
        category=inventory_category
    ))
    admin.add_view(ManagerModelView(
        journey.models.Manager, db.session, name=_("Manager"),
        category=inventory_category
    ))

    print_model_views()
    path = os.path.join(web_root, 'static')
    admin.add_view(FileAdmin(path, '/static/', name=_('Static Files')))
    admin.add_view(LoginOutView(name=_('Login Out'),
                                menu_icon_type=ICON_TYPE_FONT_AWESOME,
                                menu_icon_value='icon-glass'))
    admin.add_view(LoginOutView(name=_('Login Out'),
                                menu_icon_type=ICON_TYPE_GLYPH,
                                menu_icon_value='icon-glass',
                                endpoint='login_out2'))

    admin.add_link(MenuLink(name=_('Login Out'), url='/login_out/'))


def print_model_views():
    content_list = []
    for model_name, model_class in journey.models.__dict__.items():
        try:
            if issubclass(model_class, journey.models.BaseModel):
                view_name = '{0}ModelView'.format(model_name)
                template = '''class {0}(BaseModelView):'''
                print template.format(view_name)
                print '    column_labels = {'
                for name, attribute in model_class.__dict__.items():
                    if isinstance(attribute, QueryableAttribute):
                        label = "%s_%s" % (model_name, name)
                        print '        "{0}": _("{1}")'.format(name, label)
                print '}\r\n\r\n'
                cmd = ('admin.add_view({0}(journey.models.{1}, '
                       'db.session, name=_("{2}")))').format(
                    view_name, model_name, model_name)
                content_list.append(cmd)
        except:
            pass
    print '\r\n'.join(content_list)

