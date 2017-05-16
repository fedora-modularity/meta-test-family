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


class DockerLint(module_framework.ContainerAvocadoTest):
    """
    :avocado: enable
    """

    def testBasic(self):
        self.start()
        self.assertTrue("bin" in self.run("ls /").stdout)

    def testContainerIsRunning(self):
        self.start()
        self.assertIn(self.backend.jmeno, self.runHost("docker ps").stdout)

    def testLabels(self):
        llabels = self.getConfigModule().get('labels')
        module_framework.skipTestIf(
            llabels is None or len(llabels) == 0,
            "No labels defined in config to check")
        for key in self.getConfigModule()['labels']:
            aaa = self.checkLabel(key, self.getConfigModule()['labels'][key])
            print ">>>>>> ", aaa, key
            self.assertTrue(aaa)


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
            r'rpm -qa --qf="%{name}-%{version}-%{release} %{SIGPGP:pgpsig}\n"').stdout
        for package in [x.strip() for x in allpackages.split('\n')]:
            pinfo = package.split(', ')
            if len(pinfo) == 3:
                self.assertIn(KEY, pinfo[2])


class ModuleLintPackagesCheck(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test(self):
        self.start()
        allpackages = [
            x.strip()
            for x in self.run(r'rpm -qa --qf="%{name}\n"').stdout.split('\n')]
        for pkg in self.backend.getPackageList():
            self.assertIn(pkg, allpackages)
