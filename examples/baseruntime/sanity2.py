#!/usr/bin/python

from avocado import main
from moduleframework import module_framework


class RpmValidation(module_framework.AvocadoTest):
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
        '/usr/bin',
        '/usr/include',
        '/usr/lib',
        '/usr/libexec',
        '/usr/lib64',
        '/usr/local',
        '/usr/sbin',
        '/usr/share',
        '/usr/src',
        '/var/account',
        '/var/cache',
        '/var/crash',
        '/var/games',
        '/var/lib',
        '/var/lock',
        '/var/log',
        '/var/mail',
        '/var/opt',
        '/var/run',
        '/var/spool',
        '/var/tmp',
        '/var/yp'
    ]

    def testPaths(self):
        self.start()
        for directory in self.fhs_base_paths:
            self.run("test -d %s" % directory)

if __name__ == '__main__':
    main()
