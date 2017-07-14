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

from moduleframework import common
from moduleframework import module_framework
from avocado import skipIf
from avocado import skipUnless


class SkipTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testGccSkippedInsideTest(self):
        # rewrite it to calling cancell, it was not in production of avocado,
        # but it is fixed.
        if "gcc" not in self.getActualProfile():
            self.cancel()
        self.start()
        self.run("gcc -v")

    @skipIf(common.get_profile() == "default")
    def testDecoratorNotSkippedForDefault(self):
        self.start()
        self.run("echo for default profile")

    @skipUnless(common.get_profile() == "gcc")
    def testDecoratorSkip(self):
        self.start()
        self.run("gcc -v")
