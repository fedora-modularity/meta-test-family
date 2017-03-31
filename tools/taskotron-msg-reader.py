#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This Modularity Testing Framework helps you to write tests for modules
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

import yaml
import sys
import os

from optparse import OptionParser

ARCH="x86_64"

class FedMsgParser():
    def __init__(self,yamlinp):
        self.out = []
        raw = yaml.load(yamlinp)
        #"kojipkgs.fedoraproject.org/repos/module-" + module_name + "-" + module_stream + "/latest"
        self.topic=raw["topic"]
        if self.topic == "org.fedoraproject.prod.mbs.module.state.change":
            self.out = self.modulechangemessage(raw["msg"])

    def modulechangemessage(self,msg):
        self.rpmrepo = "http://kojipkgs.fedoraproject.org/repos/module-%s-%s-%s/latest/%s" % (
            msg["name"], msg["stream"], msg["version"], ARCH )

        omodulefile = "module.yaml"
        mdfile = open(omodulefile,mode = "w")
        mdfile.write(msg["modulemd"])
        mdfile.close()
        output = []
        output.append("URL=%s" % self.rpmrepo)
        output.append("MODULEMDURL=file://%s" % os.path.abspath(omodulefile))
        output.append("MODULE=rpm")
        return output

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="file with message to read instead of stdin",default=None)
(options, args) = parser.parse_args()
if options.filename:
    flh = open(os.path.abspath(options.filename))
    stdinput = "".join(flh.readlines()).strip()
    flh.close()
else:
    stdinput = "".join(sys.stdin.readlines()).strip()
a=FedMsgParser(stdinput)
print " ".join(a.out)