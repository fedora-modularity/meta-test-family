#!/usr/bin/python
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

from moduleframework.pdc_data import PDCParser
from argparse import ArgumentParser
import yaml
import re

def cli():
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        help="file with message to read fedora message bus",
        default=None)
    parser.add_argument(
        "-r",
        "--release",
        dest="release",
        help="Use release in format name-stream-version as input",
        default=None)
    parser.add_argument("-l", "--latest", dest="latest",
                      help="Use latest bits, build by MBS and stored in PDC")
    parser.add_argument(
        "--commit",
        dest="commit",
        action="store_true",
        help="print git commit hash of exact version of module")
    return parser.parse_args()


def main():
    options = cli()
    name = None
    stream = None
    version = None
    if options.filename:
        flh = open(options.filename)
        stdinput = "".join(flh.readlines()).strip()
        raw = yaml.load(stdinput)
        name = raw["msg"]["name"]
        stream = raw["msg"]["stream"]
        version = raw["msg"]["version"]
        flh.close()
    elif options.release:
        name, stream, version = re.search(
            "(.*)-(.*)-(.*)", options.release).groups()
    elif options.latest:
        name = options.latest
    pdc_solver = PDCParser(name, stream, version)
    if options.commit:
        print pdc_solver.generateGitHash()
    else:
        print " ".join(pdc_solver.generateParams())
