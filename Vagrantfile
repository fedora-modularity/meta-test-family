# vi: set ft=ruby :
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

Vagrant.configure(2) do |config|

    config.vm.box = "fedora/26-cloud-base"
    config.vm.synced_folder ".", "/opt/meta-test-family"
    config.vm.network "private_network", ip: "192.168.50.10"
    config.vm.network "forwarded_port", guest: 80, host: 8888
    config.vm.hostname = "moduletesting"
    config.vm.post_up_message = "Results: http://localhost:8888/avocado/job-results/latest/html/results.html"

    config.vm.provider "libvirt" do |libvirt|
        libvirt.memory = 1024
        libvirt.nested = true
        libvirt.cpu_mode = "host-model"
    end

    config.vm.provider "virtualbox" do |virtualbox|
        virtualbox.memory = 1024
    end

    config.vm.provision "shell", inline: <<-SHELL
        set -x
        TARGET=#{ENV['TARGET']}
        test -z "$TARGET" && TARGET=check-docker

        dnf install -y make docker httpd git python2-avocado python2-avocado-plugins-output-html \
                       python-netifaces redhat-rpm-config python2-devel python-gssapi krb5-devel
        cd /opt/meta-test-family
        make install
        make -C examples/testing-module $TARGET
        cp -r /root/avocado /var/www/html/
        chmod -R a+x /var/www/html/
        restorecon -r /var/www/html/
        systemctl start httpd
    SHELL
end
