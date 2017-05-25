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
# Authors: Jan Scotka <jscotka@redhat.com>
#


from moduleframework import module_framework
from avocado.utils import process

def rpmSetup():
    process.run("/bin/true; echo setup", shell=True)

def rpmStart():
    process.run("/bin/true; echo start", shell=True)

def rpmStatus():
    process.run("/bin/true; echo status", shell=True)

def rpmStop():
    process.run("/bin/true; echo stop", shell=True)

config={"module":{
    "rpm":{
        "setup": rpmSetup,
        "start": rpmStart,
        "stop": rpmStop,
        "status": rpmStart},
    "docker":{
        "setup": dockerSetup,
        "start": dockerStart,
        "stop": dockerStop,
        "status": dockerStart}
    }}

class ModuleLintSigning(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=WIP
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
                self.assertIn(KEY, pinfo[2])

