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

from moduleframework import helpfile_linter
from moduleframework import dockerlinter
from moduleframework import module_framework


class HelpFileSanity(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=optional,rhel,fedora,docker,helpmd_sanity_test,static

    """

    helpmd = None
    dp = None

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        self.helpmd = helpfile_linter.HelpMDLinter()
        self.dp = dockerlinter.DockerfileLinter()
        if self.helpmd.help_md is None or self.dp.dockerfile is None:
            self.cancel("Help file or Dockerfile was not found")

    def tearDown(self, *args, **kwargs):
        pass

    def _get_msg(self, msg):
        return msg + " is missing in help file."

    def test_helpmd_image_name(self):
        container_name = self.dp.get_docker_specific_env("NAME=")
        if container_name:
            self.assertTrue(self.helpmd.get_image_name(container_name[0].split('=')[1]),
                            msg="%s The correct format is %% MEMCACHED(1)" % self._get_msg("Image name"))

    def test_helpmd_maintainer_name(self):
        maintainer_name = self.dp.get_specific_label("maintainer")
        if maintainer_name:
            self.assertTrue(self.helpmd.get_maintainer_name(maintainer_name[0]),
                            msg="%s The correct format is '%% User Name'. Or you have a typo in the help file." % self._get_msg("maintainer"))

    def test_helpmd_name(self):
        self.assertTrue(self.helpmd.get_tag("NAME"),
                        msg=self._get_msg("NAME section"))

    def test_helpmd_description(self):
        self.assertTrue(self.helpmd.get_tag("DESCRIPTION"),
                        msg=self._get_msg("DESCRIPTION section"))

    def test_helpmd_usage(self):
        self.assertTrue(self.helpmd.get_tag("USAGE"),
                        msg=self._get_msg("USAGE section"))

    def test_helpmd_environment_variables(self):
        self.assert_to_warn(self.assertTrue, self.helpmd.get_tag("ENVIRONMENT VARIABLES"),
                            msg=self._get_msg("ENVIRONMENT VARIABLES section"))

    def test_helpmd_security_implications(self):
        if self.dp.get_docker_expose():
            self.assertTrue(self.helpmd.get_tag("SECURITY IMPLICATIONS"),
                            msg=self._get_msg("SECURITY IMPLICATIONS section"))
