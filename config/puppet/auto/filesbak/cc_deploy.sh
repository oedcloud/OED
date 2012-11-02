#!/usr/bin/sh

sh /usr/src/ospc/openstack/pre.sh
sed -i 's/OPENSTACK_HOSTNAME/CCIP/g' /usr/src/rc/nova.conf
sh /usr/src/rc/novaI.sh CCIP

