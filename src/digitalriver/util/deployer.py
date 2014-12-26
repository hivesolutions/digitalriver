#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

import appier

import digitalriver

try: import paramiko
except: paramiko = None

class Deployer(appier.Observable):

    CONFIG_FILE = "config.env"
    """ The name of the file that is going to be used to store the
    bash related variable exporting, to be used during runtime """

    DATA_DIRECTORY = "/data"
    """ The directory where all the ephemeral/persistent data will
    be stored and it's considered the state of the machine """

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

    def deploy_url(self, url, force = False):
        data = appier.get(url)
        is_dict = type(data) == dict

        if not is_dict:
            data = data.decode("utf-8")
            data = json.loads(data)

        self.deploy_torus(url, data, force = force)

    def deploy_torus(self, url, data, force = False):
        instance = self.get_instance()
        skip = instance.has_provision(url) and not force
        if skip: self.trigger("stdout", "Skipped '%s'" % url); return

        build = data["build"]
        build = self._to_absolute(url, build)
        dependencies = data.get("depends", [])

        for dependency in dependencies:
            dependency = self._to_absolute(url, dependency)
            if instance.has_provision(dependency): continue
            self.deploy_url(dependency)

        self.run_base()
        self.run_config()
        self.run_script(build)
        self.close_ssh()

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

    def has_base(self):
        cls = self.__class__
        return self.run_command("ls %s" % cls.BASE_DIRECTORY) == 0

    def run_base(self):
        cls = self.__class__
        if self.has_base(): return
        base_path = "%s/%s" % (cls.BASE_DIRECTORY, cls.CONFIG_FILE)
        data_path = "%s/%s" % (cls.DATA_DIRECTORY, cls.CONFIG_FILE)
        base_s = " ".join(cls.BASE_PACKAGES)
        self.run_command("mkdir -p %s" % cls.BASE_DIRECTORY)
        self.run_command("mkdir -p %s" % cls.DATA_DIRECTORY)
        self.run_command("ln -s %s %s" % (base_path, data_path))
        self.run_command("apt-get update")
        self.run_command("apt-get -y install %s" % base_s)

    def run_config(self):
        cls = self.__class__
        items = self.environment.items()
        base_path = "%s/%s" % (cls.BASE_DIRECTORY, cls.CONFIG_FILE)
        config_s = "\\n".join(["export " + key + "=\\${" + key + "-" + value + "}" for key, value in items])
        self.run_command("printf \"%s\" > %s" % (config_s, base_path))

    def run_script(self, url):
        cls = self.__class__
        name = url.rsplit("/", 1)[1]
        self.run_command("rm -rf %s && mkdir -p %s" % (cls.TEMP_DIRECTORY, cls.TEMP_DIRECTORY))
        self.run_command("cd %s && wget %s" % (cls.TEMP_DIRECTORY, url))
        self.run_command("cd %s && chmod +x %s && ./%s" % (cls.TEMP_DIRECTORY, name, name))
        self.run_command("rm -rf %s" % cls.TEMP_DIRECTORY)

    def run_command(self, command):
        # builds the prefix string containing the various environment
        # variables for the execution so that the command runs in context
        prefix = " ".join([key + "=\"" + value + "\"" for key, value in self.environment.items()])

        # retrieves the reference to the current ssh connection and
        # then creates a new channel stream for command execution
        ssh = self.get_ssh()
        transport = ssh.get_transport()
        channel = transport.open_session()

        try:
            stdout = channel.makefile()
            channel.set_combine_stderr(True)
            channel.exec_command(prefix + " $SHELL -c '" + command + "'")

            while True:
                data = stdout.readline()
                if not data: break
                sys.stdout.write(data)
                sys.stdout.flush()
                self.trigger("stdout", data)

            code = channel.recv_exit_status()
        except:
            channel.close()

        return code

    def get_instance(self):
        return self.instance_c.singleton(
            address = self.address,
            apply = False
        )

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

    def close_ssh(self):
        ssh = self.get_ssh()
        ssh.close()

    def _to_absolute(self, base, url):
        is_absolute = url.startswith("http://") or url.startswith("https://")
        if is_absolute: return url
        base = base.rsplit("/", 1)[0]
        return base + "/" + url
