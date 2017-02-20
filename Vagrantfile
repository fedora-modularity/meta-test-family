# vi: set ft=ruby :
#
# See HACKING.md for how to use this Vagrantfile.
#

Vagrant.configure(2) do |config|

    config.vm.box = "fedora/25-cloud-base"
    config.vm.synced_folder ".", "/vagrant"
    config.vm.network "private_network", ip: "192.168.50.10"
    config.vm.network "forwarded_port", guest: 8000, host: 8000
    config.vm.hostname = "moduletesting"
    config.vm.post_up_message = "Results: http://localhost:8000"

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
        #dnf update -y
        dnf install -y python-pip make docker python-libs
        cd /vagrant
        make install
        make check

        cd /root/avocado/
        nohup python –m SimpleHTTPServer&
        sleep 2
    SHELL
end
