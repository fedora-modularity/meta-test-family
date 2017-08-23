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
export MTF_PATH="/usr/share/moduleframework"
export MODULE_LINT="$MTF_PATH/tools/modulelint/*.py"
export MINIMAL_CONFIG="$MTF_PATH/docs/example-config-minimal.yaml"
export MODULE_TESTS="*.py *.sh"

export AVDIR=~/avocado
mkdir -p $AVDIR
export XUFILE="$AVDIR/out.xunit"
export AVOCADOCMD="avocado run --xunit $XUFILE --show-job-log"
export RESULTTOOLS=0
export MTF_RECURSIVE_DOWNLOAD=yes

function getparams_int(){
    ADDIT="$1"
    if [ "$PARSEITEMTYPE" = "" -o "$PARSEITEMTYPE" = "fedmsg" ]; then
        python $MTF_PATH/tools/taskotron-msg-reader.py -f $PARSEITEM $ADDIT
    elif [ "$PARSEITEMTYPE" = "taskotron" -o "$PARSEITEMTYPE" = "pdc" ]; then
        python $MTF_PATH/tools/taskotron-msg-reader.py -r $PARSEITEM $ADDIT
    elif [ -z $ADDIT -a "$PARSEITEMTYPE" = "compose" ]; then
        python $MTF_PATH/tools/compose_info_parser.py -c $PARSEITEM -m $MODULENAME
    fi
}

function inst_env(){
    dnf install -y python-pip make docker httpd git python2-avocado fedpkg python2-avocado-plugins-output-html \
    pdc-client python2-modulemd python-netifaces python2-dockerfile-parse
    pip install PyYAML behave
# it should not fail anyhow
    true
#    pip install --upgrade avocado-framework avocado-framework-plugin-result-html

}

function loaddistgittests(){
    fedpkg_alt clone --anonymous modules/$MODULENAME
    (
        cd $MODULENAME
        git checkout `getparams_int --commit`
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
    eval $PARAMS mtf-env-set
    eval $PARAMS make
}

function avocado_wrapper(){
    (
    cp -rf $MTF_PATH/examples/$MODULENAME tests_$MODULENAME
    cd tests_$MODULENAME
    TESTS="`ls $MODULE_TESTS $MODULE_LINT`"
    echo "AVOCADO FOUND TESTS: $TESTS"
    eval $PARAMS mtf-env-set
    eval $PARAMS $AVOCADOCMD $TESTS
    )
}

function run_modulelint(){

    TESTS="`ls $MODULE_LINT`"
    echo "RUN AT LEAST MODULE LINTER: $TESTS"
    eval $PARAMS CONFIG=$MINIMAL_CONFIG mtf-env-set
    eval $PARAMS CONFIG=$MINIMAL_CONFIG $AVOCADOCMD $TESTS
}

set -x
inst_env
RESULTTOOLS=$(($RESULTTOOLS+$?))

PARAMS="`DEBUG=yes getparams_int`"
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
    # moduleLint Disabled
    # run_modulelint
    # return code what means SKIP results and do not interpret it
    exit 126
fi
TESTRESULT=$?


MODULE=nspawn mtf-env-clean

if [ "$RESULTTOOLS" -ne 0 ]; then
    exit 2
fi

if [ "$TESTRESULT" -eq 0 ]; then
# return code what means PASS
    exit 0
else
# return code what means that some part of infra failed
    exit 125
fi

