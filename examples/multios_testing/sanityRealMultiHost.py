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

from avocado import main
from moduleframework import module_framework

TFILE = "/tmp/testfile"


class SanityRealMultihost(module_framework.AvocadoTest):
    """
    :avocado: enable
    """
    def setUp(self):
        #self.machineF25 = module_framework.get_backend()
        self.machineF26 = module_framework.get_backend()
        self.machineRawhide = module_framework.get_backend()
        #self.machineF25.info["url"] = ["http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/25/Everything/x86_64/os/"]
        self.machineF26.info["url"] = ["http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/26/Everything/x86_64/os/"]
        self.machineRawhide.info["url"] = ["http://ftp.fi.muni.cz/pub/linux/fedora/linux/development/rawhide/Everything/x86_64/os/"]
        #self.machineF25.setUp()
        self.machineF26.setUp()
        self.machineRawhide.setUp()

    def tearDown(self):
        #self.machineF25.tearDown()
        self.machineF26.tearDown()
        self.machineRawhide.tearDown()


    def testVersionsInside(self):
        #self.machineF25.start()
        self.machineF26.start()
        self.machineRawhide.start()
        #self.assertIn("25", self.machineF25.run("cat /etc/redhat-release").stdout)
        self.assertIn("26", self.machineF26.run("cat /etc/redhat-release").stdout)
        self.assertIn("awhide", self.machineRawhide.run("cat /etc/redhat-release").stdout)


if __name__ == '__main__':
    main()
