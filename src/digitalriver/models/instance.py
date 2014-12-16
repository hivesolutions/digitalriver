#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import base

class Instance(base.DRBase):

    address = appier.field(
        index = True,
        default = True
    )

    provisions = appier.field(
        type = list
    )

    def has_provision(self, name):
        return name in self.provisions
