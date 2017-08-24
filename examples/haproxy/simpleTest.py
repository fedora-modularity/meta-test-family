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
# Authors: Petr Sklenar <psklenar@redhat.com>
#

from moduleframework import module_framework
import os
from avocado.utils import service


class simpleTests(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        service_manager = service.ServiceManager()
        service_manager.start('docker')
        self.runHost('docker pull docker.io/httpd')
        self.runHost(
            'docker run --name http_name_8000 -d -p 8000:80 docker.io/httpd')
        self.runHost(
            'docker run --name http_name_8001 -d -p 8001:80 docker.io/httpd')

    def tearDown(self):
        super(self.__class__, self).tearDown()
        self.runHost('docker stop http_name_8000')
        self.runHost('docker stop http_name_8001')
        self.runHost('docker rm http_name_8000')
        self.runHost('docker rm http_name_8001')

    def testAssertIn(self):
        self.start()
        self.assertIn(
            'It works!',
            self.runHost(
                'curl 127.0.0.1:8077',
                shell=True).stdout)
