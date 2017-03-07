#!/bin/bash
set -x
EC=0
echo "Initialize module"
moduleframework-cmd -v setUp
moduleframework-cmd -v start

echo "Start testing"

echo "Test what run bash command inside module"
moduleframework-cmd -v -p run ls / | grep sbin
EC=$(($EC+$?))

echo "Test what run bash command outside, host"
echo errr | nc localhost 11211
EC=$(($EC+$?))

echo "Destroy module"
moduleframework-cmd -v tearDown
exit $EC
