% MEMCACHED(1) Container Image Pages
% Petr Hracek
% February 6, 2017

# NAME
{{ spec.envvars.name }} - {{ spec.description }}

# DESCRIPTION
Memcached is a high-performance, distributed memory object caching system, generic in nature, but intended for use in speeding up dynamic web applications by alleviating database load.

The container itself consists of:
    - fedora/{{ config.os.version }} base image
    - {{ spec.envvars.name }} RPM package

Files added to the container during docker build include: /files/memcached.sh

# USAGE
To get the memcached container image on your local system, run the following:

    docker pull docker.io/modularitycontainers/{{ spec.envvars.name }}

  
# SECURITY IMPLICATIONS
Lists of security-related attributes that are opened to the host.

-p 11211:11211
    Opens container port 11211 and maps it to the same port on the host.

# SEE ALSO
Memcached page
<https://memcached.org/>
