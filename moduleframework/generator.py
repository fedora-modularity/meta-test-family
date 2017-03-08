#!/usr/bin/python

from moduleframework.moduleframework import CommonFunctions


class TestGenerator(CommonFunctions):

    def __init__(self):
        self.loadconfig()
        self.output = ""
        self.templateClassBefore()
        if 'test' in self.config:
            for testname in self.config['test']:
                self.templateTest(testname, self.config['test'][testname])
        if 'testhost' in self.config:
            for testname in self.config['testhost']:
                self.templateTest(
                    testname,
                    self.config['testhost'][testname],
                    method="runHost")

    def templateClassBefore(self):
        self.output = """#!/usr/bin/python

import socket
from avocado import main
from moduleframework import moduleframework

if __name__ == '__main__':
    main()

class GeneratedTestsConfig(moduleframework.AvocadoTest):
    \"\"\"
    :avocado: enable
    \"\"\"
"""

    def templateTest(self, testname, testlines, method="run"):
        self.output = self.output + """
    def test_%s(self):
        self.start()
""" % testname
        for line in testlines:
            self.output = self.output + \
                """        self.%s("%s")\n""" % (method, line)
        print "Added test (runmethod: %s): %s" % (method, testname)

if __name__ == '__main__':
    config = TestGenerator()
    configout = open('generated.py', 'w')
    configout.write(config.output)
    configout.close()
