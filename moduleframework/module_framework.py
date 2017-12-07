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

"""
main module provides helpers for various module types and AVOCADO(unittest) classes
what you should use for your tests (inherited)
"""

from moduleframework.avocado_testers.avocado_test import AvocadoTest, get_backend
from moduleframework.avocado_testers.container_avocado_test import ContainerAvocadoTest
from moduleframework.avocado_testers.nspawn_avocado_test import NspawnAvocadoTest
from moduleframework.avocado_testers.rpm_avocado_test import RpmAvocadoTest
from moduleframework.avocado_testers.openshift_avocado_test import OpenShiftAvocadoTest
from moduleframework.mtfexceptions import ModuleFrameworkException

PROFILE = None


def skipTestIf(value, text="Test not intended for this module profile"):
    """
    function what solves troubles that it is not possible to call SKIP inside code
    You can use avocado decorators, it is preferred way.

    :param value: Boolean what is used for decision in case of True
    :param text: Error text what to raise
    :return: None
    """
    if value:
        raise ModuleFrameworkException(
            "DEPRECATED, don't use this skip, use self.cancel() inside test function, or self.skip() in setUp()")
