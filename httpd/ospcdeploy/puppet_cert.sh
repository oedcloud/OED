#!/bin/bash

LOG=/pxeinstall/httpd/ospcdeploy/puppet_cert.log

#while test 1; do
#  fn=`ls /var/lib/puppet/ssl/ca/requests/ | wc -l`
  #echo $fn
#  if [ "$fn" -gt 0 ]; then
puppetca -as | tee -a $LOG
#    exit 0
#  fi
#done
