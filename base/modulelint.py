#!/usr/bin/python

import inspect
import moduleframework
from avocado import utils
from avocado import main

class DockerLint(moduleframework.ContainerAvocadoTest):
    """
    :avocado: enable
    """
    def setUp(self):
        if self.moduleType != "docker":
            self.skip("Docker specific test")
        super(DockerLint, self).setUp()

    def testBasic(self):
        self.start()
        self.assertTrue("bin" in self.run("ls /").stdout)

    def testLabels(self):
        for key in self.getConfigModule()['labels']:
            print ">>>>>> ",  key
            aaa = self.checkLabel(key, self.getConfigModule()['labels'][key])
            self.log.debug(aaa, key, self.getConfigModule()['labels'][key])
            self.assertTrue(aaa)


class ModuleLint(moduleframework.AvocadoTest):
    """
    :avocado: enable
    """
    def testPackagesSign(self):
        RHKEY = "fd431d51"
        FEDKEY = "73bde98381b46521"
        KEY = FEDKEY
        self.start()
        allpackages = self.run(r'rpm -qa --qf="%{name}-%{version}-%{release} %{SIGPGP:pgpsig}\n"').stdout
        for package in allpackages.split('\n'):
            pinfo = package.split(', ')
            if len(pinfo)==3:
                self.assertIn(KEY,pinfo[2])

    def testPackagesRpms(self):
        self.start()
        allpackages = self.run(r'rpm -qa --qf="%{name}\n"').stdout.split('\n')
        for pkg in self.backend.packages:
            self.assertIn(pkg,allpackages)

if __name__ == '__main__':
    main()
