#!/bin/bash

BRIDGE=mtf
DHCPIF=dhcpm
NPREFIX=172.2.2
RANGE="${NPREFIX}.100,${NPREFIX}.199"
NETMASK=24
LOG="dnsmasq.log"
PIDFILE="${LOG}.pid"

function mtf_bridge_setup(){
    ip link add name ${DHCPIF}-br type veth peer name ${DHCPIF}
    ip link set dev ${DHCPIF}-br up
    ip link set dev ${DHCPIF} up

    ip link add name ${BRIDGE} type bridge
    ip link set ${BRIDGE} up

    ip link set ${DHCPIF}-br master ${BRIDGE}
    ip a a dev ${DHCPIF} ${NPREFIX}.1/${NETMASK}

    /usr/sbin/dnsmasq -d --log-dhcp --bind-interfaces --listen-address=${NPREFIX}.1 \
                      --dhcp-range=${RANGE} -p 0 > ${LOG} 2>&1 &
    echo $! > ${PIDFILE}
}

function mtf_bridge_cleanup(){
    ip l d dev ${BRIDGE}
    ip l d dev ${DHCPIF}
    kill `cat ${PIDFILE}`
    rm -f ${PIDFILE}
}
