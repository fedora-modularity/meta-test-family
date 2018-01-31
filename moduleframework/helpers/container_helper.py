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
from moduleframework.mtfexceptions import ContainerExc


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
        static_name = "testcontainer"
        self.tarbased = None
        self.name = None
        self.docker_id = None
        self._icontainer = self.get_url()
        if not self._icontainer:
            raise ConfigExc("No container image specified in the configuration file or environment variable.")
        if ".tar" in self._icontainer:
            self.name = static_name
            self.tarbased = True
        if "docker=" in self._icontainer:
            self.name = self._icontainer[7:]
            self.tarbased = False
        else:
            # untrusted source
            self.tarbased = False
            self.name = self._icontainer
        self.docker_static_name = ""
        if get_if_reuse():
            self.docker_static_name = "--name %s" % static_name

    def getURL(self):
        """
        It returns actual URL link string to container, It is same as URL

        :return: str
        """
        warnings.warn("Function getURL is deprecated. Use self.URL instead",
                      DeprecationWarning)
        return self._icontainer

    @property
    def URL(self):
        """
        It returns actual URL link string to container, It is same as URL

        :return: str
        """
        return self._icontainer

    @URL.setter
    def URL(self, value):
        self._icontainer = value

    def getDockerInstanceName(self):
        """
        Return docker instance name what will be used inside docker as docker image name
        :return: str
        """
        return self.name

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
        self._icontainer = self.get_url()
        self._callSetupFromConfig()
        self.__pullContainer()
        self.containerInfo = self.__load_inspect_json()

    def tearDown(self):
        """
        Cleanup environment and call also cleanup from config

        :return: None
        """
        super(ContainerHelper, self).tearDown()
        if get_if_do_cleanup():
            print_info("To run a command inside a container execute: ",
                        "docker exec %s /bin/bash" % self.docker_id)

    def __pullContainer(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.tarbased:
            self.runHost(
                "docker import %s %s" %
                (self._icontainer, self.name), verbose=is_not_silent())
        elif "docker=" in self._icontainer:
            pass
        else:
            self.runHost("docker pull %s" % self.name, verbose=is_not_silent())

    def __load_inspect_json(self):
        """
        Load json data from docker inspect command

        :return: dict
        """
        return json.loads(
            self.runHost(
                "docker inspect %s" %
                self.name, verbose=is_not_silent()).stdout)[0]["Config"]

    def start(self, args="-it -d", command="/bin/bash"):
        """
        start the docker container

        :param args: Do not use it directly (It is defined in config.yaml)
        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if not self.status():
            if self.info.get('start'):
                self.docker_id = self.runHost(
                    "%s -d %s %s" %
                    (self.info['start'], self.docker_static_name, self.name), shell=True, ignore_bg_processes=True,
                    verbose=is_not_silent()).stdout
            else:
                self.docker_id = self.runHost(
                    "docker run %s %s %s %s" %
                    (args, self.docker_static_name, self.name, command),
                    shell=True, ignore_bg_processes=True, verbose=is_not_silent()).stdout
            self.docker_id = self.docker_id.strip()
            # It installs packages in container is removed by default, in future maybe reconciled.
            # self.install_packages()
        if self.status() is False:
            raise ContainerExc(
                "Container %s (for module %s) is not running, probably DEAD immediately after start (ID: %s)" % (
                    self.name, self.moduleName, self.docker_id))
            trans_dict["GUESTPACKAGER"] = self.get_packager()

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

    def status(self, command=None):
        """
        get status if container is running

        :return: bool
        """
        if not self.docker_id and get_if_reuse():
            result = self.runHost("docker ps -q --filter %s" % self.docker_static_name[2:],
                                  ignore_status=True,
                                  verbose=is_debug())
            # lenght of docker id  number is 12
            if result.exit_status == 0 and len(result.stdout) > 10:
                self.docker_id = result.stdout.strip()
                return True
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

