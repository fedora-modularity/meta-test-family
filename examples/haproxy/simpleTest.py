#!/usr/bin/python

from moduleframework import module_framework
import os


class simpleTests(module_framework.AvocadoTest):
    """
    :avocado: enable
    """
    def setUp(self):
        super(self.__class__, self).setUp()
        self.runHost('docker pull docker.io/httpd')
        self.runHost('docker run --name http_name_8000 -d -p 8000:80 docker.io/httpd')
        self.runHost('docker run --name http_name_8001 -d -p 8001:80 docker.io/httpd')
        global myip
        myip = self.runHost('hostname -i').stdout.strip()

    def tearDown(self):
        super(self.__class__, self).tearDown()
        self.runHost('docker stop http_name_8000')
        self.runHost('docker stop http_name_8001')
        self.runHost('docker rm http_name_8000')
        self.runHost('docker rm http_name_8001')

    def testAssertIn(self):
        self.runHost(('sed s/127.0.0.1/{}/ my-haproxy.cfg > local-haproxy.cfg').format(myip), shell = True)
        self.start()
        self.assertIn('It works!',self.runHost('curl localhost:8077', shell = True).stdout)

