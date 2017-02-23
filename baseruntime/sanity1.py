#!/usr/bin/python

import socket
from avocado import main
from avocado.core import exceptions
import moduleframework

class SanityCheck1(moduleframework.AvocadoTest):
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
        if "gcc" not in self.getActualProfile():
            raise exceptions.TestDecoratorSkip("gcc is not installed")
        self.start()
        self.run("gcc -v")

if __name__ == '__main__':
    main()
    
    
