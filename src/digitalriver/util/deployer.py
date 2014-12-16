#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import appier

try: import paramiko
except: paramiko = None

class Deployer(object):

    def __init__(self, address = None, username = None, password = None, id_rsa_path = None):
        self.address = appier.conf("DR_ADDRESS", None)
        self.username = appier.conf("DR_USERNAME", None)
        self.password = appier.conf("DR_PASSWORD", None)
        self.id_rsa_path = appier.conf("DR_KEY_PATH", None)
        self.address = address or self.address
        self.username = username or self.username
        self.password = password or self.password
        self.id_rsa_path = id_rsa_path or self.id_rsa_path

    def deploy_url(self, url):
        # creates the proper ssh client with the remote host
        # adding the proper policies and then runs the connection
        # with the provided credentials and key file values
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.address,
            username = self.username,
            password = self.password,
            key_filename = self.id_rsa_path
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
