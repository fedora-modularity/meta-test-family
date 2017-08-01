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
PARAMS=$@
AVDIR=~/avocado
mkdir -p $AVDIR
XUFILE="$AVDIR/out.xunit"
AVOCADOCMD="avocado run --xunit $XUFILE"

function avocado_wrapper(){
    TESTS=`ls *.py *.sh`
    echo "FOUND TESTS: $TESTS"
    eval $PARAMS $AVOCADOCMD $TESTS
}

# workaround for missing html plugin by default installation (not necessary, but nice)
sudo dnf install -y python2-avocado-plugins-output-html || true

avocado_wrapper
