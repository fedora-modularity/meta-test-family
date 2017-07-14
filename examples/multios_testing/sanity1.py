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

import time
from avocado import main
from moduleframework import module_framework

TFILE="/tmp/testfile"

class SanityCheck1(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testServerInside(self):
        PORT = 3333
        self.start()
        self.assertIn("AHOJ", self.run("echo AHOJ").stdout)
        self.run(" nohup nc -l %d > %s 2>&1 &" % (PORT, TFILE), shell=True, ignore_bg_processes=True)
        time.sleep(2)
        a = self.runHost("cat /etc/redhat-release").stdout.strip()
        self.runHost("cat /etc/redhat-release | nc localhost %d" % PORT, shell=True)
        time.sleep(2)
        b = self.run("cat %s" %TFILE).stdout.strip()
        self.assertEqual(a,b)
        self.assertIn("26", b)



    def testServerOutside(self):
        PORT = 4444
        self.start()
        self.assertIn("AHOJ", self.runHost("echo AHOJ").stdout)
        self.runHost("nohup nc -l %d > %s 2>&1 &" % (PORT, TFILE), shell=True, ignore_bg_processes=True)
        time.sleep(2)
        a = self.run("cat /etc/redhat-release").stdout.strip()
        self.run("cat /etc/redhat-release | nc localhost %d" % PORT, shell=True)
        time.sleep(2)
        b = self.runHost("cat %s" %TFILE).stdout.strip()
        self.assertEqual(a,b)
        self.assertIn("26", b)

if __name__ == '__main__':
    main()
