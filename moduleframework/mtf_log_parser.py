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
# Authors: Petr Sklenar <psklenar@redhat.com>
#

"""
Utility for reading avocado json files.
"""

import sys
import json

def main():
    try:
        json_data=open(sys.argv[1]).read()
        data = json.loads(json_data)
    except (IOError, ValueError) as e:
        # file is not readable as json: No JSON object could be decoded
        print(e)
        exit(1)
    except:
        print("no file: specify 1 argument as existing json file")
        exit(3)
    delimiter=""
    for i in data['tests']:
        if i.get('status') in ['ERROR','FAIL']:
            print(delimiter)
            print("TEST:   {0}".format(i.get('id')))
            print("ERROR:  {0}".format(i.get('fail_reason')))
            print("        {0}".format(i.get('logfile')))
            delimiter = "-------------------------"

