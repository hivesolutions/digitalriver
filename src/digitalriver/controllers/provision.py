#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import digitalriver

class ProvisionController(appier.Controller):

    @appier.route("/provisions", "GET")
    @appier.ensure(token = "base")
    def list(self):
        return self.template(
            "provision/list.html.tpl",
            link = "provisions"
        )

    @appier.route("/provisions.json", "GET", json = True)
    @appier.ensure(token = "base")
    def list_json(self):
        object = appier.get_object(
            alias = True,
            find = True,
            sort = [("created", -1)]
        )
        provisions = digitalriver.Provision.find(map = True, **object)
        return provisions

    @appier.route("/provisions/<str:pid>", "GET")
    @appier.ensure(token = "base")
    def show(self, pid):
        provision = digitalriver.Provision.get(pid = pid)
        return self.template(
            "provision/show.html.tpl",
            link = "provisions",
            sub_link = "info",
            provision = provision
        )

    @appier.route("/provisions/<str:pid>/log", "GET")
    @appier.ensure(token = "base")
    def log(self, pid):
        provision = digitalriver.Provision.get(pid = pid)
        return self.template(
            "provision/log.html.tpl",
            link = "provisions",
            sub_link = "log",
            style_flags = "wide",
            provision = provision
        )
