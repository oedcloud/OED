#!/bin/sh

IP=`ifconfig | grep "addr:192.168.1." | awk '{print $2}'| awk -F: '{print $2}'`
DHCP_IP=`ifconfig | grep br100 -A1 | grep addr: | awk '{print $2}' | awk -F: '{print $2}'`
DISK_SIZE=`fdisk -l | grep GB | grep /dev/sda | awk '{print $3}'`
hostName=`hostname`
echo "$IP:$DHCP_IP:$DISK_SIZE:$hostName" | nc 192.168.1.1 6666
