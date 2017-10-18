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
from avocado.utils import process
from tempfile import mktemp
import os

class remoteBinary(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test_outputs(self):
        self.start()
        scriptfile = mktemp()
        script="""#!/bin/bash
echo stdoutput
echo erroutput >&2
echo $@
        """
        with open(scriptfile, "w") as text_file:
            text_file.write(script)
        outputprocess = self.run_script(scriptfile)
        self.assertIn("stdoutput", outputprocess.stdout)
        self.assertIn("erroutput", outputprocess.stderr)
        outputprocess = self.run_script(scriptfile, "Hallo", "World")
        self.assertIn("stdoutput", outputprocess.stdout)
        self.assertIn("Hallo World", outputprocess.stdout)
        os.remove(scriptfile)

    def test_exit_code(self):
        self.start()
        scriptfile = mktemp()
        ecode = 15
        script = """#!/bin/bash
exit {}
""".format(ecode)
        with open(scriptfile, "w") as text_file:
            text_file.write(script)
        outputprocess = self.run_script(scriptfile, ignore_status=True)
        self.assertEqual(ecode, outputprocess.exit_status)

        self.assertRaises(process.CmdError, self.run_script, scriptfile)
        os.remove(scriptfile)
