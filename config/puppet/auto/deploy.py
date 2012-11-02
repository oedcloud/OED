#!/usr/bin/python

import ConfigParser
import os

def readClients(domain=".sh.intel.com"):
	config = ConfigParser.RawConfigParser()
	staticIPs = []
	dhcpIPs = []
	hostnames = []
	for line in open("/pxeserver/nfsroot/clientInfo/client"):
		items = line.strip().split(":")
		staticIPs.append(items[0])
		dhcpIPs.append(items[1])
		hostnames.append(items[3]+domain)
		os.system("echo '%s\t%s' >> /etc/hosts" %(staticIPs[len(staticIPs)-1],hostnames[len(hostnames)-1]))
	config.add_section("pairs")
	config.add_section("all")
	config.add_section("cc")
	config.add_section("glance_cc")
	config.add_section("portal")
	config.set("all","clients",",".join(hostnames))
	if len(hostnames) >= 3:
		config.set("cc","cc",hostnames[0])
		config.set("glance_cc","glance_cc",hostnames[1])
		config.set("portal","portal",hostnames[2])
	else:
		config.set("cc","cc",hostnames[0])
		config.set("glance_cc","glance_cc",hostnames[0])
		config.set("portal","portal",hostnames[0])
	for i in range(len((staticIPs))):
		config.set("pairs",hostnames[i],dhcpIPs[i]+","+staticIPs[i])
	with open("/etc/puppet/auto/deploy.conf",'w') as configfile:
		config.write(configfile)

if __name__=="__main__":
	readClients()
	#os.system("cp /pxeserver/nfsroot/clientInfo/deploy.conf /etc/puppet/auto/")
