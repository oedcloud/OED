#!/bin/sh

STATIC_IP=`ifconfig eth0 | grep 'inet addr'  | awk '{print $2}' | awk -F: '{print $2}'`
DHCP_IP=`ifconfig | grep br100 -A1 | grep addr: | awk '{print $2}' | awk -F: '{print $2}'`
hostName=`hostname`
flag="2"
message="ipupdate"
telnet 192.168.1.1 3336 &
sleep 2
echo "$flag:$STATIC_IP:$DHCP_IP:$hostName:$message" | nc 192.168.1.1 6666
python /opt/logmonitor.py &> /opt/ospc/post.log &
