#!/bin/bash
PARAMS=$@
AVDIR=~/avocado
mkdir -p $AVDIR
XUFILE="$AVDIR/out.xunit"
AVOCADOCMD="avocado run --xunit $XUFILE"

function avocado_wrapper(){
    TESTS=`ls *.py *.sh`
    eval $PARAMS
    $AVOCADOCMD $TESTS
}

avocado_wrapper
