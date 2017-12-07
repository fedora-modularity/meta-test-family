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
import time
import urllib


class SimpleTests(module_framework.ContainerAvocadoTest):
    """
    :avocado: enable
    """
    ip_address = module_framework.trans_dict["GUESTIPADDR"]
    port = "8080"

    def life_check(self, ip_address=None, port=None, textcheck="Hello from gunicorn WSGI application!"):
        ip_address = ip_address or self.ip_address
        port = port or self.port
        # wait until container initialized (without probe)
        time.sleep(3)
        urlfd = urllib.urlopen("http://%s:%s" % (ip_address, port))
        self.assertIn(textcheck, urlfd.read())
        urlfd.close()

    def test_basic(self):
        self.start()
        self.life_check()

    def test_via_curl(self):
        self.start()
        self.life_check()
        output = self.runHost("curl http://%s:%s" % (self.ip_address, self.port))
        self.assertIn("Hello from gunicorn WSGI application!", output.stdout)

    def test_another_port(self):
        self.backend.info["start"]="docker run -p 9999:8080"
        self.start()
        self.life_check(port="9999")


class UsageTest(module_framework.ContainerAvocadoTest):
    """
    :avocado: enable
    """
    messages = ["This is a S2I python-", "To use it, install S2I: https://github.com/openshift/source-to-image"]

    def test_usage(self):
        usage_com = self.runHost("s2i usage %s" % self.backend.getDockerInstanceName())
        for message in self.messages:
            self.assertIn(message, usage_com.stdout)
