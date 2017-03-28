#!/bin/bash

PARAMS=$@
AVOCADOCMD="avocado run -xunit"

function avocado(){
    TESTS=`ls *.py *.sh`
    eval $PARAMS
    $AVOCADOCMD $TESTS
}

avocado
