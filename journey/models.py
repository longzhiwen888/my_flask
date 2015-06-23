#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery as _BaseQuery
from werkzeug import security
from rhct.utils import FancyDict

db = SQLAlchemy()


class BaseQuery(_BaseQuery):

    def filter_in(self, model, values):
        values = set(values)
        if len(values) == 0:
            return {}
        if len(values) == 1:
            ident = values.pop()
            rv = self.get(ident)
            if not rv:
                return {}
            return {ident: rv}
        items = self.filter(model.in_(values))
        dct = {}
        for item in items:
            dct[getattr(item, model.key)] = item
        return dct

    def as_list(self):
        return list(self)


db.Model.query_class = BaseQuery


class SessionMixin(object):

    def save(self, **kwargs):
        try:
            #针对于可能存在的批量入库问题，这里增加判断是否传递了commit参数
            commit = kwargs.get('commit', True)
            db.session.add(self)
            if commit:
                db.session.commit()
            return self
        except Exception, e:
            db.session.rollback()

    def delete(self, **kwargs):
        try:
            db.session.delete(self)
            db.session.commit()
            return self
        except Exception, e:
            db.session.rollback()


class DefaultModel(db.Model):
    __abstract__ = True
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}


class BaseModel(DefaultModel, SessionMixin):
    __abstract__ = True

    dict_default_columns = []

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self, columns=None):
        dct = FancyDict()
        if columns is None:
            columns = self.dict_default_columns
        for col in columns:
            if col == 'id' or col in getattr(self, 'encrypt_attrs', []):
                value = getattr(self, col)
                #value = getattr(self, col)
            else:
                value = getattr(self, col)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(value, BaseModel):
                value = value.to_dict()
            dct[col] = value
        return dct


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    create_time = db.Column(db.DATETIME, default=datetime.now())
    token = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.token = self.create_token()

    def create_token(self, length=16):
        return security.gen_salt(length)

    def __unicode__(self):
        return self.user_name

    def is_active(self):
        return self.active


class Inventory(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_no = db.Column(db.String(120))
    goods_no = db.Column(db.String(120))
    goods_num = db.Column(db.Integer)


class Warehouse(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    admin_id = db.Column(db.Integer)


class Goods(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    goods_no = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    measurement_unit = db.Column(db.String(250), nullable=False)


class Supplier(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    contact_name = db.Column(db.String(250), nullable=False)
    contact_phone = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(250), nullable=False)


class Manager(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    contact_phone = db.Column(db.String(250), nullable=False)


class OutboundOrder(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(250), nullable=False)
    goods_no = db.Column(db.String(250), nullable=False)
    goods_num = db.Column(db.Integer)
    warehouse_no = db.Column(db.String(250), nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now())


class InboundOrder(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(250), nullable=False)
    goods_no = db.Column(db.String(250), nullable=False)
    goods_num = db.Column(db.Integer)
    warehouse_no = db.Column(db.String(250), nullable=False)
    goods_price = db.Column(db.Float)
    supplier_no = db.Column(db.String(250), nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now())
