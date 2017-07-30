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

from moduleframework.compose_info import ComposeParser
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option(
        "-c",
        "--compose",
        dest="compose",
        help="Compose repo URL")
    parser.add_option(
        "-l",
        "--list",
        action="store_true",
        default=False,
        dest="list",
        help="List Modules in compose")
    parser.add_option("-m", "--module", dest="module",
                      help="get env variable for module")
    (options, args) = parser.parse_args()
    # REPO=https://kojipkgs.stg.fedoraproject.org/compose/branched/jkaluza/latest-Boltron-26/compose/base-runtime/x86_64/os/
    if options.compose:
        a = ComposeParser(options.compose)
        if options.list:
            for foo in a.getModuleList():
                print foo
        if options.module:
            print " ".join(a.variableListForModule(options.module))
