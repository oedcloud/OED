#!/bin/bash

#nc -l 6666 >> /etc/puppet/client_info

info=`nc -l 6666`
OLD_IFS="$IFS"
IFS=":"
arr=($info)
IFS="$OLD_IFS"
static_ip=${arr[0]}
dhcp_ip=${arr[1]}
host_name=${arr[2]}

echo -e "$static_ip\t$host_name.sh.intel.com" >> /etc/hosts

#sqlite3 somedb 'insert into sometalbe(hostname, static_ip, dhcp_ip, timestamp) values("'$host_name'","'$static_ip'","'$dhcp_ip'",CURRENT_TIMESTAMP);'
