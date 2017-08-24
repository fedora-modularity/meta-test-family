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

from moduleframework import module_framework


class microDNFTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        if self.moduleType != "nspawn":
            try:
                self.tearDown()
            except Exception as e:
                print e
                pass
            self.skip("NSPAWN specific test (there is microdnf now)")

    def testInstallMicroDNFEmpty(self):
        self.start()
        self.run("microdnf install microdnf", ignore_status=True)
