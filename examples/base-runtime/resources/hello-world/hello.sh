#!/bin/bash
set -e  # exit immediately on any failure
microdnf install tar make gcc 1>&2
cd /mnt
tar xzvf hello.tgz 1>&2
make 1>&2
./hello
