#!/bin/bash

for ip in `seq 30`
do 
  ping -c 2 192.168.1.$ip
done
