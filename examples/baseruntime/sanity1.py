#!/usr/bin/python

from avocado import main
from moduleframework import module_framework


class SanityCheck1(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test1echo(self):
        self.start()
        self.assertIn("AHOJ", self.run("echo AHOJ").stdout)

    def test2ls(self):
        self.start()
        self.assertIn("sbin", self.run("ls /").stdout)

    def test3GccSkipped(self):
        module_framework.skipTestIf("gcc" not in self.getActualProfile())
        self.start()
        self.run("gcc -v")

    def test4failedCommand(self):
        self.start()
        self.runCheckState("ls /abc",2)


if __name__ == '__main__':
    main()
