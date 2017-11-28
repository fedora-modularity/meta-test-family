# -*- coding: utf-8 -*-
#
# Meta test family (MTF) is a tool to test components of a modular Fedora:
# https://docs.pagure.org/modularity/
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
# Authors: Jan Scotka <jscotka@redhat.com>
#

"""
module for environment setup and cleanup, to be able to split action for ansible, more steps instead of one complex
"""

from avocado.utils import service
from moduleframework.common import print_info, CommonFunctions
import os


class EnvDocker(CommonFunctions):

    def prepare_env(self):
        print_info('Loaded config for name: {}'.format(self.config['name']))
        self.installTestDependencies()
        self.__install_env()
        self.__start_service()

    def cleanup_env(self):
        self.__stop_service()

    def add_insecure_registry(self, registry):
        """
        https://github.com/fedora-modularity/meta-test-family/issues/52

        Deprecated: Append registry into inserure registry.


        :param registry: string cotain value to add to insecure registry variable to config file
        :return:
        """

        if registry not in open('/etc/sysconfig/docker', 'r').read():
            print_info("Adding %s to insecure registry" % registry)
            with open("/etc/sysconfig/docker", "a") as myfile:
                myfile.write(
                    "INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" % registry)

    def __install_env(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """

        if not os.path.exists('/usr/bin/docker'):
            self.installTestDependencies(['docker'])

    def __start_service(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """

        if not os.path.exists('/var/run/docker.sock'):
            print_info("Starting Docker")
            service_manager = service.ServiceManager()
            service_manager.start('docker')

    def __stop_service(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """

        if os.path.exists('/var/run/docker.sock'):
            print_info("Stopping Docker")
            service_manager = service.ServiceManager()
            service_manager.stop('docker')

