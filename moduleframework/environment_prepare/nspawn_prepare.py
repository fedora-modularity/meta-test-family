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

import os
from moduleframework.common import CommonFunctions, print_info, is_not_silent

selinux_state_file="/var/tmp/mtf_selinux_state"
setseto = "Permissive"


class EnvNspawn(CommonFunctions):

    def prepare_env(self):
        print_info('Loaded config for name: {}'.format(self.config['name']))
        self.installTestDependencies()
        self.__prepare_selinux()
        self.__install_machined()

    def cleanup_env(self):
        self.__cleanup()

    def __prepare_selinux(self):
        # disable selinux by default if not turned off
        if not os.environ.get('MTF_SKIP_DISABLING_SELINUX'):
            # https://github.com/fedora-modularity/meta-test-family/issues/53
            # workaround because systemd nspawn is now working well in F-26
            if not os.path.exists(selinux_state_file):
                print_info("Disabling selinux")
                actual_state = self.runHost("getenforce", ignore_status=True).stdout.strip()
                with open(selinux_state_file, 'w') as openfile:
                    openfile.write(actual_state)
                if setseto not in actual_state:
                    self.runHost("setenforce %s" % setseto,
                                 verbose=is_not_silent(),
                                 sudo=True)

    def __install_machined(self):
        # install systemd-nspawn in case not installed
        if self.runHost("machinectl --version", ignore_status=True).exit_status != 0:
            self.installTestDependencies(['systemd-container'])

    def __cleanup(self):
        if not os.environ.get('MTF_SKIP_DISABLING_SELINUX'):
            print_info("Turning back selinux to previous state")
            actual_state = self.runHost("getenforce", ignore_status=True).stdout.strip()
            if os.path.exists(selinux_state_file):
                print_info("Turning back selinux to previous state")
                with open(selinux_state_file, 'r') as openfile:
                    stored_state = openfile.readline()
                    if stored_state != actual_state:
                        self.runHost("setenforce %s" % stored_state,
                                     ignore_status=True,
                                     verbose=is_not_silent(),
                                     sudo=True)
                os.remove(selinux_state_file)
            else:
                print_info("Selinux state is not stored, skipping.")
