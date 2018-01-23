# -*- coding: utf-8 -*-
#
# Meta test family (MTF) is a tool to test components of a modular Fedora:
# https://docs.pagure.org/modularity/
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copied from: https://github.com/fedora-modularity/module-tests/blob/master/rpmvalidation.py
#
# Authors: Stephen Gallagher <sgallagh@redhat.com>
#          Jan Scotka <jscotka@redhat.com>
#


from moduleframework import module_framework
from moduleframework import common


class rpmvalidation(module_framework.AvocadoTest):
    """
    Provide a list of acceptable file paths based on
    http://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html
    
    :avocado: enable
    :avocado: tags=sanity,rhel,fedora,docker,module,rpmvalidation_test,generic
    """
    fhs_base_paths_workaound = [
        '/var/kerberos',
        '/var/db'
    ]
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
    ] + fhs_base_paths_workaound

    def _compare_fhs(self, filepath):
        if '(contains no files)' in filepath or filepath in self.fhs_base_paths:
            self.log.info("no files there (trivial case), or this is filesystem package")
            return True
        for path in self.fhs_base_paths:
            if filepath.startswith(path):
                self.log.info("%s starts with FSH %s" % (filepath, path))
                return True
        self.log.info("%s not found in %s" % (filepath, self.fhs_base_paths))
        return False

    def testPaths(self):
        self.start()
        allpackages = filter(bool, self.run("rpm -qa").stdout.split("\n"))
        common.print_debug(allpackages)
        for package in allpackages:
            if 'filesystem' in package:
                continue
            for package_file in filter(bool, self.run("rpm -ql %s" % package).stdout.split("\n")):
                if not self._compare_fhs(package_file):
                    self.fail("(%s): File [%s] violates the FHS." % (package, package_file))
