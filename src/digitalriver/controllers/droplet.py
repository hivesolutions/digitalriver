#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import digitalriver

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

    @appier.route("/droplets/<int:id>/config", "GET")
    @appier.ensure("base")
    def config(self, id):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        droplet = api.get_droplet(id)
        instance = digitalriver.Instance.by_droplet(droplet)
        return self.template(
            "droplet/config.html.tpl",
            link = "droplets",
            sub_link = "config",
            droplet = droplet,
            instance = instance,
            errors = {}
        )

    @appier.route("/droplets/<int:id>/config", "POST")
    @appier.ensure("base")
    def do_config(self, id):
        instance = digitalriver.Instance.singleton()
        try: instance.save()
        except appier.ValidationError as error:
            url = self.ensure_api()
            if url: return self.redirect(url)
            api = self.get_api()
            droplet = api.get_droplet(id)
            instance = digitalriver.Instance.by_droplet(droplet)
            return self.template(
                "droplet/config.html.tpl",
                link = "droplets",
                sub_link = "config",
                droplet = droplet,
                isntance = error.model,
                errors = error.errors
            )
        return self.redirect(
            self.url_for("droplet.show", id = id)
        )

    @appier.route("/droplets/<int:id>/provision", "GET")
    @appier.ensure("base")
    def new_provision(self, id):
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
    def create_provision(self, id):
        provision = digitalriver.Provision.new()
        try: provision.save()
        except appier.ValidationError as error:
            url = self.ensure_api()
            if url: return self.redirect(url)
            api = self.get_api()
            droplet = api.get_droplet(id)
            return self.template(
                "droplet/provision.html.tpl",
                link = "droplets",
                sub_link = "provision",
                droplet = droplet,
                provision = error.model,
                errors = error.errors
            )
        return self.redirect(
            self.url_for("provision.log", pid = provision.pid)
        )
