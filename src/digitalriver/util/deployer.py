#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

import appier

import digitalriver

try: import paramiko
except: paramiko = None

class Deployer(appier.Observable):

    def __init__(
        self,
        address = None,
        username = None,
        password = None,
        id_rsa_path = None,
        instance_c = None
    ):
        appier.Observable.__init__(self)
        self.address = appier.conf("DR_ADDRESS", None)
        self.username = appier.conf("DR_USERNAME", None)
        self.password = appier.conf("DR_PASSWORD", None)
        self.id_rsa_path = appier.conf("DR_KEY_PATH", None)
        self.address = address or self.address
        self.username = username or self.username
        self.password = password or self.password
        self.id_rsa_path = id_rsa_path or self.id_rsa_path
        self.instance_c = instance_c or digitalriver.Instance
        self.ssh = None

    def deploy_url(self, url):
        data = appier.get(url)
        is_dict = type(data) == dict

        if not is_dict:
            data = data.decode("utf-8")
            data = json.loads(data)

        self.deploy_torus(data)

    def deploy_torus(self, url, data):
        instance = self.get_instance()
        build = data["build"]
        dependencies = data.get("depends", [])

        for dependency in dependencies:
            if instance.has_provision(dependency): continue
            self.deploy_url(dependency)

        self.run_base()
        self.run_script(build)

        instance.provisions.append(url)
        instance.save()

    def run_base(self):
        self.run_command("apt-get update")
        self.run_command("apt-get -y install ruby nodejs")

    def run_script(self, url):
        name = url.rsplit("/", 1)[1]
        self.run_command("wget %s" % url)
        self.run_command("chmod +x %s && ./%s" % (name, name))

    def run_command(self, command):
        ssh = self.get_ssh()
        _stdin, stdout, _stderr = ssh.exec_command(command + " 2>&1")

        while True:
            data = stdout.readline()
            if not data: break
            sys.stdout.write(data)
            sys.stdout.flush()
            self.trigger("stdout", data)

    def get_instance(self):
        instance = self.instance_c.get(address = self.address, raise_e = False)
        if instance: return instance
        instance = self.instance_c(address = self.address)
        return instance

    def get_ssh(self, force = False):
        # in case the ssh connection already exists and no
        # forced is ensured, returns the current connection
        if self.ssh and not force: return self.ssh

        # creates the proper ssh client with the remote host
        # adding the proper policies and then runs the connection
        # with the provided credentials and key file values
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            self.address,
            username = self.username,
            password = self.password,
            key_filename = self.id_rsa_path
        )
        return self.ssh
