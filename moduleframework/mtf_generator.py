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
# Authors: Jan Scotka <jscotka@redhat.com>
#

from __future__ import print_function

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
            # only use shell=True for runHost() calls, otherwise variables etc.
            # get expanded too early, i.e. on the host
            self.output = self.output + \
                '        self.%s(""" %s """,  shell=%r)\n' % (
                    method, line, method == "runHost")
        print("Added test (runmethod: %s): %s" % (method, testname))


def main():
    config = TestGenerator()
    configout = open('generated.py', 'w')
    configout.write(config.output)
    configout.close()

if __name__ == '__main__':
    main()
