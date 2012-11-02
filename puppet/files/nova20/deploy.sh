#!/bin/bash

set -e
LOGFILE=/opt/inst-deploy.log
PKG_NAME=ospc.tar.gz
ROOT=/opt
HTTP_URL=http://pxeserver/puppet
SERVER_IP=192.168.1.1
INSTALL_ROOT=/opt/stack
DEPLOY_ROOT=$INSTALL_ROOT/devstack/

STATIC_IP=`ifconfig eth0 | grep 'inet addr'  | awk '{print $2}' | awk -F: '{print $2}'`
DHCP_IP=`ifconfig | grep br100 -A1 | grep addr: | awk '{print $2}' | awk -F: '{print $2}'`
hostName=`hostname`

function nc_message()
{
    flag=$1
    message=$2
    telnet 192.168.1.1 3336 &
    sleep 2
    echo "$flag:$STATIC_IP:$DHCP_IP:$hostName:$message" | nc 192.168.1.1 6666
}

nc_message "1" "installing"

if [  -n "`ping -c 3 $SERVER_IP`" ]; then
    wget -O $ROOT/$PKG_NAME $HTTP_URL/$PKG_NAME | tee -a $LOGFILE
    if [ ! -n "$?" ]; then
        echo `date "+%Y-%m-%d %H:%M:%S"` "Failed to download the deployment package. Are you sure it exists?" | tee -a $LOGFILE
        exit 1
    else
        echo `date "+%Y-%m-%d %H:%M:%S"` "Transformation done." | tee -a $LOGFILE
        #[[ -d $INSTALL_ROOT ]] && rm -rfv $INSTALL_ROOT | tee -a $LOGFILE
        tar zvxf $ROOT/$PKG_NAME -C $ROOT 
    fi
else
    echo `date "+%Y-%m-%d %H:%M:%S"` "Deployment Server can't be reached, plz check your network." | tee -a $LOGFILE
    exit 1
fi

if [ -f $ROOT/localrc ]; then 
   
   #[[ -d $INSTALL_ROOT ]] && rm -rfv $INSTALL_ROOT | tee -a $LOGFILE 

   #mkdir -p $INSTALL_ROOT
   echo `date "+%Y-%m-%d %H:%M:%S"` "Begin configuration." | tee -a $LOGFILE

   #cp $ROOT/localrc $DEPLOY_ROOT | tee -a $LOGFILE
   
   #executing install.sh
   echo `date "+%Y-%m-%d %H:%M:%S"` "Running install.sh." | tee -a $LOGFILE
   olddir=`pwd`
   cd $ROOT/ospc
   ./install.sh >>$LOGFILE 2>&1
   cd $olddir
   
   echo `date "+%Y-%m-%d %H:%M:%S"` "Running stack.sh." | tee -a $LOGFILE
   cp -rfv $ROOT/localrc $DEPLOY_ROOT | tee -a $LOGFILE
   echo "exit; exit; exit;" >> $DEPLOY_ROOT/stack.sh
   olddir=`pwd`
   cd $DEPLOY_ROOT
   ./stack.sh >>$LOGFILE 2>&1
   cd $olddir
   nc_message "1" "Finished"
fi
#stop logmonitor process
#ps aux | grep -v "grep" | grep "logmonitor" | awk '{print $2}'| xargs -i kill -9 {}

#rebooting nova-compute service
ps aux | grep -v "grep" | grep "nova-compute" | grep -v "deploy.sh" | awk '{print $2}' | xargs -i kill -9 {}
nohup python /opt/stack/nova/bin/nova-compute --flagfile=/etc/nova/nova.conf --logfile=/var/log/nova/nova-compute.log>/var/log/nova/nova-compute.log 2>&1 &
exit 0
