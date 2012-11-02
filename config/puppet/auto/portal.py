#!/usr/bin/python

import ConfigParser
import os
import time
import puppet_run

def portal_install():
	config = ConfigParser.RawConfigParser()
	config.read("deploy.conf")
	portal_host = config.get("portal","portal")
	portal_deploy(portal_host)

def portal_deploy(host):
	os.system("sed -i 's/NODE/portal/g' /etc/puppet/manifests/site.pp")
	puppet_run.puppet_run(host)
	time.sleep(15)
	os.system("sed -i 's/portal/NODE/g' /etc/puppet/manifests/site.pp")

if __name__=="__main__":
	portal_install()
