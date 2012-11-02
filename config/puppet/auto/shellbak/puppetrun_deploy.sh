#!/usr/bin/sh

echo "    listen = true" >> /etc/puppet/puppet.conf
echo "PUPPET_SERVER=nova7.sh.intel.com" >> /etc/sysconfig/puppet
echo -e "[puppetrunner]\n    allow *" > /etc/puppet/namespaceauth.conf
FILE=/etc/puppet/auth.conf
line=`sed -n '/path \/$/=' $FILE`
sed -i -e ${line}i"path /run\nmethod save\nallow *" $FILE
service puppet restart
