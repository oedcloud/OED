#!/usr/bin/python

import ConfigParser
import os
import sys
import time

def puppetrun(hosts=[]):
	if len(hosts)==0:
		for line in open("puppetrun.hosts"):
			os.system("puppetrun -p 10 --host %s" % (line))
	else:
		for host in hosts:
			os.system("puppetrun -p 10 --host %s" % (host))

def puppet_run():
	config = ConfigParser.RawConfigParser()
	config.read("deploy.conf")
	
	cc_host = config.get("cc","cc_client")
	hosts = config.get("all","clients").split(",")
	cc_deploy(cc_host,hosts,config)
	
	glance_cc_host = config.get("glance_cc","glance_cc_client")
	glance_cc_deploy(cc_host,glance_cc_host,cc_host,config)
	
	glance_nc_deploy(hosts,glance_cc_host,cc_host,config)
	
	portal_host = config.get("portal","portal_client")
	portal_deploy(portal_host)
	
	tomcat_deploy(portal_host,cc_host.split(".")[0]+":"+glance_cc_host.split(".")[0]+":"+portal_host.split(".")[0])

def cc_deploy(cc_host,hosts,config):
	staticIP = config.get("pairs",cc_host).split(",")[1]
	os.system("sed -i 's/CCIP/%s/g' /etc/puppet/files/cc_deploy.sh" % (staticIP))
	os.system("sed -i 's/NODE/cc/g' /etc/puppet/manifests/site.pp")
	#os.system("sed -i 's/CCNODES/%s/g' /etc/puppet/manifests/cc.pp" % (" ".join(hosts)))
	puppetrun(hosts)
	time.sleep(5)
	os.system("sed -i 's/cc/NODE/g' /etc/puppet/manifests/site.pp")
	#os.system("sed -i 's/%s/CCNODES/g' /etc/puppet/manifests/cc.pp" % (" ".join(hosts)))
	os.system("sed -i 's/%s/CCIP/g' /etc/puppet/files/cc_deploy.sh" % (staticIP))

def glance_cc_deploy(target, glance_cc_host, cc_host, config):
	glanceIP = config.get("pairs", glance_cc_host).split(",")[1]
	ccIP = config.get("pairs", cc_host).split(",")[1]
	os.system("sed -i 's/GLANCEIP/%s/g' /etc/puppet/files/glance_cc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/CCIP/%s/g' /etc/puppet/files/glance_cc_deploy.sh" % (ccIP))
	os.system("sed -i 's/NODE/glance_cc/g' /etc/puppet/manifests/site.pp")
	if isinstance(target,list):
		#os.system("sed -i 's/GLANCECCNODES/%s/g' /etc/puppet/manifests/glance_cc.pp" % (" ".join(target)))
		puppetrun(target)
		#os.system("sed -i 's/%s/GLANCECCNODES/g' /etc/puppet/manifests/glance_cc.pp" % (" ".join(target)))
	else:
		#os.system("sed -i 's/GLANCECCNODES/%s/g' /etc/puppet/manifests/glance_cc.pp" % (target))
		puppetrun([target])
		#os.system("sed -i 's/%s/GLANCECCNODES/g' /etc/puppet/manifests/glance_cc.pp" % (target))
	time.sleep(5)
	os.system("sed -i 's/glance_cc/NODE/g' /etc/puppet/manifests/site.pp")
	os.system("sed -i 's/%s/GLANCEIP/g' /etc/puppet/files/glance_cc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/%s/CCIP/g' /etc/puppet/files/glance_cc_deploy.sh" % (ccIP))

def glance_nc_deploy(hosts, glance_cc_host, cc_host, config):
	confstr = ""
	print hosts
	#confstr = cc_host.split(".")[0]+","+config.get("pairs",cc_host)+"*"
	for host in hosts:
		confstr += host.split(".")[0]+","+config.get("pairs",host)+"*"
	os.system("sed -i 's/CONFIG/%s/g' /etc/puppet/files/glance_nc_deploy.sh" % (confstr.rstrip("*")))
	#os.system("sed -i 's/GLANCENCNODES/%s/g' /etc/puppet/manifests/glance_nc.pp" % (cc_host))
	os.system("sed -i 's/NODE/glance_nc/g' /etc/puppet/manifests/site.pp")
	puppetrun([cc_host])
	time.sleep(5)
	os.system("sed -i 's/%s/CONFIG/g' /etc/puppet/files/glance_nc_deploy.sh" % (confstr.rstrip("*")))
	#os.system("sed -i 's/%s/GLANCENCNODES/g' /etc/puppet/manifests/glance_nc.pp" % (cc_host))
	os.system("sed -i 's/glance_nc/NODE/g' /etc/puppet/manifests/site.pp")
	hosts.remove(cc_host)
	if hosts:
		glance_cc_deploy(hosts, glance_cc_host, cc_host, config)

def portal_deploy(host):
	#os.system("sed -i 's/PORTALNODE/%s/g' /etc/puppet/manifests/portal.pp" % (host))
	os.system("sed -i 's/NODE/portal/g' /etc/puppet/manifests/site.pp")
	puppetrun([host])
	time.sleep(5)
	#os.system("sed -i 's/%s/PORTALNODE/g' /etc/puppet/manifests/portal.pp" % (host))
	os.system("sed -i 's/portal/NODE/g' /etc/puppet/manifests/site.pp")

def tomcat_deploy(portal_host,hostnames):
	os.system("sed -i 's/HOSTNAME/%s/g' /etc/puppet/files/tomcat_deploy.sh" % (hostnames))
	#os.system("sed -i 's/TOMCATNODE/%s/g' /etc/puppet/manifests/tomcat.pp" % (portal_host))
	os.system("sed -i 's/NODE/tomcat/g' /etc/puppet/manifests/site.pp")
	puppetrun([portal_host])
	time.sleep(5)
	os.system("sed -i 's/%s/HOSTNAME/g' /etc/puppet/files/tomcat_deploy.sh" % (hostnames))
	#os.system("sed -i 's/%s/TOMCATNODE/g' /etc/puppet/manifests/tomcat.pp" % (portal_host))
	os.system("sed -i 's/tomcat/NODE/g' /etc/puppet/manifests/site.pp")

if __name__=="__main__":
	puppet_run()
