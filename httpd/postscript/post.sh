#!/bin/bash

#pxeserver IP
PXE_SERVER=192.168.1.1

#static IP
STATIC_IP=`ifconfig eth0 | grep 'inet addr'  | awk '{print $2}' | awk -F: '{print $2}'`

#lightdm conf file to config sreen login
LIGHTDM_CONF=/etc/lightdm/lightdm.conf

#ubuntu oneiric source list
APT_SOURCE=/etc/apt/sources.list

#apt conf file
APT_CONF=/etc/apt/apt.conf

#puppet client root
PUPPET_CONF=/etc/puppet/

#network config file
NET_CONF=/etc/network/interfaces

#ssh config file
SSH_CONF=/etc/ssh/ssh_config

#ssh key pair folder
SSH_KEY=/root/.ssh/

#ospc installation and source file directory
OSPC_ROOT=/opt/ospc

#log file for this script
LOG=$OSPC_ROOT/post.log

if [ ! -d $OSPC_ROOT ]; then 
	mkdir -p $OSPC_ROOT
fi

if [ -z $LOG ]; then
        cat /dev/null > $LOG
fi

echo `date "+%Y-%m-%d %H:%M:%S"` Remove guest session. | tee $LOG
if [ ! -n "`grep allow-guest $LIGHTDM_CONF`" ]; then 
	echo allow-guest=false >> $LIGHTDM_CONF
        /etc/init.d/lightdm restart | tee -a $LOG
fi

echo `date "+%Y-%m-%d %H:%M:%S"` Set /etc/hosts  | tee -a $LOG
if [ ! -n "`grep $PXE_SERVER /etc/hosts`" ]; then
	echo $PXE_SERVER    pxeserver >> /etc/hosts
fi

echo `date "+%Y-%m-%d %H:%M:%S"` Set up bridge  | tee -a $LOG
cat > $NET_CONF << EOF
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address $STATIC_IP
    netmask 255.255.255.0
    broadcast 192.168.1.255

auto eth1
iface eth1 inet dhcp

auto br100
iface br100 inet dhcp
bridge_ports eth1
bridge_stps off
bridge_maxwait 0
bridge_fd 0
EOF

PKG_NAME=bridge-utils_1.5-2ubuntu1_amd64.deb
echo `date "+%Y-%m-%d %H:%M:%S"` Download bridge-utils from server  | tee -a $LOG
wget -O $OSPC_ROOT/$PKG_NAME http://$PXE_SERVER/package/$PKG_NAME | tee -a $LOG
dpkg -i $OSPC_ROOT/$PKG_NAME | tee -a $LOG
dpkg -l bridge-utils  | tee -a $LOG
if [ "$?" -eq 0 ]; then
	/etc/init.d/networking stop | tee -a $LOG
	/etc/init.d/networking start | tee -a $LOG
else
	echo `date "+%Y-%m-%d %H:%M:%S"` failed to install bridge-utils | tee -a $LOG
fi

echo `date "+%Y-%m-%d %H:%M:%S"` Set up default gateway  | tee -a $LOG
if [ -n "`route -n | grep 192.168.1.1`" ] ; then
	echo `date "+%Y-%m-%d %H:%M:%S"` Delete gw 192.168.1.1 if exists | tee -a $LOG
	route del default gw 192.168.1.1 | tee -a $LOG
fi
route add -net 192.168.1.0/24 gw 192.168.1.1 dev eth0 metric 1 | tee -a $LOG
if [ ! -n "`route -n | grep 10.239.82.1`" ]; then
	echo `date "+%Y-%m-%d %H:%M:%S"` Add default gw 10.239.82.1  if exists | tee -a $LOG
	route add default gw 10.239.82.1 | tee -a $LOG
	#route add -net 192.168.1.0/24 gw 192.168.1.1 dev eth0 metric 1 | tee -a $LOG
fi

echo `date "+%Y-%m-%d %H:%M:%S"` Change apt source.list | tee -a $LOG
sed -i "s/$PXE_SERVER/cn.archive.ubuntu.com/" $APT_SOURCE && echo done. || echo failed.

echo `date "+%Y-%m-%d %H:%M:%S"` Change apt http proxy setting | tee -a $LOG
if [ ! -n "`grep proxy.pd.intel.com $APT_CONF`" ]; then
cat >> $APT_CONF << EOF
Acquire::http::proxy "http://proxy.pd.intel.com:911";
Acquire::ftp::proxy "http://proxy.pd.intel.com:911";
Acquire::https::proxy "http://proxy.pd.intel.com:911";
EOF
fi
proc_id=`ps -ef | grep apt | grep -v grep | awk "{print $2 }"`
if [ -n "$proc_id" ]; then
	kill -9 $proc_id | tee -a $LOG
fi

#echo `date "+%Y-%m-%d %H:%M:%S"` Refresh apt-get source | tee -a $LOG 
#ifconfig br100 | tee -a $LOG
#if [ -n "$?" ]; then
#apt-get update
#echo `date "+%Y-%m-%d %H:%M:%S"` Install new packages | tee -a $LOG
#apt-get install -y --force-yes puppet | tee -a $LOG
#apt-get install -y --force-yes vim
#apt-get install -y --force-yes bridge-utils
#else
#	echo network failure | tee -a $LOG
#fi
	 

#echo `date "+%Y-%m-%d %H:%M:%S"` Install new packages | tee -a $LOG 
#apt-get install -y --force-yes puppet
#apt-get install -y --force-yes vim
#apt-get install -y --force-yes bridge-utils

#echo `date "+%Y-%m-%d %H:%M:%S"` Transfer puppet config file  | tee -a $LOG
#for file in auth.conf puppet.conf namespaceauth.conf; do
#	echo `date "+%Y-%m-%d %H:%M:%S"` transfer file $file  | tee -a $LOG
#	wget -O $PUPPET_CONF/$file http://$PXE_SERVER/puppet/$file | tee -a $LOG
#done

#echo `date "+%Y-%m-%d %H:%M:%S"` Change puppet conf  | tee -a $LOG
#sed -i "s/START=no/START=yes/" /etc/default/puppet | tee -a $LOG

#echo `date "+%Y-%m-%d %H:%M:%S"` Set up bridge  | tee -a $LOG
#cat > $NET_CONF << EOF
#auto lo
#iface lo inet loopback

#auto eth0
#iface eth0 inet static
#    address $STATIC_IP
#    netmask 255.255.255.0
#    broadcast 192.168.1.255

#auto eth1
#iface eth1 inet dhcp

#auto br100
#iface br100 inet dhcp
#bridge_ports eth1
#bridge_stps off
#bridge_maxwait 0
#bridge_fd 0
#EOF
#/etc/init.d/networking restart | tee -a $LOG

#echo `date "+%Y-%m-%d %H:%M:%S"` SSH key pair  | tee -a $LOG
#sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/" $SSH_CONF 
#mkdir -p $SSH_KEY/
#for key in authorized_keys id_rsa; do
#        echo `date "+%Y-%m-%d %H:%M:%S"` transfer file $SSH_KEY/$key  | tee -a $LOG
#        wget -O $SSH_KEY/$key http://$PXE_SERVER/ssh/$key | tee -a $LOG
#done
#if [ -d $SSH_KEY ]; then
#	chmod 400 $SSH_KEY/ -R | tee -a $LOG
#fi

wget -O $OSPC_ROOT/puppet_deploy.sh http://$PXE_SERVER/postscript/puppet_deploy.sh
wget -O $OSPC_ROOT/ip_update.sh http://$PXE_SERVER/postscript/ip_update.sh
wget http://$PXE_SERVER/package/logmonitor.py -O /opt/logmonitor.py
chmod 777 $OSPC_ROOT/puppet_deploy.sh
chmod 777 $OSPC_ROOT/ip_update.sh
chmod 777 /opt/logmonitor.py
sed -i '/exit/d' /etc/rc.local
echo "sh $OSPC_ROOT/puppet_deploy.sh" >> /etc/rc.local
echo "sh $OSPX_ROOT/ip_update.sh" >> /etc/rc.local

#echo `date "+%Y-%m-%d %H:%M:%S"` Run puppet client and return host info  | tee -a $LOG
#dpkg -l puppet
#if [ -n "$?" ]; then
#	rm -rf /var/lib/puppet | tee -a $LOG
#	service puppet restart | tee -a $LOG
#	telnet 192.168.1.1 3335 &
#	IP=$STATIC_IP
#	DHCP_IP=`ifconfig | grep br100 -A1 | grep addr: | awk '{print $2}' | awk -F: '{print $2}'`
#	DISK_SIZE=`fdisk -l | grep GB | grep /dev/sda | awk '{print $3}'`
#	hostName=`hostname`
#	telnet 192.168.1.1 3336 &
#	sleep 3
#	echo "$IP:$DHCP_IP:$DISK_SIZE:$hostName" | nc 192.168.1.1 6666 
#else
#	echo "package puppet has not been installed."
#fi

#finish
echo
echo installation complete!
echo if there were problems with package installation and configuration due to
echo missing data directories, create/restore those directories and network failure 
echo run sh /opt/post.sh again to fix it.
echo
