#!/usr/bin/python

import inspect
import moduleframework
from avocado import utils
from avocado import main

class DockerLint(moduleframework.AvocadoTest):
    """
    :avocado: enable
    """
    def setUp(self):
        if moduleframework.MODULE != "docker":
            self.skip("Docker specific test")
        super(DockerLint, self).setUp()


    def testBasic(self):
        self.start()
        self.assertTrue("bin" in self.run("ls /").stdout)

    def testLabels(self):
        for key in self.info['labels']:
            aaa = self.checkLabel(key, self.info['labels'][key])
            self.log.debug(aaa, key, self.info['labels'][key])
            self.assertTrue(aaa)


class ModuleLint(moduleframework.AvocadoTest):
    """
    :avocado: enable
    """
    def testPackages(self):
        RHKEY = "fd431d51"
        FEDKEY = "73bde98381b46521"
        KEY = FEDKEY
        self.start()
        allpackages = self.run(r'rpm -qa --qf="%{name}-%{version}-%{release} %{SIGPGP:pgpsig}\n"').stdout
        for package in allpackages.split('\n'):
            pinfo = package.split(', ')
            if len(pinfo)==3:
                if KEY not in pinfo[2]:
                    print "FAIL", pinfo[0]
                else:
                    print "PASS", pinfo[0]

if __name__ == '__main__':
    main()
