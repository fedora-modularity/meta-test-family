#!/usr/bin/python

# this is template showed in tool mtf-init
# try mtf-init to create basic config.yaml
# start test by: "sudo mtf"

from avocado import main
from avocado.core import exceptions
from moduleframework import module_framework

class Smoke1(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test_uname(self):
        self.start()
        self.run("uname | grep Linux")

    def test_echo(self):
        self.start()
        self.runHost("echo test | grep test")

if __name__ == '__main__':
    main()
