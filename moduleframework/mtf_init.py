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

import argparse
import os.path
import logging
import sys
import yaml

logger = logging.getLogger("mtf-init")

# path fot templates test.py:
TEMPLATE_TEST = '/usr/share/moduleframework/examples/template/test.py'


def set_logging(level=logging.INFO):
    global logger
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)-6s %(message)s', '%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    mekk_logger = logging.getLogger("mekk.xmind")
    null_handler = logging.NullHandler()
    mekk_logger.addHandler(null_handler)


def cli():
    parser = argparse.ArgumentParser(
        description="Create template of your first test!",
    )
    parser.add_argument('--verbose', '-v', action='store_true',   default=False)
    parser.add_argument("--name", "-n", action="store", default="name not given", help='Name of module for testing')
    parser.add_argument("--container", "-c", action="store", required=True,
                        help='Specify container path, example: docker.io/modularitycontainers/memcached')

    args = parser.parse_args()

    set_logging(level=logging.DEBUG if args.verbose else logging.INFO)

    return args


class Template(object):
    def __init__(self, name, container):
        self.name = name
        self.container = container

    def set_content_config_yaml(self):
        self.filePathConfig = 'config.yaml'
        data = {"document" : "meta-test",
                "version" : "1",
                "name" : "xxx",
                "default_module" : "docker",
                "module" : {"docker" : {"container" : "xxx"}}}
        data['name'] = self.name
        data['module']['docker']['container'] = self.container
        self.configYaml = yaml.dump(data)
        logger.debug("{0}\n{1}".format(self.filePathConfig, self.configYaml))

    def set_content_test_py(self):
        # local name of the file:
        self.filePathTest = 'test.py'
        # use it from examples/template directory
        with open(TEMPLATE_TEST,'r') as file:
            self.test = file.read()
            file.close()

        logger.debug("{0}\n{1}".format(self.filePathTest, self.test))

    def confirm(self):
        gogo = raw_input("Continue? yes/no\n")
        if gogo.lower() == 'yes':
            exit_condition = 0
            return exit_condition
        elif gogo.lower() == "no":
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
        with open(self.filePathConfig,'w') as f1:
            f1.write(self.configYaml)
            logger.debug("{0} was changed".format(self.filePathConfig))
            f1.close()

        with open(self.filePathTest,'w') as f2:
            f2.write(self.test)
            logger.debug("{0} was changed".format(self.filePathTest))
            f2.close()


def main():
    args = cli()
    logger.debug("Options: name={0}, container={1}".format(args.name, args.container))
    resobj = Template(args.name, args.container)
    resobj.set_content_config_yaml()
    resobj.set_content_test_py()
    if not resobj.check_file():
        print("do nothing")
        exit(1)
    resobj.save()
    print("Done, to run test:\n\tsudo mtf test.py")
