#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class BaseController(appier.Controller):

    @appier.route("/", "GET")
    @appier.route("/index", "GET")
    def index(self):
        return self.template("index.html.tpl")

    @appier.route("/deploy", ("GET", "POST"))
    def deploy(self):
        pass
