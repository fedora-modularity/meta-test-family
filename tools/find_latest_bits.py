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

import yaml
import sys
import os
import json
import urllib
import re

from optparse import OptionParser

ARCH = "x86_64"
PDCURL = "https://pdc.fedoraproject.org/rest_api/v1/unreleasedvariants"


class FedMsgParser():

    def __init__(self, yamlinp, taskotron=False):
        self.out = []
        if taskotron:
            name, stream, version = re.search(
                "(.*)-(.*)-(.*)", yamlinp).groups()
        else:
            raw = yaml.load(yamlinp)
            self.topic = raw["topic"]
            name = raw["msg"]["name"]
            stream = raw["msg"]["stream"]
            version = raw["msg"]["version"]
        PDC = "%s/?variant_name=%s&variant_version=%s&variant_release=%s&active=True" % (
            PDCURL, name, stream, version)
        self.pdcdata = json.load(urllib.urlopen(PDC))["results"][0]

    def generateParams(self):
        self.rpmrepo = "http://kojipkgs.fedoraproject.org/repos/%s/latest/%s" % (
            self.pdcdata["koji_tag"], ARCH)

        omodulefile = "module.yaml"
        mdfile = open(omodulefile, mode="w")
        mdfile.write(self.pdcdata["modulemd"])
        mdfile.close()
        output = []
        output.append("URL=%s" % self.rpmrepo)
        output.append("MODULEMDURL=file://%s" % os.path.abspath(omodulefile))
        output.append("MODULE=rpm")
        return output


parser = OptionParser()
parser.add_option(
    "-f",
    "--file",
    dest="filename",
    help="file with message to read fedora message bus",
    default=None)
parser.add_option(
    "-r",
    "--release",
    dest="release",
    help="Use release in format name-stream-version as input",
    default=None)

(options, args) = parser.parse_args()
if options.filename:
    flh = open(os.path.abspath(options.filename))
    stdinput = "".join(flh.readlines()).strip()
    flh.close()
    a = FedMsgParser(stdinput)
    print " ".join(a.generateParams())
elif options.release:
    a = FedMsgParser(options.release, taskotron=True)
    print " ".join(a.generateParams())
else:
    raise Exception(parser.print_help())
