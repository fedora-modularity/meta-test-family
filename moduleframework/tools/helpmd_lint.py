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
from moduleframework import helpfile_linter
from moduleframework import dockerlinter
from moduleframework import module_framework
from moduleframework.common import get_docker_file


class HelpMDLinter(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=docker,fedora,rhel,optional

    """

    dp = None

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        self.dp = dockerlinter.DockerfileLinter()
        if self.dp.dockerfile is None:
            dir_name = os.getcwd()
            self.log.info("Dockerfile was not found in %s directory." % dir_name)
            self.skip()
        self.helpmd = helpfile_linter.HelpMDLinter(dockerfile=self.dp.dockerfile)
        if self.helpmd is None:
            self.log.info("help.md file was not found in Dockerfile directory")
            self.skip()

    def test_helpmd_exists(self):
        self.assertTrue(self.helpmd)

    def test_helpmd_image_name(self):
        container_name = self.dp.get_docker_specific_env("NAME=")
        if container_name:
            self.assertTrue(self.helpmd.get_image_name(container_name[0].split('=')[1]))
        else:
            self.cancel()

    def test_helpmd_maintainer_name(self):
        maintainer_name = self.dp.get_specific_label("maintainer")
        if maintainer_name:
            self.assertTrue(self.helpmd.get_maintainer_name(maintainer_name[0]))
        else:
            self.cancel()

    def test_helpmd_name(self):
        self.assertTrue(self.helpmd.get_tag("NAME"))

    def test_helpmd_description(self):
        self.assertTrue(self.helpmd.get_tag("DESCRIPTION"))

    def test_helpmd_usage(self):
        self.assertTrue(self.helpmd.get_tag("USAGE"))

    def test_helpmd_environment_variables(self):
        env_variables = self.helpmd.get_tag("ENVIRONMENT VARIABLES")
        if not env_variables:
            self.log.warn("help.md file does not contain section ENVIRONMENT VARIABLES")
        # In order to report warning, test has to report with True always
        self.assertTrue(True)

    def test_helpmd_security_implications(self):
        if self.dp.get_docker_expose():
            self.assertTrue(self.helpmd.get_tag("SECURITY IMPLICATIONS"))
        else:
            self.cancel()
