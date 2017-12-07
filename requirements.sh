#!/bin/bash

GENERICPACKAGES="
curl
git
make
python-pip
"
RPMPACKAGES="
fedpkg
httpd
koji
krb5-devel
nc
pdc-client
python-devel
python-gssapi
python-netifaces
python2-avocado
python2-avocado-plugins-output-html
python2-devel
python2-dockerfile-parse
python2-modulemd
python2-odcs-client
python2-pytest
redhat-rpm-config
"

APTPACKAGES="
build-essential
libkrb5-dev
mysql-client-5.5
netcat
python-dev
python-pytest
python-software-properties
software-properties-common
"

PIPPACKAGES="
avocado-framework
"

if [ -e /usr/bin/dnf ]; then
    dnf -y install $GENERICPACKAGES $RPMPACKAGES
elif [ -e /usr/bin/yum ]; then
    yum -y install $GENERICPACKAGES $RPMPACKAGES
else
    apt-get -y install $GENERICPACKAGES $APTPACKAGES
    pip install $PIPPACKAGES
fi
