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

import socket
from avocado import main
from avocado.core import exceptions
from moduleframework import module_framework


class SanityCheck1(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test1(self):
        self.start()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', self.getConfig()['service']['port']))
        s.sendall('set Test 0 100 4\r\n\n')
        #data = s.recv(1024)
        # print data

        s.sendall('get Test\r\n')
        #data = s.recv(1024)
        # print data
        s.close()

    def test2(self):
        self.start()
        self.run("ls / | grep bin")

    def test3GccSkipped(self):
        module_framework.skipTestIf("gcc" not in self.getActualProfile())
        self.start()
        self.run("gcc -v")


if __name__ == '__main__':
    main()
