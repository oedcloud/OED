#!/usr/bin/sh

echo HOSTNAME > /usr/src/rc/portalDB.conf
sed -i 's/:/ /g' /usr/src/rc/portalDB.conf
sh /usr/src/rc/portalDBConf.sh
sh /usr/src/rc/tomcat.sh
sh /usr/src/rc/tomcatI.sh
