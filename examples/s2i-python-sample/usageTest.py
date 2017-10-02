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

from moduleframework import module_framework

class UsageTest(module_framework.ContainerAvocadoTest):
    """
    :avocado: enable
    """
    messages = ["This is a S2I python-", "To use it, install S2I: https://github.com/openshift/source-to-image"]

    def test_usage_message(self):
        usage_com = self.runHost("docker run %s" % self.backend.getDockerInstanceName())
        for message in self.messages:
            self.assertIn(message, usage_com.stdout)

