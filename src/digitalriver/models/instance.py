#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import base
from . import provision

class Instance(base.DRBase):

    iid = appier.field(
        index = True,
        default = True
    )

    address = appier.field(
        index = True
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

    droplet = appier.field(
        type = dict
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
    def validate(cls):
        return super(Instance, cls).validate() + [
            appier.not_null("iid"),
            appier.not_empty("iid"),
            appier.not_duplicate("iid", cls._name()),

            appier.not_null("address"),
            appier.not_empty("address"),
            appier.not_duplicate("address", cls._name())
        ]

    @classmethod
    def provision_post_create(cls, ctx):
        instance = ctx.get_instance()
        instance.address = ctx.droplet_address
        instance.provisions.append(ctx)
        instance.save()

    @classmethod
    def ensure(cls, droplet):
        instance = cls.by_droplet(droplet)
        instance.save()
        return instance

    @classmethod
    def by_droplet(cls, droplet):
        address = droplet["networks"]["v4"][0]["ip_address"]
        iid = cls.to_iid(droplet["id"])
        instance = cls.singleton(
            iid = iid,
            address = address,
            form = False
        )
        instance.iid = iid
        instance.address = address
        instance.droplet = droplet
        return instance

    @classmethod
    def by_id(cls, id):
        iid = cls.to_iid(id)
        return cls.by_iid(iid)

    @classmethod
    def by_iid(cls, iid):
        instance = cls.get(iid = iid, raise_e = False)
        print(instance)
        if instance: return instance
        return cls.new(form = False)

    @classmethod
    def to_iid(cls, id):
        return "digitalocean-" + str(id)

    def pre_validate(self):
        base.DRBase.pre_validate(self)
        is_valid = hasattr(self, "names") and hasattr(self, "values")
        if not is_valid: self.names = self.values = []

    def pre_save(self):
        base.DRBase.pre_save(self)
        self.join_config()

    def sync(self):
        if not self.address: return
        deployer = self.owner.get_deployer(
            address = self.address,
            username = "root",
            instance = self
        )
        deployer.sync_torus()

    def join_config(self):
        self.config = zip(self.names, self.values)
        return self.config

    def get_id(self):
        id_s = self.iid[13:]
        return int(id_s)

    def has_feature(self, name):
        return hasattr(self, "features") and name in self.features

    def has_provision(self, name):
        return self.has_feature(name)
