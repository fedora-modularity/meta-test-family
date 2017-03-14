#!/usr/bin/python

from avocado import main
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

class SanityCheckCopyFiles(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test1(self):
        self.start()
        self.runHost("touch a")
        self.copyTo("a", "/a.test")
        self.run("ls /a.test")
        self.run("echo x > a.test")
        self.copyFrom("/a.test", "b")
        self.runHost("grep x b")

if __name__ == '__main__':
    main()
