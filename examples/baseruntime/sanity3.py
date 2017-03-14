#!/usr/bin/python

from avocado import main
from moduleframework import module_framework


class SanityCheck1(module_framework.AvocadoTest):
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

if __name__ == '__main__':
    main()
