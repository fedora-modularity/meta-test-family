#!/usr/bin/python

from avocado import main
from moduleframework import module_framework


class ExampleRpmValidation(module_framework.AvocadoTest):
    """
    :avocado: enable
    """
    fhs_base_paths = [
        '/bin',
        '/boot',
        '/dev',
        '/etc',
        '/home',
        '/lib',
        '/lib64',
        '/media',
        '/mnt',
        '/opt',
        '/proc',
        '/root',
        '/run',
        '/sbin',
        '/sys',
        '/srv',
        '/tmp',
        '/usr/bin'
    ]

    def testPaths(self):
        self.start()
        for directory in self.fhs_base_paths:
            self.run("test -d %s" % directory)
