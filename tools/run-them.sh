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
export MODULENAME=$1
export FEDMSGFILE=$2
export MTF_PATH=/usr/share/moduleframework
export MODULE_LINT=$MTF_PATH/tools/modulelint.py

export AVDIR=~/avocado
mkdir -p $AVDIR
export XUFILE="$AVDIR/out.xunit"
export AVOCADOCMD="avocado run --xunit $XUFILE"


function getparams_int(){
    python $MTF_PATH/tools/taskotron-msg-reader.py -f $FEDMSGFILE
}

function inst_env(){
    dnf install -y python-pip make docker httpd git python2-avocado fedpkg python2-avocado-plugins-output-html
    pip install PyYAML behave
}

function loaddistgittests(){
    fedpkg clone -a modules/$MODULENAME
    test -f $MODULENAME/tests/Makefile
}

function loadexampletests(){
    test -e $MTF_PATH/examples/$MODULENAME
}

function distgit_wrapper_rpm(){
    cd $MODULENAME
    eval $PARAMS make
}

function avocado_wrapper(){
    (
    TESTS="`ls $MTF_PATH/examples/$MODULENAME/*.py $MTF_PATH/examples/$MODULENAME/*.sh` $MODULE_LINT"
    echo "AVOCADO FOUND TESTS: $TESTS"
    eval $PARAMS CONFIG=$MTF_PATH/examples/$MODULENAME/config.yaml $AVOCADOCMD $TESTS
    )
}

function run_modulelint(){

    TESTS="$MODULE_LINT"
    echo "RUN AT LEAST MODULE LINTER: $TESTS"
    eval $PARAMS $AVOCADOCMD $TESTS
}

inst_env

export PARAMS="`getparams_int`"

if loaddistgittests; then
    distgit_wrapper_rpm
elif loadexampletests; then
    avocado_wrapper
else
    run_modulelint
fi
