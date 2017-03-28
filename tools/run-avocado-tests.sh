#!/bin/bash
PARAMS=$@
XUFILE="out.xunit"
AVOCADOCMD="avocado run --xunit $XUFILE"

function avocado_wrapper(){
    TESTS=`ls *.py *.sh`
    eval $PARAMS
    $AVOCADOCMD $TESTS
}

avocado_wrapper
