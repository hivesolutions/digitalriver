#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import threading

import pushi
import appier

from . import base

class Provision(base.DRBase):

    pid = appier.field(
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

    config = appier.field(
        type = dict
    )

    log = appier.field(
        type = list
    )

    @classmethod
    def validate(cls):
        return super(Provision, cls).validate() + [
            appier.not_null("pid"),
            appier.not_empty("pid"),

            appier.not_null("droplet_id"),

            appier.not_null("droplet_address"),
            appier.not_empty("droplet_address"),

            appier.not_null("url"),
            appier.not_empty("url")
        ]

    def pre_validate(self):
        base.DRBase.pre_validate(self)
        self.pid = str(uuid.uuid4())

    def post_create(self):
        base.DRBase.post_create(self)
        thread = threading.Thread(target = self.deploy)
        thread.start()

    def deploy(self):
        logger = self.create_logger()
        deployer = self.owner.get_deployer(
            address = self.droplet_address,
            username = "root"
        )
        deployer.bind("stdout", logger)
        deployer.deploy_url(self.url)

    def create_logger(self):
        data_logger = self.create_data()
        pushi_logger = self.create_pushi()

        def logger(message):
            data_logger(message)
            pushi_logger(message)

        return logger

    def create_data(self):

        def logger(message):
            provision = Provision.get(pid = self.pid)
            provision.log.append(message)
            provision.save()

        return logger

    def create_pushi(self):

        def on_connect(connection):
            connection.subscribe_pushi(self.pid)

        client_key = appier.conf("PUSHI_KEY")
        client = pushi.PushiClient(client_key = client_key)
        connection = client.connect_pushi(callback = on_connect)

        def logger(message):
            connection.send_channel("stdout", message, self.pid, persist = False)

        return logger
