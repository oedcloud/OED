#!/bin/bash

set -e

echo Pxeserver start up on `date`
#check the network
if [ ! -n "`ifconfig eth0 | grep 192.168.1.1`" ]; then
cat > /etc/network/interfaces << EOF
auto lo
iface lo inet loopback

auto eth1
iface eth1 inet static
    address 192.168.1.1
    netmask 255.255.255.0
    broadcast 192.168.1.255   
EOF
    /etc/init.d/networking restart
fi

/etc/init.d/dnsmasq restart
/etc/init.d/xinetd restart
#/etc/init.d/rabbitmq-server restart
/etc/init.d/apache2 restart
/etc/init.d/puppetmaster restart
/etc/init.d/ntp restart
/etc/init.d/celeryd restart
chmod 777 -R /pxeinstall/httpd/ospcdeploy

echo 
echo "If no error occurs, you can enter the ospcdeploy home page through the link http://pxeserver/ospcdeploy/ospcdeploy now."
echo

