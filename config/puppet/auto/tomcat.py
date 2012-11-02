#!/usr/bin/python

import ConfigParser
import os
import time
import puppet_run

def tomcat_install():
	config = ConfigParser.RawConfigParser()
	config.read("deploy.conf")
	cc_host = config.get("cc","cc")
	glance_cc_host = config.get("glance_cc","glance_cc")
	portal_host = config.get("portal","portal")
	tomcat_deploy(portal_host,cc_host.split(".")[0]+":"+glance_cc_host.split(".")[0]+":"+portal_host.split(".")[0])

def tomcat_deploy(portal_host,hostnames):
	os.system("sed -i 's/HOSTNAME/%s/g' /etc/puppet/files/tomcat_deploy.sh" % (hostnames))
	os.system("sed -i 's/NODE/tomcat/g' /etc/puppet/manifests/site.pp")
	puppet_run.puppet_run(portal_host)
	time.sleep(15)
	os.system("sed -i 's/%s/HOSTNAME/g' /etc/puppet/files/tomcat_deploy.sh" % (hostnames))
	os.system("sed -i 's/tomcat/NODE/g' /etc/puppet/manifests/site.pp")

if __name__=="__main__":
	tomcat_install()
