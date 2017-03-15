#!/usr/bin/python

from moduleframework import module_framework
from avocado import skipIf

class SkipTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testGccSkipped(self):
        module_framework.skipTestIf("gcc" not in self.getActualProfile())
        self.start()
        self.run("gcc -v")

    @skipIf(module_framework.get_correct_profile()=="gcc")
    def testDecoratorSkip(self):
        self.start()
        self.run("gcc -v")
