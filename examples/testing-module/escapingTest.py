#!/usr/bin/python

from moduleframework import module_framework

class SanityCheckApostophes(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test1(self):
        self.start()
        self.run("ls /| grep bin")

    def test2(self):
        self.start()
        self.run("echo 'a'")

    def test3(self):
        self.start()
        self.run("""su - -c 'echo "echo under root"' """)
