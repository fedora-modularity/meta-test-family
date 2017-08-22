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
Module to setup and cleanup the test environment.
"""
from moduleframework.module_framework import *
from moduleframework.environment_prepare.docker_prepare import EnvDocker
from moduleframework.environment_prepare.rpm_prepare import EnvRpm
from moduleframework.environment_prepare.nspawn_prepare import EnvNspawn

(module_object, module_name) = get_backend()

if module_name == "docker":
    env = EnvDocker()
elif module_name == "rpm":
    env = EnvRpm()
elif module_name == "nspawn":
    env = EnvNspawn()

def mtfenvset():
    env.prepare_env()

def mtfenvclean():
    env.cleanup_env()

