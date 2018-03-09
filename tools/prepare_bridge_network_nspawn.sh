#!/bin/bash

BRIDGE=mtf
DHCPIF=dhcpm
SECONDIF=sec
NPREFIX=192.168.223
RANGE="${NPREFIX}.100,${NPREFIX}.199"
DHCPSERVERIP=${NPREFIX}.1
NETMASK=24
LOG="dnsmasq.log"
PIDFILE="${LOG}.pid"

function mtf_bridge_setup(){
    ip link add name ${BRIDGE} type bridge
    brctl stp ${BRIDGE} off
    ip link set ${BRIDGE} up

    ip link add name ${DHCPIF}-br type veth peer name ${DHCPIF}
    ip link set dev ${DHCPIF}-br up
    ip link set dev ${DHCPIF} up
    ip link set ${DHCPIF}-br master ${BRIDGE}

    ip link add name ${SECONDIF}-br type veth peer name ${SECONDIF}
    ip link set dev ${SECONDIF}-br up
    ip link set dev ${SECONDIF} up
    ip link set ${SECONDIF}-br master ${BRIDGE}

    ip a a dev ${DHCPIF} ${DHCPSERVERIP}/${NETMASK}
    sleep 5
    /usr/sbin/dnsmasq -d --log-dhcp -i ${DHCPIF} --dhcp-range=${RANGE} -p 0 > ${LOG} 2>&1 &
    echo $! > ${PIDFILE}
}

function mtf_bridge_cleanup(){
    kill `cat ${PIDFILE}`
    sleep 5
    ip l d dev ${DHCPIF}
    ip l d dev ${SECONDIF}
    ip l d dev ${BRIDGE}
    rm -f ${PIDFILE}
}
