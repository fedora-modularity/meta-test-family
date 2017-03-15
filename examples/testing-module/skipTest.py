#!/usr/bin/python

from moduleframework import module_framework
from avocado import skipIf
from avocado import skipUnless

class SkipTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testGccSkippedInsideTest(self):
        # rewrite it to calling cancell, it was not in production of avocado, but it is fixed.
        module_framework.skipTestIf("gcc" not in self.getActualProfile())
        self.start()
        self.run("gcc -v")

    @skipIf(module_framework.get_correct_profile() == "default")
    def testDecoratorNotSkippedForDefault(self):
        self.start()
        self.run("echo for default profile")


    @skipUnless(module_framework.get_correct_profile() == "gcc")
    def testDecoratorSkip(self):
        self.start()
        self.run("gcc -v")

