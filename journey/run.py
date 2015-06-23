#!/usr/bin/env python
# -*- coding: utf-8 -*-

from journey.flask_init import app
from journey.views.admin import register_admin

register_admin()
app.run(debug=False)

