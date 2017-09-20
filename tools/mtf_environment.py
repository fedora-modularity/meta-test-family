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

"""
module for environment setup and cleanup, to be able to split action for ansible, more steps instead of one complex
"""
from moduleframework.module_framework import *
from moduleframework.environment_prepare.docker_prepare import EnvDocker
from moduleframework.environment_prepare.rpm_prepare import EnvRpm
from moduleframework.environment_prepare.nspawn_prepare import EnvNspawn
from optparse import OptionParser

module_name = get_base_module()

parser = OptionParser()
parser.add_option(
    "-p",
    "--phase",
    dest="phase",
    help="apply selected mtf phase, allowed are (prepare|cleanup)",
    default=None)

(options, args) = parser.parse_args()

if module_name == "docker":
    env = EnvDocker()
elif module_name == "rpm":
    env = EnvRpm()
elif module_name == "nspawn":
    env = EnvNspawn()

if options.phase:
    if options.phase == "prepare":
        env.prepare_env()
    elif options.phase == "cleanup":
        env.cleanup_env()
    else:
        raise Exception(parser.print_help())
else:
    raise Exception(parser.print_help())
