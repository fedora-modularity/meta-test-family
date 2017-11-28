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


class NspawnAvocadoTest(AvocadoTest):
    """
    Class for writing tests specific just for RPM module testing inside NSPAWN env
    derived from AvocadoTest class.

    :avocado: disable
    """

    def setUp(self):
        if get_module_type_base() != "nspawn":
            self.cancel("Nspawn specific test")
        super(NspawnAvocadoTest, self).setUp()


