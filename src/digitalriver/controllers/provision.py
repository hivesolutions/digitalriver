#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import digitalriver

class ProvisionController(appier.Controller):

    @appier.route("/provisions", "GET")
    @appier.ensure("base")
    def list(self):
        return self.template(
            "provision/list.html.tpl",
            link = "provisions"
        )

    @appier.route("/provisions.json", "GET", json = True)
    @appier.ensure("base")
    def list_json(self):
        object = appier.get_object(alias = True, find = True)
        provisions = digitalriver.Provision.find(map = True, **object)
        return provisions
