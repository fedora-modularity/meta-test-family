#!/usr/bin/python
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
import glob
from moduleframework import module_framework
from avocado import utils


class Module(module_framework.CommonFunctions):

    whattoinstall = None
    baseruntimeyaml = None

    def __init__(self):
        self.loadconfig()
        self.yamlconfig = self.getModulemdYamlconfig()
        self.profile = module_framework.PROFILE if module_framework.PROFILE else "default"
        if self.yamlconfig:
            self.whattoinstall = self.yamlconfig['data']['profiles'][self.profile]
        self.rootdir = "/tmp/tmpmodule1"
        self.rpmsrepo = self.rootdir + "/rpms"
        self.rpmsinstalled = self.rootdir + "/installed"
        utils.process.run("mkdir -p %s" % self.rootdir)
        utils.process.run("mkdir -p %s" % self.rpmsrepo)
        utils.process.run("mkdir -p %s" % self.rpmsinstalled)
        self.baseruntimeyaml = self.getModulemdYamlconfig(
            "https://raw.githubusercontent.com/fedora-modularity/check_modulemd/develop/examples-modulemd/base-runtime.yaml")

    def CreateLocalRepo(self):
        allmodulerpms = None
        allbasertrpms = None
        if self.whattoinstall:
            allmodulerpms = " ".join(self.whattoinstall['rpms'])
        if self.baseruntimeyaml:
            allbasertrpms = " ".join(self.baseruntimeyaml['data'][
                'profiles']['default']['rpms'])
        if allbasertrpms is not None and allmodulerpms is not None:
            utils.process.run(
                "yumdownloader --destdir=%s --resolve %s %s" %
                (self.rpmsrepo, allmodulerpms, allbasertrpms))
        utils.process.run(
            "cd %s; createrepo --database %s" %
            (self.rpmsrepo, self.rpmsrepo), shell=True)
        print("file://%s" % self.rpmsrepo)

    def CreateContainer(self):
        localfiles = glob.glob('%s/*.rpm' % self.rpmsrepo)
        if localfiles and self.rpmsinstalled:
            utils.process.run(
                "dnf -y install --disablerepo=* --allowerasing --installroot=%s %s" %
                (self.rpmsinstalled, " ".join(localfiles)))
            print("file://%s" % self.rpmsrepo)


m = Module()
m.CreateLocalRepo()
m.CreateContainer()
