#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .local import LocalConfig
from .prod import ProdConfig

CONFIG_MAPPING = {
    'local': LocalConfig,
    'prod': ProdConfig,
}
