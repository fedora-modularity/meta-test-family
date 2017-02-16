#!/usr/bin/python

import inspect
import moduleframework
from avocado import utils
from avocado import main

class ModuleLint(moduleframework.AvocadoTest):
    """
    :avocado: enable
    """
    def __init__(self, *args, **kwargs):
        super(ModuleLint, self).__init__(*args, **kwargs)
        methods = [x for x in inspect.getmembers(ModuleLint, predicate=inspect.ismethod) if 'Sanity' in x[0]]
        for parentfunc in methods:
            setattr(self, "test"+parentfunc[0], parentfunc[1])
            print  "test"+parentfunc[0], parentfunc[1]
            
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

    def Xtestinsideconfig(self):
        for key,value in self.config['test']:
            print key
            for line in lines:
                print ">>", line

if __name__ == '__main__':
    main()
