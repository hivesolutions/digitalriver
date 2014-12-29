#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import base

class Feature(base.DRBase):

    url = appier.field(
        index = True,
        default = True
    )

    name = appier.field(
        index = True
    )
