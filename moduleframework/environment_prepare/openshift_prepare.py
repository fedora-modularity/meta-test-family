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
        self.__prepare_selinux()
        self.__start_openshift_cluster()

    def cleanup_env(self):
        self.__stop_openshift_cluster()

    def __prepare_selinux(self):
        # disable selinux by default if not turned off
        if not os.environ.get('MTF_SKIP_DISABLING_SELINUX'):
            # https://github.com/fedora-modularity/meta-test-family/issues/53
            # workaround because systemd nspawn is now working well in F-26
            if not os.path.exists(selinux_state_file):
                common.print_info("Disabling selinux")
                actual_state = self.runHost("getenforce", ignore_status=True).stdout.strip()
                with open(selinux_state_file, 'w') as openfile:
                    openfile.write(actual_state)
                if setseto not in actual_state:
                    self.runHost("setenforce %s" % setseto,
                                 verbose=common.is_not_silent(),
                                 sudo=True)

    def __cleanup(self):
        if not os.environ.get('MTF_SKIP_DISABLING_SELINUX'):
            common.print_info("Turning back selinux to previous state")
            actual_state = self.runHost("getenforce", ignore_status=True).stdout.strip()
            if os.path.exists(selinux_state_file):
                common.print_info("Turning back selinux to previous state")
                with open(selinux_state_file, 'r') as openfile:
                    stored_state = openfile.readline()
                    if stored_state != actual_state:
                        self.runHost("setenforce %s" % stored_state,
                                     ignore_status=True,
                                     verbose=common.is_not_silent(),
                                     sudo=True)
                os.remove(selinux_state_file)
            else:
                common.print_info("Selinux state is not stored, skipping.")

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
        if os.environ.get('OPENSHIFT_LOCAL'):
            if not os.path.exists('/usr/bin/oc'):
                self.installTestDependencies(['origin', 'origin-clients'])

    def __start_openshift_cluster(self):
        """
        Internal method, do not use it anyhow. It starts OpenShift cluster

        :return: None
        """

        if os.environ.get('OPENSHIFT_LOCAL'):
            if int(self.__oc_status()) == 0:
                common.print_info("Seems like OpenShift is already started.")
            else:
                common.print_info("Starting OpenShift")
                self.runHost("oc cluster up", verbose=common.is_not_silent())

    def __stop_openshift_cluster(self):
        """
        Internal method, do not use it anyhow. It stops OpenShift cluster

        :return: None
        """
        if os.environ.get('OPENSHIFT_LOCAL'):
            if int(self.__oc_status()) == 0:
                common.print_info("Stopping OpenShift")
                self.runHost("oc cluster down", verbose=common.is_not_silent())
            else:
                common.print_info("OpenShift is already stopped.")

