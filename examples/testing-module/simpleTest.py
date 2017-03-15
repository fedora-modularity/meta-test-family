#!/usr/bin/python

from moduleframework import module_framework
import os


class simpleTests(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testPath(self):
        print ">>>>>>>>>>>>>> ", module_framework.__file__
        print ">>>>>>>>>>>>>> ", __file__
        self.assertIn(os.path.dirname(__file__), os.path.dirname(module_framework.__file__))

    def testAssertIn(self):
        self.start()
        self.assertIn("sbin", self.run("ls /").stdout)

    def testInsideModule(self):
        self.start()
        self.assertEqual("a", self.run("echo a").stdout.strip())

    def testCommandOnHost(self):
        self.start()
        self.assertEqual("a", self.runHost("echo a").stdout.strip())
