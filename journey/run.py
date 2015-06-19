#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_init import *
from journey.admin import register_admin

register_admin()
app.run(debug=True)
