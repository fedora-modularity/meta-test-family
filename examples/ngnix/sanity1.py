#!/usr/bin/python

from moduleframework import module_framework
import time
import urllib

class SanityCheck1(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testGetCurl(self):
        self.start()
        time.sleep(2)
        self.runHost("curl http://localhost:80")

    def testGetUrllib(self):
        self.start()
        time.sleep(2)
        fh = urllib.urlopen("http://localhost:80")
        print fh.readlines()
