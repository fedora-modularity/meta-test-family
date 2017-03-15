#!/usr/bin/python

from moduleframework import module_framework


class CheckCopyFiles(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testCopyThereAndBack(self):
        self.start()
        self.runHost("echo x > a", shell=True)
        self.copyTo("a", "/a.test")
        self.run("ls /a.test")
        self.copyFrom("/a.test", "b")
        self.runHost("grep x b")
