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

from moduleframework.common import *


class OnlyTestsHelper(CommonFunctions):
    """
    Class for testing "modules" on local machine (host) directly. It could be used for scheduling tests for
    system packages

    :avocado: disable
    """

    def __init__(self):
        """
        Set basic variables for RPM based testing, based on modules.rpm section of config.yaml
        """
        super(OnlyTestsHelper, self).__init__()
        self.loadconfig()
        self.info = self.config['module']['only_tests']

    def setUp(self):
        """
        It is called by child class and it is same methof as Avocado/Unittest has. It prepares environment
        for RPM based testing
        * installing dependencies from config
        * setup environment from config

        :return: None
        """
        self.__callSetupFromConfig()

    def __addModuleDependency(self, url, name=None, stream="master"):
        name = name if name else self.moduleName
        if name in self.dependencylist:
            self.dependencylist[name]['urls'].append(url)
        else:
            self.dependencylist[name] = {'urls': [url], 'stream': stream}

    def tearDown(self):
        """
        cleanup enviroment and call cleanup from config

        :return: None
        """
        self.stop()
        self.__callCleanupFromConfig()

    def status(self, command="/bin/true"):
        """
        Return status of module

        :param command: which command used for do that. it could be defined inside config
        :return: bool
        """
        try:
            if 'status' in self.info and self.info['status']:
                a = self.runHost(self.info['status'], shell=True, ignore_bg_processes=True,
                                 verbose=is_not_silent())
            else:
                a = self.runHost("%s" % command, shell=True, ignore_bg_processes=True, verbose=is_not_silent())
            print_debug("command:", a.command, "stdout:", a.stdout, "stderr:", a.stderr)
            return True
        except BaseException:
            return False

    def start(self, command="/bin/true"):
        """
        start the RPM based module (like systemctl start service)

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if 'start' in self.info and self.info['start']:
            self.runHost(self.info['start'], shell=True, ignore_bg_processes=True, verbose=is_not_silent())
        else:
            self.runHost("%s" % command, shell=True, ignore_bg_processes=True, verbose=is_not_silent())

    def stop(self, command="/bin/true"):
        """
        stop the RPM based module (like systemctl stop service)

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if 'stop' in self.info and self.info['stop']:
            self.runHost(self.info['stop'], shell=True, ignore_bg_processes=True, verbose=is_not_silent())
        else:
            self.runHost("%s" % command, shell=True, ignore_bg_processes=True, verbose=is_not_silent())

    def run(self, command="ls /", **kwargs):
        """
        Run command inside module, for RPM based it is same as runHost

        :param command: str of command to execute
        :param kwargs: dict from avocado.process.run
        :return: avocado.process.run
        """
        return self.runHost('bash -c "%s"' %
                            sanitize_cmd(command), **kwargs)

    def copyTo(self, src, dest):
        """
        Copy file from one location (host) to another one to (module)

        :param src: str
        :param dest: str
        :return: None
        """
        self.runHost("cp -r %s %s" % (src, dest), verbose=is_not_silent())

    def copyFrom(self, src, dest):
        """
        Copy file from one location (module) to another one to (host)

        :param src: str
        :param dest: str
        :return: None
        """
        self.runHost("cp -r %s %s" % (src, dest), verbose=is_not_silent())

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
            self.runHost(self.info.get("cleanup"), shell=True, ignore_bg_processes=True,
                         verbose=is_not_silent())
