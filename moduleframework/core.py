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

from __future__ import print_function
import sys
import os

DATADIR = ['usr', 'share', 'moduleframework']

def is_debug():
    """
    Return the **DEBUG** envvar.

    :return: bool
    """
    return bool(os.environ.get("DEBUG"))


def is_not_silent():
    """
    Return the opposite of the **DEBUG** envvar.

    :return: bool
    """
    return is_debug()


def print_info(*args):
    """
    Print information from the expected stdout and
    stderr files from the native test scope.

    See `Test log, stdout and stderr in native Avocado modules
    <https://avocado-framework.readthedocs.io/en/latest/WritingTests.html
    #test-log-stdout-and-stderr-in-native-avocado-modules>`_ for more information.

    :param args: object
    :return: None
    """
    for arg in args:
        print(arg, file=sys.stderr)


def print_debug(*args):
    """
    Print information from the expected stdout and
    stderr files from the native test scope if
    the **DEBUG** envvar is set to True.

    See `Test log, stdout and stderr in native Avocado modules
    <https://avocado-framework.readthedocs.io/en/latest/WritingTests.html
    #test-log-stdout-and-stderr-in-native-avocado-modules>`_ for more information.

    :param args: object
    :return: None
    """
    if is_debug():
        print_info(*args)
