#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import base
from . import provision

class Instance(base.DRBase):

    address = appier.field(
        index = True,
        default = True
    )

    features = appier.field(
        type = list
    )

    provisions = appier.field(
        type = appier.references(
            provision.Provision,
            name = "pid"
        )
    )

    def has_provision(self, name):
        return name in self.features
