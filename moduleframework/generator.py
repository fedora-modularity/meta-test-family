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

from moduleframework.module_framework import CommonFunctions


class TestGenerator(CommonFunctions):

    def __init__(self):
        self.loadconfig()
        self.output = ""
        self.templateClassBefore()
        if 'test' in self.config:
            for testname in self.config['test']:
                self.templateTest(testname, self.config['test'][testname])
        if 'testhost' in self.config:
            for testname in self.config['testhost']:
                self.templateTest(
                    testname,
                    self.config['testhost'][testname],
                    method="runHost")

    def templateClassBefore(self):
        self.output = """#!/usr/bin/python

import socket
from avocado import main
from moduleframework import module_framework

if __name__ == '__main__':
    main()

class GeneratedTestsConfig(module_framework.AvocadoTest):
    \"\"\"
    :avocado: enable
    \"\"\"
"""

    def templateTest(self, testname, testlines, method="run"):
        self.output = self.output + """
    def test_%s(self):
        self.start()
""" % testname
        for line in testlines:
            self.output = self.output + \
                """        self.%s("%s")\n""" % (method, line.replace('"', r'\"'))
        print "Added test (runmethod: %s): %s" % (method, testname)


def main():
    config = TestGenerator()
    configout = open('generated.py', 'w')
    configout.write(config.output)
    configout.close()

if __name__ == '__main__':
    main()
