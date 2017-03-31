# vi: set ft=ruby :
# -*- coding: utf-8 -*-
#
# This Modularity Testing Framework helps you to write tests for modules
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

    config.vm.box = "fedora/25-cloud-base"
    config.vm.synced_folder ".", "/vagrant"
    config.vm.network "private_network", ip: "192.168.50.10"
    config.vm.network "forwarded_port", guest: 80, host: 8888
    config.vm.hostname = "moduletesting"
    config.vm.post_up_message = "Results: http://localhost:8888/job-results"

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
        dnf install -y python-pip make docker httpd git python2-avocado
        pip install PyYAML behave
        
        git clone --depth 1 https://github.com/avocado-framework/avocado.git
        cd avocado
        make install

        cd optional_plugins/html
        python setup.py install

        cd /vagrant
        dnf -y copr enable phracek/Modularity-testing-framework
        dnf install -y modularity-testing-framework
        for foo in baseruntime memcached; do
            for bar in docker rpm; do
                ./run-tests $foo $bar
                mkdir -p /var/www/html/job-results/$foo-$bar
                cp -r /root/avocado/job-results/latest/* /var/www/html/job-results/$foo-$bar
                ln -sf /var/www/html/job-results/$foo-$bar/html/results.html /var/www/html/job-results/$foo-$bar/html/index.html
            done
        done
        chmod -R a+x /var/www/html/
        restorecon -r /var/www/html/
        systemctl start httpd

    SHELL
end
