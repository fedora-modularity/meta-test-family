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

from moduleframework.common import CommonFunctions, print_info


class EnvRpm(CommonFunctions):

    def prepare_env(self):
        print_info('Loaded config for name: {}'.format(self.config['name']))
        self.installTestDependencies()
        print_info("WARNING: Testing is going to be performed on this machine")
        pass

    def cleanup_env(self):
        print_info("WARNING: No cleanup as it can destroy this machine")
        pass
