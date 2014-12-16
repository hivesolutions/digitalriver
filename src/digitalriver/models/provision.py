#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import base

class Provision(base.DRBase):

    id = appier.field(
        index = True,
        immutable = True,
        default = True
    )
