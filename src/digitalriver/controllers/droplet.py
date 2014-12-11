#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class DropletController(appier.Controller):

    @appier.route("/droplets", "GET")
    def list(self, id):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        droplets = api.list_droplets(id)
        return self.template(
            "droplet/list.html.tpl",
            droplets = droplets["droplets"]
        )

    @appier.route("/droplets/<str:id>", "GET")
    def show(self, id):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        droplet = api.get_droplet(id)
        return self.template(
            "droplet/show.html.tpl",
            droplet = droplet
        )
