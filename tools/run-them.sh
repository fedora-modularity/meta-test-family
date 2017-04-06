#!/bin/bash
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
set -x
MODULENAME=$1
FEDMSGFILE=$2
MTF_PATH=/usr/share/moduleframework

function getparams_int(){
    python modularity-testing-framework/tools/taskotron-msg-reader.py -f $FEDMSGFILE
}
function inst_env(){
    dnf copr -y enable jscotka/modularity-testing-framework
    dnf install -y modularity-testing-framework
    dnf install -y python-pip make docker httpd git python2-avocado fedpkg python2-avocado-plugins-output-html
    pip install PyYAML behave
}

function loaddistgittests(){
    fedpkg clone -a modules/$MODULENAME
    test -f $MODULENAME/tests/Makefile
}

function loadexampletests(){
    test -f $MTF_PATH/examples/$MODULENAME
}

function distgit_wrapper_rpm(){
    cd $MODULENAME
    eval $PARAMS make
}

function examples_wrapper_rpm(){
    cd $MODULENAME
    eval $PARAMS make
}

AVDIR=~/avocado
mkdir -p $AVDIR
XUFILE="$AVDIR/out.xunit"
AVOCADOCMD="avocado run --xunit $XUFILE"
#MODULE_LINT=/usr/lib/python2.7/site-packages/moduleframework/modulelint.py
MODULE_LINT=/bin/true

function avocado_wrapper(){
    (
    cd modularity-testing-framework/examples/$MODULENAME
    TESTS="`ls *.py *.sh` $MODULE_LINT"
    echo "AVOCADO FOUND TESTS: $TESTS"
    eval $PARAMS $AVOCADOCMD $TESTS
    )
}

function run_modulelint(){

    TESTS="$MODULE_LINT"
    echo "RUN AT LEAST MODULE LINTER: $TESTS"
    eval $PARAMS $AVOCADOCMD $TESTS
}

inst_env
export PARAMS=`getparams_int`
if loaddistgittests; then
    distgit_wrapper_rpm
elif loadexampletests; then
    avocado_wrapper
else
    run_modulelint
fi
