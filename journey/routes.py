#!/usr/bin/env python
# -*- coding: utf-8 -*-


def register_routes(app):
    from .views import index
    app.register_blueprint(index.bp)
