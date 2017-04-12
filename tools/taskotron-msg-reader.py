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

from moduleframework.pdc_data import PDCParser
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="file with message to read fedora message bus",default=None)
    parser.add_option("-r", "--release", dest="release",
                      help="Use release in format name-stream-version as input",default=None)
    parser.add_option("-l", "--latest", dest="latest",
                      help="Use latest bits, build by MBS and stored in PDC")

    a = PDCParser()
    (options, args) = parser.parse_args()
    if options.filename:
        flh = open(options.filename)
        stdinput = "".join(flh.readlines()).strip()
        flh.close()
        a.setViaFedMsg(stdinput)
        print " ".join(a.generateParams())
    elif options.release:
        a.setFullVersion(options.release)
        print " ".join(a.generateParams())
    elif options.latest:
        a.setLatestPDC(options.latest)
        print " ".join(a.generateParams())
    else:
        raise Exception(parser.print_help())

