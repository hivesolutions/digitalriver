#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

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
        droplet = api.create_droplet(droplet)

        links = droplet.get("links", {})
        actions = links.get("actions", [])
        action_id = actions[0]["id"]

        while True:
            action = api.get_action(action_id)
            status = action["status"]
            if status == "completed": break
            print("waiting for complete")
            time.sleep(1.0)

        droplet = droplet["droplet"]
        droplet_id = droplet["id"]
        droplet = api.get_droplet(droplet_id)

        networks = droplet["networks"]
        ipv4 = networks["v4"][0]
        address = ipv4["ip_address"]

        print(address)

        return self.redirect(
            self.url_for("base.index")
        )

    @appier.route("/test", ("GET", "POST"))
    def test(self):
        address = self.field("address", mandatory = True)
        username = self.field("username")
        password = self.field("password")
        id_rsa_path = self.field("id_rsa_path")

        import paramiko

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            address,
            username = username,
            password = password,
            key_filename = id_rsa_path
        )

        self.run_command(ssh, "apt-get update")
        #self.run_command(ssh, "apt-get -y upgrade")
        #self.run_command(ssh, "apt-get -y dist-upgrade")
        #self.run_command(ssh, "apt-get -y autoremove")
        self.run_command(ssh, "apt-get -y install ruby nodejs")
        #self.run_script(ssh, "https://raw.githubusercontent.com/hivesolutions/config/master/instances/base/docker.sh")
        #self.run_script(ssh, "https://raw.githubusercontent.com/hivesolutions/config/master/instances/base/mysql.docker.sh")
        #self.run_script(ssh, "https://raw.githubusercontent.com/hivesolutions/config/master/instances/base/redis.docker.sh")

    def run_script(self, ssh, url):
        name = url.rsplit("/", 1)[1]
        self.run_command(ssh, "wget %s" % url)
        self.run_command(ssh, "chmod +x %s && ./%s" % (name, name))

    def run_command(self, ssh, command):
        _stdin, stdout, _stderr = ssh.exec_command(command + " 2>&1")

        while True:
            data = stdout.readline()
            if not data: break
            sys.stdout.write(data)
            sys.stdout.flush()

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
