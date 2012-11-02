#!/bin/sh

rm -rf /var/lib/puppet/
service puppetmaster restart
puppetca -as
