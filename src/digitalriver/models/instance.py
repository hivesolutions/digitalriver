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

    @classmethod
    def setup(cls):
        super(base.DRBase, cls).setup()
        provision.Provision.bind_g("post_create", cls.provision_post_create)

    @classmethod
    def provision_post_create(cls, ctx):
        instance = Instance.singleton(address = ctx.droplet_address)
        instance.provisions.append(ctx)
        instance.save()

    def has_provision(self, name):
        return name in self.features
