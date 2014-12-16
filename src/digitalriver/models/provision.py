#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid

import appier

from . import base

class Provision(base.DRBase):

    id = appier.field(
        index = True,
        immutable = True,
        default = True
    )

    droplet_id = appier.field(
        type = int,
        index = True,
        immutable = True
    )

    droplet_address = appier.field(
        index = True,
        immutable = True
    )

    url = appier.field(
        index = True,
        immutable = True
    )

    log = appier.field()

    @classmethod
    def validate(cls):
        return super(Provision, cls).validate() + [
            appier.not_null("id"),
            appier.not_empty("id"),

            appier.not_null("droplet_id"),

            appier.not_null("droplet_address"),
            appier.not_empty("droplet_address"),

            appier.not_null("url"),
            appier.not_empty("url")
        ]

    def pre_validate(self):
        base.DRBase.pre_validate(self)
        self.id = str(uuid.uuid4())

    def post_create(self):
        base.DRBase.post_create(self)
        self.deploy()

    def deploy(self):
        api = self.owner.get_api()
        if not api: return
        deployer = self.owner.get_deployer(
            address = self.droplet_address,
            username = "root"
        )
        deployer.deploy_url(self.url)
