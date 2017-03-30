#!/usr/bin/python

import inspect
from moduleframework import module_framework
from avocado import utils
from avocado import main


class DockerLint(module_framework.ContainerAvocadoTest):
    """
    :avocado: enable
    """


    def testBasic(self):
        self.start()
        self.assertTrue("bin" in self.run("ls /").stdout)

    def testContainerIsRunning(self):
        self.start()
        self.assertIn(self.backend.jmeno, self.runHost("docker ps").stdout)

    def testLabels(self):
        llabels = self.getConfigModule().get('labels')
        module_framework.skipTestIf( llabels == None or len(llabels) == 0, "No labels defined in config to check")
        for key in self.getConfigModule()['labels']:
            aaa = self.checkLabel(key, self.getConfigModule()['labels'][key])
            print ">>>>>> ", aaa, key
            self.assertTrue(aaa)



class ModuleLintSigning(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=WIP
    """
    def setUp(self):
        # it is not intended just for docker, but just docker packages are actually properly signed
        super(self.__class__, self).setUp()
        if self.moduleType != "docker":
            self.skip("Docker specific test")

    def test(self):
        RHKEY = "fd431d51"
        FEDKEY = "73bde98381b46521"
        KEY = FEDKEY
        self.start()
        allpackages = self.run(
            r'rpm -qa --qf="%{name}-%{version}-%{release} %{SIGPGP:pgpsig}\n"').stdout
        for package in allpackages.split('\n'):
            pinfo = package.split(', ')
            if len(pinfo) == 3:
                self.assertIn(KEY, pinfo[2])

class ModuleLintPackagesCheck(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test(self):
        self.start()
        allpackages = self.run(r'rpm -qa --qf="%{name}\n"').stdout.split('\n')
        for pkg in self.backend.packages:
            self.assertIn(pkg, allpackages)


if __name__ == '__main__':
    main()
