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
        start = self.field("start_record", 0, cast = int)
        count = self.field("list_droplets", 10, cast = int)
        droplets = api.list_droplets()
        droplets = droplets["droplets"][start:start + count]
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
            sub_link = "info",
            droplet = droplet
        )

    @appier.route("/droplets/<int:id>/provision", "GET")
    @appier.ensure("base")
    def provision(self, id):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        droplet = api.get_droplet(id)
        return self.template(
            "droplet/provision.html.tpl",
            link = "droplets",
            sub_link = "provision",
            droplet = droplet,
            provision = {},
            errors = {}
        )

    @appier.route("/droplets/<int:id>/provision", "POST")
    @appier.ensure("base")
    def do_provision(self, id):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        droplet = api.get_droplet(id)    #@todo must implement this under a model (called provision)
        networks = droplet["networks"]
        ipv4 = networks["v4"][0]
        address = ipv4["ip_address"]
        deployer = self.get_deployer(address = address)
        deployer.deploy_url("tobias") #@this is still not working
        return self.redirect(
            self.url_for("droplet.show", id = id)
        )
