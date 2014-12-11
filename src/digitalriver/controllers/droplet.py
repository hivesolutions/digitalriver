#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class DropletController(appier.Controller):

    @appier.route("/droplets", "GET")
    @appier.ensure("base")
    def list(self):
        url = self.ensure_api()
        if url: return self.redirect(url)
        return self.template(
            "droplet/list.html.tpl",
            link = "droplets"
        )

    @appier.route("/droplets.json", "GET", json = True)
    @appier.ensure("base")
    def list_json(self):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        droplets = api.list_droplets()
        droplets = droplets["droplets"]
        return droplets

    @appier.route("/droplets/<int:id>", "GET")
    @appier.ensure("base")
    def show(self, id):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        droplet = api.get_droplet(id)
        return self.template(
            "droplet/show.html.tpl",
            link = "droplets",
            droplet = droplet
        )
