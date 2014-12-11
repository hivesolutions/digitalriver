#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import digitalocean

SPEC_URL = "https://raw.githubusercontent.com/hivesolutions/config/master/instances/base/docker.sh"

class BaseController(appier.Controller):

    @appier.route("/", "GET")
    @appier.route("/index", "GET")
    def index(self):
        state = self.field("state")
        if state: return self.redirect(
            self.url_for("base.deploy"),
            spec_url = state
        )
        return self.template("index.html.tpl")

    @appier.route("/deploy", ("GET", "POST"))
    def deploy(self):
        spec_url = self.field("spec_url", SPEC_URL)
        url = self.ensure_api(state = spec_url)
        if url: return self.redirect(url)
        api = self.get_api()
        droplet = dict(
            name = self.field("name", "digitalriver"),
            region = self.field("region", "ams1"),
            size = self.field("size", "512mb"),
            image = self.field("image", "ubuntu-14-04-x64"),
            ssh_keys = self.field("ssh_keys", None),
            backups = self.field("backups", False, cast = bool),
            ipv6 = self.field("ipv6", False, cast = bool),
            private_networking = self.field("private_networking", None),
            user_data = self.field("user_data", None)
        )
        api.create_droplet(droplet)

    @appier.route("/oauth", "GET")
    def oauth(self):
        code = self.field("code")
        state = self.field("state")
        api = self.get_api()
        access_token = api.oauth_access(code)
        self.session["do.access_token"] = access_token
        return self.redirect(
            self.url_for("base.index"),
            state = state
        )

    @appier.exception_handler(appier.OAuthAccessError)
    def oauth_error(self, error):
        if "do.access_token" in self.session: del self.session["do.access_token"]
        return self.redirect(
            self.url_for("base.index")
        )

    def ensure_api(self, state = None):
        access_token = self.session.get("do.access_token", None)
        if access_token: return
        api = self._get_api()
        return api.oauth_authorize(state = state)

    def get_api(self):
        access_token = self.session and self.session.get("do.access_token", None)
        api = self._get_api()
        api.access_token = access_token
        return api

    def _get_api(self):
        return digitalocean.Api(
            client_id = appier.conf("DO_ID"),
            client_secret = appier.conf("DO_SECRET"),
            redirect_url = appier.conf("DO_REDIRECT_URL")
        )
