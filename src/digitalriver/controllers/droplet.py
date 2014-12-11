#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class DropletController(appier.Controller):

    @appier.route("/providers/<str:id>", "GET")
    def show(self, id):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        droplet = api.get_droplet(id)
        return self.template(
            "droplet/show.html.tpl",
            droplet = droplet
        )
