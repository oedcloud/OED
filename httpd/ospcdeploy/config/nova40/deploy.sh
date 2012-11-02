#!/bin/bash

set -e
LOGFILE=/opt/deploy.log
PKG_NAME=ospc.tar.gz
ROOT=/opt
HTTP_URL=http://pxeserver/puppet
SERVER_IP=192.168.1.1
INSTALL_ROOT=/opt/stack
DEPLOY_ROOT=$INSTALL_ROOT/devstack/

if [ -n "`ping -c 3 $SERVER_IP`" ]; then
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
   cd $ROOT/ospc && ./install.sh | tee -a $LOGFILE
   
   if [ ! -n "$?" ]; then
        echo `date "+%Y-%m-%d %H:%M:%S"` "Installation error." | tee -a $LOGFILE
        exit 1
   else
       echo `date "+%Y-%m-%d %H:%M:%S"` "Running stack.sh." | tee -a $LOGFILE
       cp $ROOT/localrc $DEPLOY_ROOT | tee -a $LOGFILE
       cd $DEPLOY_ROOT && ./stack.sh | tee -a $LOGFILE
       if [ ! -n "$?" ]; then
        echo `date "+%Y-%m-%d %H:%M:%S"` "Software deployment error." | tee -a $LOGFILE
        exit 1
       fi
   fi
else
   echo `date "+%Y-%m-%d %H:%M:%S"` "localrc does not exist." | tee -a $LOGFILE
fi

echo 
echo `date "+%Y-%m-%d %H:%M:%S"` "File transfer done." | tee -a $LOGFILE
echo

exit 0
