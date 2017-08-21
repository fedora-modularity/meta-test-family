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
import os

from moduleframework import module_framework
from moduleframework import dockerlinter


class DockerfileLinter(module_framework.AvocadoTest):
    """
    :avocado: enable

    """

    dp = None

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        self.dp = dockerlinter.DockerfileLinter(os.path.join(os.getcwd(), ".."))
        if self.dp.dockerfile is None:
            self.skip()

    def testDockerFromBaseruntime(self):
        self.assertTrue(self.dp.check_baseruntime())

    def testDockerRunMicrodnf(self):
        self.assertTrue(self.dp.check_microdnf())

    def testArchitectureInEnvAndLabelExists(self):
        self.assertTrue(self.dp.get_docker_specific_env("ARCH="))
        self.assertTrue(self.dp.get_specific_label("architecture"))

    def testNameInEnvAndLabelExists(self):
        self.assertTrue(self.dp.get_docker_specific_env("NAME="))
        self.assertTrue(self.dp.get_specific_label("name"))

    def testReleaseLabelExists(self):
        self.assertTrue(self.dp.get_specific_label("release"))

    def testVersionLabelExists(self):
        self.assertTrue(self.dp.get_specific_label("version"))

    def testComRedHatComponentLabelExists(self):
        self.assertTrue(self.dp.get_specific_label("com.redhat.component"))

    def testIok8sDescriptionExists(self):
        self.assertTrue(self.dp.get_specific_label("io.k8s.description"))

    def testIoOpenshiftExposeServicesExists(self):
        label_io_openshift = "io.openshift.expose-services"
        exposes = self.dp.get_docker_expose()
        label_list = self.dp.get_docker_labels()
        self.assertTrue(label_list[label_io_openshift])
        for exp in exposes:
            self.assertTrue("%s" % exp in label_list[label_io_openshift])

    def testIoOpenShiftTagsExists(self):
        label_list = self.dp.get_docker_labels()
        self.assertTrue("io.openshift.tags" in label_list)


class DockerLint(module_framework.ContainerAvocadoTest):
    """
    :avocado: enable
    """

    def testBasic(self):
        self.start()
        self.assertTrue("bin" in self.run("ls /").stdout)

    def testContainerIsRunning(self):
        """
        Function tests whether container is running
        :return:
        """
        self.start()
        self.assertIn(self.backend.jmeno.rsplit("/")[-1], self.runHost("docker ps").stdout)

    def testLabels(self):
        """
        Function tests whether labels are set in modulemd YAML file properly.
        :return:
        """
        llabels = self.getConfigModule().get('labels')
        if llabels is None or len(llabels) == 0:
            print("No labels defined in config to check")
            self.cancel()
        for key in self.getConfigModule()['labels']:
            aaa = self.checkLabel(key, self.getConfigModule()['labels'][key])
            print(">>>>>> ", aaa, key)
            self.assertTrue(aaa)


class ModuleLintSigning(module_framework.AvocadoTest):
    """
    :avocado: disable
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


class ModuleLintPackagesCheck(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test(self):
        self.start()
        allpackages = [
            x.strip()
            for x in self.run(r'rpm -qa --qf="%{{name}}\n"').stdout.split('\n')]
        for pkg in self.backend.getPackageList():
            self.assertIn(pkg, allpackages)
