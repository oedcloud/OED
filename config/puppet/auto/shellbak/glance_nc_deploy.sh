#!/usr/bin/sh

echo CONFIG > /usr/src/rc/cc.conf
sed -i 's/,/ /g' /usr/src/rc/cc.conf
sed -i 's/*/\n/g' /usr/src/rc/cc.conf
sh /usr/src/rc/cc-db-conf.sh

