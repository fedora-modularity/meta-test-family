#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This Modularity Testing Framework helps you to write tests for modules
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Petr Hracek <phracek@redhat.com>
#

import json
from moduleframework.common import *


class ContainerHelper(CommonFunctions):
    """
    Basic Helper class for Docker container module type

    :avocado: disable
    """

    def __init__(self):
        """
        set basic object variables
        """
        super(ContainerHelper, self).__init__()
        self.loadconfig()
        self.info = self.config['module']['docker']
        self.tarbased = None
        self.jmeno = None
        self.docker_id = None
        self.icontainer = get_url(
        ) if get_url() else self.info['container']
        if ".tar" in self.icontainer:
            self.jmeno = "testcontainer"
            self.tarbased = True
        if "docker=" in self.icontainer:
            self.jmeno = self.icontainer[7:]
            self.tarbased = False
        elif "docker.io" in self.info['container']:
            # Trusted source
            self.tarbased = False
            self.jmeno = self.icontainer
        else:
            # untrusted source
            self.tarbased = False
            self.jmeno = self.icontainer

    def getURL(self):
        """
        It returns actual URL link string to container, It is same as URL

        :return: str
        """
        return self.icontainer

    def getDockerInstanceName(self):
        """
        Return docker instance name what will be used inside docker as docker image name
        :return: str
        """
        return self.jmeno

    def setUp(self):
        """
        It is called by child class and it is same methof as Avocado/Unittest has. It prepares environment
        for docker testing
        * start docker if not
        * pull docker image
        * setup environment from config
        * run and store identification

        :return: None
        """
        self.installTestDependencies()
        self.__callSetupFromConfig()
        self.__pullContainer()

    def tearDown(self):
        """
        Cleanup environment and call also cleanup from config

        :return: None
        """
        self.stop()
        self.__callCleanupFromConfig()


    def __pullContainer(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.tarbased:
            self.runHost(
                "docker import %s %s" %
                (self.icontainer, self.jmeno), verbose=is_not_silent())
        elif "docker=" in self.icontainer:
            pass
        else:
            self.runHost("docker pull %s" % self.jmeno, verbose=is_not_silent())

        self.containerInfo = json.loads(
            self.runHost(
                "docker inspect %s" %
                self.jmeno, verbose=is_not_silent()).stdout)[0]["Config"]

    def start(self, args="-it -d", command="/bin/bash"):
        """
        start the docker container

        :param args: Do not use it directly (It is defined in config.yaml)
        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if not self.status():
            if 'start' in self.info and self.info['start']:
                self.docker_id = self.runHost(
                    "%s -d %s" %
                    (self.info['start'], self.jmeno), shell=True, ignore_bg_processes=True,
                    verbose=is_not_silent()).stdout
            else:
                self.docker_id = self.runHost(
                    "docker run %s %s %s" %
                    (args, self.jmeno, command), shell=True, ignore_bg_processes=True, verbose=is_not_silent()).stdout
            self.docker_id = self.docker_id.strip()
            if self.getPackageList():
                a = self.run(
                    "%s install %s" %
                    (trans_dict["HOSTPACKAGER"], " ".join(
                        self.getPackageList())),
                    ignore_status=True, verbose=False)
                b = self.run(
                    "%s install %s" %
                    (trans_dict["GUESTPACKAGER"], " ".join(
                        self.getPackageList())),
                    ignore_status=True, verbose=False)
                if a.exit_status == 0:
                    print_info("Packages installed via {HOSTPACKAGER}", a.stdout)
                elif b.exit_status == 0:
                    print_info("Packages installed via {GUESTPACKAGER}", b.stdout)
                else:
                    print_info(
                        "Nothing installed (nor via {HOSTPACKAGER} nor {GUESTPACKAGER}), but package list is not empty",
                        self.getPackageList())
        if self.status() is False:
            raise ContainerExc(
                "Container %s (for module %s) is not running, probably DEAD immediately after start (ID: %s)" % (
                    self.jmeno, self.moduleName, self.docker_id))

    def stop(self):
        """
        Stop the docker container

        :return: None
        """
        if self.status():
            try:
                self.runHost("docker stop %s" % self.docker_id, verbose=is_not_silent())
                self.runHost("docker rm %s" % self.docker_id, verbose=is_not_silent())
            except Exception as e:
                print_debug(e, "docker already removed")
                pass

    def status(self):
        """
        get status if container is running

        :return: bool
        """
        if self.docker_id and self.docker_id[
                              : 12] in self.runHost(
            "docker ps", shell=True, verbose=is_not_silent()).stdout:
            return True
        else:
            return False

    def run(self, command="ls /", **kwargs):
        """
        Run command inside module, all params what allows avocado are passed inside shell,ignore_status, etc.

        :param command: str
        :param kwargs: dict
        :return: avocado.process.run
        """
        self.start()
        return self.runHost(
            'docker exec %s bash -c "%s"' %
            (self.docker_id, sanitize_cmd(command)),
            **kwargs)

    def copyTo(self, src, dest):
        """
        Copy file to module

        :param src: str path to source file
        :param dest: str path to file inside module
        :return: None
        """
        self.start()
        self.runHost("docker cp %s %s:%s" % (src, self.docker_id, dest), verbose=is_not_silent())

    def copyFrom(self, src, dest):
        """
        Copy file from module

        :param src: str path of file inside module
        :param dest: str path of destination file
        :return: None
        """
        self.start()
        self.runHost("docker cp %s:%s %s" % (self.docker_id, src, dest), verbose=is_not_silent())

    def __callSetupFromConfig(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.info.get("setup"):
            self.runHost(self.info.get("setup"), shell=True, ignore_bg_processes=True, verbose=is_not_silent())

    def __callCleanupFromConfig(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.info.get("cleanup"):
            self.runHost(self.info.get("cleanup"), shell=True, ignore_bg_processes=True, verbose=is_not_silent())

