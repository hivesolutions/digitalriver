#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

import appier

try: import paramiko
except: paramiko = None

class Deployer(appier.Observable):
    """
    Base deployer class responsible for the deploying operations
    under the Torus infra-structure. It's design should respect
    a modular design so that it may be used in multiple back-ends.
    """

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
        provision = None,
        environment = None,
        config_file = None,
        data_directory = None,
        base_directory = None,
        temp_directory = None,
        base_packages = None
    ):
        appier.Observable.__init__(self)
        cls = self.__class__
        self.address = appier.conf("DR_ADDRESS", None)
        self.username = appier.conf("DR_USERNAME", None)
        self.password = appier.conf("DR_PASSWORD", None)
        self.id_rsa_path = appier.conf("DR_KEY_PATH", None)
        self.address = address or self.address
        self.username = username or self.username
        self.password = password or self.password
        self.id_rsa_path = id_rsa_path or self.id_rsa_path
        self.provision = provision or None
        self.environment = environment or self.provision.extra_config()
        self.config_file = config_file or cls.CONFIG_FILE
        self.data_directory = data_directory or cls.DATA_DIRECTORY
        self.base_directory = base_directory or cls.BASE_DIRECTORY
        self.temp_directory = temp_directory or cls.TEMP_DIRECTORY
        self.base_packages = base_packages or cls.BASE_PACKAGES
        self.ssh = None

    def deploy_url(self, url, force = False):
        data = appier.get(url)
        is_dict = type(data) == dict

        if not is_dict:
            data = data.decode("utf-8")
            data = json.loads(data)

        self.deploy_torus(url, data, force = force)

    def deploy_torus(self, url, data, force = False):
        instance = self.provision.get_instance()
        skip = instance.has_provision(url) and not force
        if skip: self.trigger("stdout", "Skipped '%s'" % url); return

        build = data["build"]
        build = self._to_absolute(url, build)
        dependencies = data.get("depends", [])

        for dependency in dependencies:
            dependency = self._to_absolute(url, dependency)
            if instance.has_provision(dependency): continue
            self.deploy_url(dependency)

        self.build_all(data = data)
        self.run_script(build, env = True)
        self.close_ssh()

        self.trigger("deployed", url)

    def start_torus(self, url, data):
        start = data.get("start", None)
        if not start: return
        self.run_command(start)

    def stop_torus(self, url, data):
        stop = data.get("stop", None)
        if not stop: return
        self.run_command(stop)

    def has_base(self):
        return self.run_command("ls %s" % self.base_directory, output = False) == 0

    def build_all(self, data = None):
        self.build_base()
        self.build_config()
        self.build_feature(data = data)

    def build_base(self):
        if self.has_base(): return
        base_path = "%s/%s" % (self.base_directory, self.config_file)
        data_path = "%s/%s" % (self.data_directory, self.config_file)
        base_s = " ".join(self.base_packages)
        self.run_command("mkdir -p %s" % self.base_directory)
        self.run_command("mkdir -p %s" % self.data_directory)
        self.run_command("ln -s %s %s" % (base_path, data_path))
        self.run_command("apt-get update")
        self.run_command("apt-get -y install %s" % base_s)

    def build_config(self):
        instance = self.provision.get_instance()
        items = instance.config
        config_path = "%s/%s" % (self.base_directory, self.config_file)
        config_s = "\\n".join(["export " + key + "=\\${" + key + "-" + value + "}" for key, value in items])
        self.run_command("printf \"%s\" > %s" % (config_s, config_path))

    def build_feature(self, data = None):
        name = self.provision.get_name()
        items = self.provision.join_config()
        provision_directory = "%s/features/%s" % (self.base_directory, name)
        config_path = "%s/%s" % (provision_directory, self.config_file)
        start_path = "%s/%s" % (provision_directory, "start.sh")
        stop_path = "%s/%s" % (provision_directory, "stop.sh")
        torus_path = "%s/%s" % (provision_directory, "torus.json")
        config_s = "\\n".join(["export " + key + "=\\${" + key + "-" + value + "}" for key, value in items])
        self.run_command("rm -rf %s && mkdir -p %s" % (provision_directory, provision_directory))
        self.run_command("printf \"%s\" > %s" % (config_s, config_path))
        if not data: return
        start_s = data.get("start", "")
        stop_s = data.get("stop", "")
        data_s = json.dumps(data)
        self.run_command("cat > %s << \"EOF\"\n%s\nEOF\n" % (torus_path, data_s))
        self.run_command("cat > %s << \"EOF\"\n%s\nEOF\n" % (start_path, start_s))
        self.run_command("cat > %s << \"EOF\"\n%s\nEOF\n" % (stop_path, stop_s))
        self.run_command("chmod +x %s" % start_path)
        self.run_command("chmod +x %s" % stop_path)

    def run_script(self, url, env = False):
        name = url.rsplit("/", 1)[1]
        self.run_command("rm -rf %s && mkdir -p %s" % (self.temp_directory, self.temp_directory))
        self.run_command("cd %s && wget %s" % (self.temp_directory, url))
        self.run_command("cd %s && chmod +x %s && ./%s" % (self.temp_directory, name, name), env = env)
        self.run_command("rm -rf %s" % self.temp_directory)

    def run_command(self, command, env = False, output = True, timeout = None, bufsize = -1):
        # builds the prefix string containing the various environment
        # variables for the execution so that the command runs in context
        prefix = " ".join([key + "=\"" + value + "\"" for key, value in self.environment])
        if not env: prefix = ""

        # retrieves the reference to the current ssh connection and
        # then creates a new channel stream for command execution
        ssh = self.get_ssh()
        transport = ssh.get_transport()
        channel = transport.open_session()

        try:
            channel.settimeout(timeout)
            channel.set_combine_stderr(True)
            _stdin = channel.makefile("wb", bufsize)
            stdout = channel.makefile("r", bufsize)
            channel.exec_command(prefix + " $SHELL -c '" + command + "'")

            while True:
                data = stdout.readline()
                if not data: break
                if not output: continue
                sys.stdout.write(data)
                sys.stdout.flush()
                self.trigger("stdout", data)

            code = channel.recv_exit_status()
        except:
            channel.close()

        return code

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
        if not self.ssh: return
        self.ssh.close()
        self.ssh = None

    def _to_absolute(self, base, url):
        is_absolute = url.startswith("http://") or url.startswith("https://")
        if is_absolute: return url
        base = base.rsplit("/", 1)[0]
        return base + "/" + url
