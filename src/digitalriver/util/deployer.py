#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

import appier

import digitalriver

try: import paramiko
except: paramiko = None

class Deployer(appier.Observable):

    BASE_DIRECTORY = "/torus"
    """ The base directory where the instance configuration of the
    torus infra-structure will be positioned for execution """

    TEMP_DIRECTORY = "/tmp/torus"
    """ The temporary directory that is going to be used in the
    build process and any other ephemeral operations """

    BASE_PACKAGES = ("ruby", "nodejs")
    """ Sequence containing the various packages that are considered
    to be foundation and that should always be installed """

    def __init__(
        self,
        address = None,
        username = None,
        password = None,
        id_rsa_path = None,
        instance_c = None,
        environment = None
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
        self.environment = environment or dict()
        self.ssh = None

    def deploy_url(self, url):
        data = appier.get(url)
        is_dict = type(data) == dict

        if not is_dict:
            data = data.decode("utf-8")
            data = json.loads(data)

        self.deploy_torus(url, data)

    def deploy_torus(self, url, data):
        instance = self.get_instance()
        if instance.has_provision(url): return

        build = data["build"]
        build = self._to_absolute(url, build)
        dependencies = data.get("depends", [])

        for dependency in dependencies:
            dependency = self._to_absolute(url, dependency)
            if instance.has_provision(dependency): continue
            self.deploy_url(dependency)

        self.run_base()
        self.run_script(build)

        instance.features.append(url)
        instance.save()

    def start_torus(self, url, data):
        start = data.get("start", None)
        if not start: return
        self.run_command(start)

    def stop_torus(self, url, data):
        stop = data.get("stop", None)
        if not stop: return
        self.run_command(stop)

    def run_base(self):
        base_s = " ".join(Deployer.BASE_PACKAGES)
        self.run_command("mkdir -p %s" % Deployer.BASE_DIRECTORY)
        self.run_command("apt-get update")
        self.run_command("apt-get -y install %s" % base_s)

    def run_script(self, url):
        name = url.rsplit("/", 1)[1]
        self.run_command("mkdir -p %s" % Deployer.TEMP_DIRECTORY)
        self.run_command("cd %s && wget %s" % (Deployer.TEMP_DIRECTORY, url))
        self.run_command("cd %s && chmod +x %s && ./%s" % (Deployer.TEMP_DIRECTORY, name, name))
        self.run_command("rm -rf %s" % Deployer.TEMP_DIRECTORY)

    def run_command(self, command):
        ssh = self.get_ssh()
        prefix = " ".join([key + "=\"" + value + "\"" for key, value in self.environment])
        suffix = "2>&1"
        _stdin, stdout, _stderr = ssh.exec_command(prefix + " " + command + " " + suffix)

        while True:
            data = stdout.readline()
            if not data: break
            sys.stdout.write(data)
            sys.stdout.flush()
            self.trigger("stdout", data)

    def get_instance(self):
        return self.instance_c.singleton(address = self.address)

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

    def _to_absolute(self, base, url):
        is_absolute = url.startswith("http://") or url.startswith("https://")
        if is_absolute: return url
        base = base.rsplit("/", 1)[0]
        return base + "/" + url
