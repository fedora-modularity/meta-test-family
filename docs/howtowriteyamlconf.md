## Document identification
There is nothing important, just parser inside check if config yaml is the proper one, that nobody for example does not used modulemd.yaml as config.yaml
```yaml
document: modularity-testing
version: 1
```

## Module generic part
This part contain generic part of module
```yaml
name: memcached
modulemd-url: http://raw.githubusercontent.com/container-images/memcached/master/memcached.yaml
service:
    port: 11211
packages:
    rpms:
        - memcached
        - perl-Carp
testdependecies:
    rpms:
        - nc
```
 * `name:` name of module
 * `modulemd-url:` link to modulemd file, now it is not used anyhow, just for installing packages for proper module
 * `service:` In case module is service like memcached, store there port number, can be then used in tests, to not hardcode port number *(Optional)*
 * `packages:` Which packages has to be installed, propabably there will be packages from __api__ specification
 * `testdependecies:` Install dependecies on host, what are important for module testing, for example when you would like to use `nc`, you have to install it explicitly, it is not in cloud images.

## Module types specification
It contains specification for each type of module, now for __rpm__ and __docker__ based modules
```yaml
module:
    docker:
        start: "docker run -it -e CACHE_SIZE=128 -p 11211:11211"
        labels:
            description: "memcached is a high-performance, distributed memory"
            io.k8s.description: "memcached is a high-performance, distributed memory"
        source: https://github.com/container-images/memcached.git
        container: docker.io/phracek/memcached
    rpm:
        start: systemctl start memcached
        stop: systemctl stop memcached
        status: systemctl status memcached
        repos:
            - http://download.englab.brq.redhat.com/pub/fedora/releases/25/Everything/x86_64/os/
            - https://phracek.fedorapeople.org/memcached-module-repo/
```
 * `start:` how to start service in case it is service, in case of generic module it is *(Optional)*
 * `stop:` how to service service in case it is service, in case of generic module it is *(Optional)*
 * `status:` how to check service state, in case of generic module it is *(Optional)*
 * `labes:` docker labels to check, specific just for *docker* cotainer *(Docker specific)*
 * `cotainer:` where is link to container, now it support docker.io link or using locally tar.gz file specified *(Docker specific)*
 *  `repos:` contains all repos what has to be used for this module (typically baseruntime + specific one) *(Rpm specific)*

## Simple tests inside config
 This part is little but __controversial__ , some of users are fans and some hates this. It allows you to specify bash style tests directly inside config file
```yaml
test:
    processrunning:
        - 'ls  /proc/*/exe -alh | grep memcached'
testhost:
    selfcheck:
        - 'echo errr | nc localhost 11211'
        - 'echo set AAA 0 4 2 | nc localhost 11211'
        - 'echo get AAA | nc localhost 11211'
    selcheckError:
        - 'echo errr | nc localhost 11211 |grep ERROR'
```
 * `test:` tests what will run inside container - it means that there has to be all dependencies for these test *(Optional)*
  * every command has to finish with __0 return code__ otherwise it will __fail__
  * next level like __processrunning__ is test name what will be visible on output of avocado run, then all lines will be run as commands for this test
 * `testhost:` it is similar to *test*,  just difference is that it runs commands on host machine so that there could be more dependencies than just are in module. I', not sure if this part is usefull, will see after discussion *(Optional)*
  * other specification is same as `test`

