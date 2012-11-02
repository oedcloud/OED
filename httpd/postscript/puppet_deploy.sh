#!/bin/sh
PXE_SERVER=192.168.1.1
LOG=/opt/ospc/post.log
PUPPET_CONF=/etc/puppet
STATIC_IP=`ifconfig eth0 | grep 'inet addr'  | awk '{print $2}' | awk -F: '{print $2}'`
SSH_KEY=/root/.ssh
SSH_CONF=/etc/ssh/ssh_config

apt-get update
echo `date "+%Y-%m-%d %H:%M:%S"` Install new packages | tee -a $LOG
apt-get install -y --force-yes puppet | tee -a $LOG
apt-get install -y --force-yes vim
apt-get install -y --force-yes bridge-utils

echo `date "+%Y-%m-%d %H:%M:%S"` SSH key pair  | tee -a $LOG
sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/" $SSH_CONF
mkdir -p $SSH_KEY/
for key in authorized_keys id_rsa; do
        echo `date "+%Y-%m-%d %H:%M:%S"` transfer file $SSH_KEY/$key  | tee -a $LOG
        wget -O $SSH_KEY/$key http://$PXE_SERVER/ssh/$key | tee -a $LOG
done
if [ -d $SSH_KEY ]; then
        chmod 400 $SSH_KEY/ -R | tee -a $LOG
fi

echo `date "+%Y-%m-%d %H:%M:%S"` Transfer puppet config file  | tee -a $LOG
for file in auth.conf puppet.conf namespaceauth.conf; do
        echo `date "+%Y-%m-%d %H:%M:%S"` transfer file $file  | tee -a $LOG
        wget -O $PUPPET_CONF/$file http://$PXE_SERVER/puppet/$file | tee -a $LOG
done

echo `date "+%Y-%m-%d %H:%M:%S"` Sync datetime with ntp server  | tee -a $LOG
ntpdate -u 192.168.1.1 | tee -a $LOG

echo `date "+%Y-%m-%d %H:%M:%S"` Change puppet conf  | tee -a $LOG
sed -i "s/START=no/START=yes/" /etc/default/puppet | tee -a $LOG

echo `date "+%Y-%m-%d %H:%M:%S"` Run puppet client and return host info  | tee -a $LOG
dpkg -l puppet
if [ -n "$?" ]; then
	#service puppet stop
        #rm -rf /var/lib/puppet/ssl | tee -a $LOG
        #puppetd --no-client | tee -a $LOG
        #sign the ca
        #telnet 192.168.1.1 3335 &
        IP=$STATIC_IP
        DHCP_IP=`ifconfig | grep br100 -A1 | grep addr: | awk '{print $2}' | awk -F: '{print $2}'`
        #DISK_SIZE=`fdisk -l | grep GB | grep /dev/sda | awk '{print $3}'`
        hostName=`hostname`
        flag="0"
        message="ready"
        #register host
        telnet 192.168.1.1 3336 &
        sleep 3
        echo "$flag:$IP:$DHCP_IP:$hostName:$message" | nc 192.168.1.1 6666
        sleep 5
        service puppet stop | tee -a $LOG
        rm -rf /var/lib/puppet/ssl | tee -a $LOG
        puppetd --no-client | tee -a $LOG
else
        echo "package puppet has not been installed."
fi

#wget http://$PXE_SERVER/package/logmonitor.py -O /opt/logmonitor.py
#python /opt/logmonitor.py &> /opt/ospc/post.log &

sed -i '/puppet_deploy/d' /etc/rc.local

#begin log file track
touch /opt/inst-deploy.log 
if [ -f /opt/logmonitor.py ]; then
    /usr/bin/python /opt/logmonitor.py &
fi
#tail -f /opt/inst-deploy.log | nc -l 7777 &

echo
echo "OS is ready for openstack installation."
echo
#reboot
