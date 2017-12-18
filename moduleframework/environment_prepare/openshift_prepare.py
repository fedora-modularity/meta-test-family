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
# Authors: Petr Hracek <phracek@redhat.com>
#

"""
module for OpenShift environment setup and cleanup
"""

import os
from moduleframework.common import CommonFunctions
from moduleframework import common

selinux_state_file="/var/tmp/mtf_selinux_state"
setseto = "Permissive"


class EnvOpenShift(CommonFunctions):

    def prepare_env(self):
        common.print_info('Loaded config for name: {}'.format(self.config['name']))
        self.__start_openshift_cluster()

    def cleanup_env(self):
        self.__stop_openshift_cluster()

    def __oc_status(self):
        oc_status = self.runHost("oc status", ignore_status=True, verbose=common.is_not_silent())
        common.print_debug(oc_status.stdout)
        common.print_debug(oc_status.stderr)
        return oc_status.exit_status

    def __install_env(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if common.get_openshift_local():
            if not os.path.exists('/usr/bin/oc'):
                self.installTestDependencies(['origin', 'origin-clients'])

    def __start_openshift_cluster(self):
        """
        Internal method, do not use it anyhow. It starts OpenShift cluster

        :return: None
        """

        if common.get_openshift_local():
            if int(self.__oc_status()) == 0:
                common.print_info("Seems like OpenShift is already started.")
            else:
                oc_run = self.runHost("oc cluster up", ignore_status=True)
                common.print_info(oc_run.stdout)
                common.print_info(oc_run.stderr)

    def __stop_openshift_cluster(self):
        """
        Internal method, do not use it anyhow. It stops OpenShift cluster

        :return: None
        """
        if common.get_openshift_local():
            if int(self.__oc_status()) == 0:
                common.print_info("Stopping OpenShift")
                self.runHost("oc cluster down", verbose=common.is_not_silent())
            else:
                common.print_info("OpenShift is already stopped.")

