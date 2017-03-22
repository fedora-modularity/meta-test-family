#!/usr/bin/python

from moduleframework import module_framework
from avocado import Test
from avocado import utils

class PureAvocadoTest(Test):
    def setUp(self):
        self.backend, self.moduletype = module_framework.get_correct_backend()
        self.backend.setUp()

    def testInsideModule(self):
        self.backend.start()
        self.backend.run("ls /")

    def testOnHost(self):
        utils.process.run("ls /")

    def tearDown(self):
        self.backend.tearDown()
