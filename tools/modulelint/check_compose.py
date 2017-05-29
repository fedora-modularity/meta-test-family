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
# Copied from: https://github.com/fedora-modularity/check_compose/blob/master/check_compose.py
#
# Authors: <rasibley@redhat.com>
#          Jan Scotka <jscotka@redhat.com>
#

from moduleframework import module_framework
from moduleframework import common
from moduleframework import pdc_data


class ComposeTest(module_framework.NspawnAvocadoTest):
    """
    Validate overall module compose.

    :avocado: enable
    """

    def test_component_profile_installability(self):
        """
        try to install and remove components for each profile
        """
        self.log.info("Checking availability of component and installation and remove them")
        for profile in self.getModulemdYamlconfig()["data"].get("profiles"):
            actualpackagelist = " ".join(
                set(self.getModulemdYamlconfig()["data"]["profiles"].get(profile))
                -set(self.backend.bootstrappackages)
            )
            packager = common.trans_dict["GUESTPACKAGER"]
            if actualpackagelist:
                self.run("%s install %s" % (packager, actualpackagelist))
                self.run("rpm -q %s" % actualpackagelist)
                self.run("%s remove %s" % (packager, actualpackagelist))
