How to use Meta Test Family in real examples
============================================

Read <environment_setup.rst> and <how_to_write_conf_file> before playing with these examples.
There is set of real examples how to use MTF. Makefile does not need to be changed.
If something is different, it is mentioned.

How to start to two containers
------------------------------

This example shows you how to start two containers with MTF.

.. code-block:: python
from avocado import main
from moduleframework import module_framework

TFILE = "/tmp/testfile"


class SanityRealMultihost(module_framework.AvocadoTest):
    """
    :avocado: enable
    """
    def setUp(self):
        self.machineF25 = module_framework.get_backend()[0]
        self.machineF26 = module_framework.get_backend()[0]
        self.machineRawhide = module_framework.get_backend()[0]
        self.machineF25.info["repo"] = "http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/25/Everything/x86_64/os/"
        self.machineF26.info["repo"] = "http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/26/Everything/x86_64/os/"
        self.machineRawhide.info["repo"] = "http://ftp.fi.muni.cz/pub/linux/fedora/linux/development/rawhide/Everything/x86_64/os/"
        self.machineF25.setUp()
        self.machineF26.setUp()
        self.machineRawhide.setUp()

    def tearDown(self):
        self.machineF25.tearDown()
        self.machineF26.tearDown()
        self.machineRawhide.tearDown()


    def testVersionsInside(self):
        self.machineF25.start()
        self.machineF26.start()
        self.machineRawhide.start()
        self.assertIn("25", self.machineF25.run("cat /etc/redhat-release").stdout)
        self.assertIn("26", self.machineF26.run("cat /etc/redhat-release").stdout)
        self.assertIn("awhide", self.machineRawhide.run("cat /etc/redhat-release").stdout)


if __name__ == '__main__':
main()



