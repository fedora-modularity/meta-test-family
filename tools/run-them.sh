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

SLEEP=15

function sleep_a_while(){
    echo "sleep for $SLEEP minutes to ensure that repos are ready"
    for foo in `seq $SLEEP`; do
        sleep 60
        echo "$foo/$SLEEP minutes done"
    done
}

function fedpkg_alt(){
    #LFILE="alt_fedpkg.conf"
    #cat /etc/rpkg/fedpkg.conf |sed 's/anongiturl.*/anongiturl = https:\/\/src.fedoraproject.org\/git\/%(module)s/' > $LFILE
    #fedpkg --config $LFILE $@
    fedpkg $@
}

export MODULENAME=$1
export PARSEITEM=$2
# compose fedmsg or None same as fedmsg
export PARSEITEMTYPE=$3
export SELECTION=$4
export MTF_PATH=/usr/share/moduleframework
export MODULE_LINT="$MTF_PATH/tools/modulelint/*.py"
export MODULE_TESTS="*.py *.sh"

export AVDIR=~/avocado
mkdir -p $AVDIR
export XUFILE="$AVDIR/out.xunit"
export AVOCADOCMD="avocado run --xunit $XUFILE"
export RESULTTOOLS=0

function getparams_int(){
    ADDIT="$1"
    if [ "$PARSEITEMTYPE" = "" -o "$PARSEITEMTYPE" = "fedmsg" ]; then
        python $MTF_PATH/tools/taskotron-msg-reader.py -f $PARSEITEM --localrepo $ADDIT
    elif [ "$PARSEITEMTYPE" = "taskotron" -o "$PARSEITEMTYPE" = "pdc" ]; then
        python $MTF_PATH/tools/taskotron-msg-reader.py -r $PARSEITEM --localrepo $ADDIT
    elif [ -z $ADDIT -a "$PARSEITEMTYPE" = "compose" ]; then
        python $MTF_PATH/tools/compose_info_parser.py -c $PARSEITEM -m $MODULENAME
    fi
}

function inst_env(){
    dnf install -y python-pip make docker httpd git python2-avocado fedpkg python2-avocado-plugins-output-html \
    pdc-client python2-modulemd python-netifaces python2-dockerfile-parse
    pip install PyYAML behave
#    pip install --upgrade avocado-framework avocado-framework-plugin-result-html

}

function loaddistgittests(){
    fedpkg_alt clone --anonymous modules/$MODULENAME
    (
        cd $MODULENAME
        git reset `getparams_int --commit`
    )
    test -f $MODULENAME/tests/Makefile
}

function loadexampletests(){
    test -e $MTF_PATH/examples/$MODULENAME
}

function is_selected(){
    test -n "$SELECTION"
}

function runselected(){
    if [ "$SELECTION" = "lint" ]; then
        run_modulelint
    fi
}



function distgit_wrapper_rpm(){
    cd $MODULENAME/tests
    eval $PARAMS make
}

function avocado_wrapper(){
    (
    cp -rf $MTF_PATH/examples/$MODULENAME tests_$MODULENAME
    cd tests_$MODULENAME
    TESTS="`ls $MODULE_TESTS $MODULE_LINT`"
    echo "AVOCADO FOUND TESTS: $TESTS"
    eval $PARAMS $AVOCADOCMD $TESTS
    )
}

function run_modulelint(){

    TESTS="`ls $MODULE_LINT`"
    echo "RUN AT LEAST MODULE LINTER: $TESTS"
    eval $PARAMS CONFIG=$MTF_PATH/docs/example-config-minimal.yaml $AVOCADOCMD $TESTS
}

set -x
inst_env
RESULTTOOLS=$(($RESULTTOOLS+$?))
PARAMS="`getparams_int`"
RESULTTOOLS=$(($RESULTTOOLS+$?))
export PARAMS

if [ "$RESULTTOOLS" -ne 0 ]; then
    echo "PREVIOUS TOOLS FAILED, STOP running Tests" > /dev/stderr
    exit 2
fi

test "$MODULENAME" = "testmodule" && MODULENAME="testing-module"

if is_selected; then
    runselected
elif loaddistgittests; then
    distgit_wrapper_rpm
elif loadexampletests; then
    avocado_wrapper
else
    run_modulelint
fi
TESTRESULT=$?

if [ "$RESULTTOOLS" -ne 0 ]; then
    exit 2
fi

if [ "$TESTRESULT" -eq 0 ]; then
    exit 0
else
    exit 125
fi
