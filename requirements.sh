#!/bin/bash

GENERICPACKAGES="make git curl"
RPMPACKAGES="httpd python2-avocado python2-avocado-plugins-output-html
             python-netifaces redhat-rpm-config python2-devel python-gssapi krb5-devel"
APTPACKAGES="python-software-properties software-properties-common python-pip python-dev
             build-essential libkrb5-dev netcat mysql-client-5.5 python-pytest"
PIPPACKAGES="avocado-framework"

if [ -e /usr/bin/dnf ]; then
    dnf -y install $GENERICPACKAGES $RPMPACKAGES
elif [ -e /usr/bin/yum ]; then
    yum -y install $GENERICPACKAGES $RPMPACKAGES
else
    apt-get -y install $GENERICPACKAGES $APTPACKAGES
    pip install $PIPPACKAGES
fi
