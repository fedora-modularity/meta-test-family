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

ARCH="x86_64"
REPOMD="repodata/repomd.xml"
MODULEFILE='tempmodule.yaml'

class ComposeParser():
    def __init__(self,compose):
        self.compose = compose
        xmlrepomd = compose + "/" + REPOMD
        e = xml.etree.ElementTree.parse(urllib.urlopen(xmlrepomd)).getroot()
        modulelocaltion = e.findall(".//{http://linux.duke.edu/metadata/repo}data[@type='modules']/{http://linux.duke.edu/metadata/repo}location")[0]
        mdrawlocaltion = modulelocaltion.attrib["href"]
        response = ''.join(urllib.urlopen(compose +  "/" + mdrawlocaltion).readlines())
        tmpf=tempfile.mkstemp()
        tmpfo=open(tmpf[1],mode='w+b')
        tmpfo.write(response)
        tmpfo.close()
        self.modules = yaml.load(''.join(gzip.open(tmpf[1]).readlines()))
        os.remove(tmpf[1])

    def getModuleList(self):
        out=[]
        for foo in self.modules['modules']:
            out.append({'name':foo['data']['name'],'stream':foo['data']['stream'],'version':foo['data']['version'],})
        return out

    def variableListForModule(self,name):
        stream=None
        version=None
        thismodule=None
        out=[]
        for foo in  self.modules['modules']:
            if foo['data']['name'] == name:
                thismodule = foo
        if thismodule:
            mdo = file(MODULEFILE,mode="w")
            yaml.dump(foo,mdo)
            mdo.close()
            out.append("MODULENAME=%s" % foo['data']['name'])
            out.append("MODULE=%s" % "nspawn")
            out.append("URL=%s" % self.compose)
            out.append("MODULEMDURL=file://%s" % os.path.abspath(MODULEFILE))
            return out
