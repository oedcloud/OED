#!/usr/bin/sh

sed -i 's/GLANCE_HOSTNAME/GLANCEIP/g' /usr/src/rc/glance.conf
sed -i 's/GLANCE_HOSTNAME/GLANCEIP/g' /usr/src/rc/nova.conf
 /usr/src/rc/glanceI.sh GLANCEIP CCIP
sh /usr/src/ospc/openstack/conf >> /usr/src/ospc/openstack/iPorter.log
