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
# Authors: Petr Hracek <phracek@redhat.com>
#

from moduleframework.module_framework import AvocadoTest
from moduleframework.common import get_module_type_base


# INTERFACE CLASSES FOR SPECIFIC MODULE TESTS
class ContainerAvocadoTest(AvocadoTest):
    """
    Class for writing tests specific just for DOCKER
    derived from AvocadoTest class.

    :avocado: disable
    """

    def setUp(self):
        if get_module_type_base() != "docker":
            self.cancel("Docker specific test")
        super(ContainerAvocadoTest, self).setUp()

    def checkLabel(self, key, value):
        """
        check label of docker image, expect key value (could be read from config file)

        :param key: str
        :param value: str
        :return: bool
        """
        if key in self.backend.containerInfo['Labels'] and (
                    value in self.backend.containerInfo['Labels'][key]):
            return True
        return False


