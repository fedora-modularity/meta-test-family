#!/bin/bash
set -x
CMD=./moduleframework-cmd
EC=0
echo "Initialize module"
$CMD -v setUp
$CMD -v start

echo "Start testing"

echo "Test what run bash command inside module"
$CMD -v -p run echo ahoj
$CMD -v -p run ls / | grep bin
EC=$(($EC+$?))

echo "Destroy module"
$CMD -v tearDown
exit $EC
