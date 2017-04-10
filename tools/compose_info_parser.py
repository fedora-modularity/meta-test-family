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
import urllib
import xml.etree.ElementTree
import gzip
import tempfile
import os

from optparse import OptionParser

ARCH="x86_64"
REPOMD="repodata/repomd.xml"
MODULEFILE='tempmodule.yaml'
class ComposeParser():
    def __init__(self,compose):
        xmlrepomd = compose + "/" + REPOMD
        e = xml.etree.ElementTree.parse(urllib.urlopen(xmlrepomd)).getroot()
        modulelocaltion = e.findall(".//{http://linux.duke.edu/metadata/repo}data[@type='modules']/{http://linux.duke.edu/metadata/repo}location")[0]
        mdrawlocaltion = modulelocaltion.attrib["href"]
        response = ''.join(urllib.urlopen(compose +  "/" + mdrawlocaltion).readlines())
        tmpf=tempfile.mkstemp()
        tmpfo=open(tmpf[1],mode='w+b')
        tmpfo.write(response)
        tmpfo.close()
        modules = yaml.load(''.join(gzip.open(tmpf[1]).readlines()))
        os.remove(tmpf[1])
        for foo in  modules['modules']:
            print foo['data']['name']
            mdo = file(MODULEFILE,mode="w")
            yaml.dump(foo,mdo)
            mdo.close()
            print "MODULENAME=%s" % foo['data']['name']
            print "URL=%s" % compose
            print "MODULEMDURL=file://%s" % MODULEFILE




parser = OptionParser()
parser.add_option("-c", "--compose", dest="compose", help="Compose repo URL")
(options, args) = parser.parse_args()
#REPO=https://kojipkgs.stg.fedoraproject.org/compose/branched/jkaluza/latest-Boltron-26/compose/base-runtime/x86_64/os/
if options.compose:
    a = ComposeParser(options.compose)

