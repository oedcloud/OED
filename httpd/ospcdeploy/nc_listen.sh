#!/bin/bash

#nc -l 6666 >> /etc/puppet/client_info

info=`nc -l 6666`
OLD_IFS="$IFS"
IFS=":"
arr=($info)
IFS="$OLD_IFS"
flag=${arr[0]}
static_ip=${arr[1]}
dhcp_ip=${arr[2]}
host_name=${arr[3]}
message=${arr[4]}
log=/tmp/nc_listen.log
sta=`sqlite3 /pxeinstall/httpd/ospcdeploy/hosts.db 'select status from hosts_hosts where hostname="'$host_name'";'`

if [ "$flag" -eq "0" ];then
if [ -n "$host_name" ];then

echo -e "$static_ip\t$host_name\t$host_name.sh.intel.com" >> /etc/hosts | tee -a $log

sqlite3 /pxeinstall/httpd/ospcdeploy/hosts.db 'delete from hosts_hosts where hostname="'$host_name'";' | tee -a $log

if [ $? -eq 0 ]; then
    puppetca clean $host_name.sh.intel.com | tee -a $log
fi

sqlite3 /pxeinstall/httpd/ospcdeploy/hosts.db 'insert into hosts_hosts(hostname, static_ip, dhcp_ip, timestamp, status) values("'$host_name'","'$static_ip'","'$dhcp_ip'",CURRENT_TIMESTAMP,"'$message'");' | tee -a $log
fi
fi


if [ "$flag" -eq "1" ];then
if [ "$sta" != "Finished" ];then
sqlite3 /pxeinstall/httpd/ospcdeploy/hosts.db 'update hosts_hosts set status="'$message'" where hostname="'$host_name'";'
fi
fi

if [ "$flag" -eq "2" ];then
sqlite3 /pxeinstall/httpd/ospcdeploy/hosts.db 'update hosts_hosts set dhcp_ip="'$dhcp_ip'" where hostname="'$host_name'";'
fi
