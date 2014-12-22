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

    names = appier.field(
        type = list
    )

    values = appier.field(
        type = list
    )

    config = appier.field(
        type = list
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
        instance.address = ctx.droplet_address
        instance.provisions.append(ctx)
        instance.save()

    @classmethod
    def by_droplet(cls, droplet):
        address = droplet["networks"]["v4"][0]["ip_address"]
        instance = cls.singleton(address = address)
        instance.address = address
        return instance

    def pre_save(self):
        base.DRBase.pre_save(self)
        self.join_config()

    def join_config(self):
        self.config = zip(self.names, self.values)
        return self.config

    def has_feature(self, name):
        return hasattr(self, "features") and name in self.features

    def has_provision(self, name):
        return self.has_feature(name)
