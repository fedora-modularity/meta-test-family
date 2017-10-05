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
from moduleframework.avocado_testers import container_avocado_test


class DockerFileLinter(module_framework.AvocadoTest):
    """
    :avocado: enable

    """

    dp = None

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        self.dp = dockerlinter.DockerfileLinter()
        if self.dp.dockerfile is None:
            self.skip()

    def test_architecture_in_env_and_label_exists(self):
        self.assertTrue(self.dp.get_docker_specific_env("ARCH="))
        self.assertTrue(self.dp.get_specific_label("architecture"))

    def test_name_in_env_and_label_exists(self):
        self.assertTrue(self.dp.get_docker_specific_env("NAME="))
        self.assertTrue(self.dp.get_specific_label("name"))

    def test_maintainer_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("maintainer"))

    def test_release_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("release"))

    def test_version_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("version"))

    def test_com_redhat_component_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("com.redhat.component"))

    def test_summary_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("summary"))

    def test_run_or_usage_label_exists(self):
        label_found = True
        run = self.dp.get_specific_label("run")
        if not run:
            label_found = self.dp.get_specific_label("usage")
        self.assertTrue(label_found)

    def test_from_is_first_directive(self):
        self.assertTrue(self.dp.check_from_is_first())

    def test_from_correct_format(self):
        self.assertTrue(self.dp.check_from_format())


class DockerLint(container_avocado_test.ContainerAvocadoTest):
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
