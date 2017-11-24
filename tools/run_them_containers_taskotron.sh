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


function inst_env(){
    dnf install -y python-pip make docker httpd git python2-avocado fedpkg python2-avocado-plugins-output-html \
    pdc-client python2-modulemd python-netifaces python2-dockerfile-parse
    pip install PyYAML behave
# it should not fail anyhow
    true
#    pip install --upgrade avocado-framework avocado-framework-plugin-result-html

}

function installdeps(){
    DEPS="requirements.sh"
    echo "INSTALL TEST DEPENDENCY IF ANY FILE: $DEPS exist"
    if [ -e $DEPS ]; then
        sh $DEPS
    fi
}

function runtests(){
    echo "RUN MAKE TEST"
    make test
}

function schedule(){
    set -x
    local RESULTTOOLS=0
    local RESULT=0

    inst_env
    RESULTTOOLS=$(($RESULTTOOLS+$?))

    installdeps
    RESULT=$(($RESULT+$?))
    runtests
    RESULT=$(($RESULT+$?))

    if [ "$RESULTTOOLS" -ne 0 ]; then
        return 2
    fi

    if [ "$RESULT" -eq 0 ]; then
        # return code what means PASS
        return 0
    else
        # return code what means that some part of infra failed
        return 125
    fi
    set +x
}

schedule
exit $?
