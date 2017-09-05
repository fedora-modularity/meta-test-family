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
# Authors: Jan Scotka <jscotka@redhat.com>
#

from moduleframework import module_framework


class SanityCheckApostophes(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testSimpleShell(self):
        self.start()
        self.run("ls /| grep bin")

    def testApostrophesInside(self):
        self.start()
        self.run("echo 'a'")

    def testMoreLevelApostrophes(self):
        self.start()
        self.run("""bash -c 'echo "echo under bash"' """)

    def testStderr(self):
        self.start()
        x = self.run("echo a; echo b >&2; exit 1", ignore_status=True)
        self.assertEqual("a", x.stdout.strip())
        self.assertEqual("b", x.stderr.strip())
        self.assertEqual(1, x.exit_status)
