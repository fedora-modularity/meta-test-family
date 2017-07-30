#!/bin/bash
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

set -x
EC=0
echo "Initialize module"
moduleframework-cmd -v setUp
moduleframework-cmd -v start

echo "Start testing"

echo "Test what run bash command inside module"
moduleframework-cmd -v -p run ls / | grep sbin
EC=$(($EC+$?))

echo "Test what run bash command outside, host"
echo errr | nc localhost 11211
EC=$(($EC+$?))

echo "Destroy module"
moduleframework-cmd -v tearDown
exit $EC
