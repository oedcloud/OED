#!/usr/bin/sh

echo nova29,10.239.82.107,GLANCEIP*nova25,10.239.82.172,GLANCEIP > /usr/src/rc/cc.conf
sed -i 's/,/ /g' /usr/src/rc/cc.conf
sed -i 's/*/\n/g' /usr/src/rc/cc.conf
sh /usr/src/rc/cc-db-conf.sh
sh /usr/src/rc/glancencI.sh GLANCEIP
