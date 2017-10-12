# -*- coding: utf-8 -*-
# Script generates super easy template of test for module docker
# Purpose of this script is to generate needed files to start testing
# Author Petr Sklenar psklenar@gmail.com
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

from optparse import OptionParser
import os.path

def get_options():
    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")
    parser.add_option("-n", "--name",
                      default="name",
                      dest="name",
                      help="Name of module for testing")
    parser.add_option("-c", "--container",
                      dest="container",
                      default="docker.io/modularitycontainers/memcached",
                      action="store",
                      help="Specify container path, example: docker.io/modularitycontainers/memcached")
    (options, args) = parser.parse_args()

    return options

class Template(object):
    def __init__(self, name, container):
        self.name = name
        self.container = container

    def set_content_config_yaml(self):
        self.filePathConfig = 'config.yaml'
        configYaml = """# this is generated config.yaml with minimum stuff
---
document: meta-test
version: 1
name: {name}
default_module: docker
module:
    docker:
        container: {container}
""".format(name=self.name, container=self.container)
        self.configYaml = configYaml

    def set_content_test_py(self):
        self.filePathTest = 'test.py'
        test = '''#!/usr/bin/python

# test example
# start test: "sudo mtf"

from avocado import main
from avocado.core import exceptions
from moduleframework import module_framework

class Smoke1(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test_uname(self):
        self.start()
        self.run("uname | grep Linux")

    def test_echo(self):
        self.start()
        self.runHost("echo test | grep test")

if __name__ == '__main__':
    main()

'''
        self.test = test

    def confirm(self):
        gogo = raw_input("Continue? yes/no\n")
        if gogo == 'yes':
            exit_condition = 0
            return exit_condition
        elif gogo == "no":
            exit_condition = 1
            exit(1)
            return exit_condition
        else:
            print "Please answer with yes or no."
            return 2

    def check_file(self):
        if os.path.isfile(self.filePathConfig) and os.path.isfile(self.filePathTest):
            print("!!! File exists, rewrite?")
            continue1=2
            while continue1 is 2:
                continue1=self.confirm()
            if continue1 is 1:
                return False
        return True

    def save(self):
        f1 = open(self.filePathConfig,'w')
        f1.write(self.configYaml)
        f1.close()

        f2 = open(self.filePathTest,'w')
        f2.write(self.test)
        f2.close()

def main():
    options=get_options()
    resobj = Template(options.name, options.container)
    resobj.set_content_config_yaml()
    resobj.set_content_test_py()
    if not resobj.check_file():
        print("do nothing")
        exit(1)
    resobj.save()
    print("Done, to run test:\n\tsudo mtf test.py")