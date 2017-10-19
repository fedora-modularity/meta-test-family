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
from __future__ import print_function

from moduleframework import module_framework


class ModuleLintSigning(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=docker,fedora,rhel,tier1,WIP
    """

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        if self.moduleType != "docker":
            self.skip("Docker specific test")
        super(self.__class__, self).setUp()

    def test(self):
        RHKEY = "fd431d51"
        FEDKEY = "73bde98381b46521"
        KEY = FEDKEY
        self.start()
        allpackages = self.run(
            r'rpm -qa --qf="%{{name}}-%{{version}}-%{{release}} %{{SIGPGP:pgpsig}}\n"').stdout
        for package in [x.strip() for x in allpackages.split('\n')]:
            pinfo = package.split(', ')
            if len(pinfo) == 3:
                if KEY in pinfo[2]:
                    self.assertTrue(True,msg="%s in %s" % (KEY,pinfo[2]))
                else:
                    self.log.warn("Package sign verify failed: %s not in %s" % (KEY,pinfo[2]))


class ModuleLintPackagesCheck(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=docker,fedora,rhel,tier1
    """

    def test(self):
        self.start()
        allpackages = [
            x.strip()
            for x in self.run(r'rpm -qa --qf="%{{name}}\n"').stdout.split('\n')]
        for pkg in self.backend.getPackageList():
            self.assertIn(pkg, allpackages)
