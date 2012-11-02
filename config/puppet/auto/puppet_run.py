#!/usr/bin/python

import os
import sys

def puppet_run(hosts):
	logfile="/tmp/tmptest.log"
	if not isinstance(hosts,list):
		os.system("puppetrun -p 10 --host %s | tee -a %s" % (hosts,logfile))
	else:
		for host in hosts:
			os.system("puppetrun -p 10 --host %s | tee -a %s" % (host,logfile))

if __name__=="__main__":
	puppet_run(sys.argv[1:])
