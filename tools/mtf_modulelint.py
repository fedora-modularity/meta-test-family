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
# Copied from: https://github.com/fedora-modularity/check_compose/blob/master/check_compose.py
#
# Authors: Jan Scotka <jscotka@redhat.com>
#
# TODO: This is not working now, because it is still not  implemented in upsteram avocado:
# TODO: https://github.com/avocado-framework/avocado/issues/1792

from moduleframework.tests.generic.check_compose import ComposeTest
from moduleframework.tests.generic.rpmvalidation import rpmvalidation
from moduleframework.tests.generic.modulelint import *
from moduleframework.tests.generic.dockerlint import *
from moduleframework.tests.static.dockerfile_lint import *

class MTFComposeTest(ComposeTest):
    """
    :avocado: recursive
    """
    pass


class MTFRpmValidation(rpmvalidation):
    """
    :avocado: recursive
    """
    pass


class MTFDockerFileLinter(DockerfileLinterInContainer):
    """
    :avocado: recursive
    """
    pass


class MTFDockerLinter(DockerLint):
    """
    :avocado: recursive
    """
    pass

class MTFModuleLintSigning(ModuleLintSigning):
    """
    :avocado: recursive
    """
    pass

class MTFModuleLintPackagesCheck(ModuleLintPackagesCheck):
    """
    :avocado: recursive
    """
    pass
