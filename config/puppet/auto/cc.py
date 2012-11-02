#!/usr/bin/python

import ConfigParser
import time
import os
import puppet_run

def cc_install():
	config = ConfigParser.RawConfigParser()
	config.read("deploy.conf")
	
	cc_host = config.get("cc","cc")
	hosts = config.get("all","clients").split(",")
	cc_deploy(cc_host,hosts,config)

def cc_deploy(cc_host,hosts,config):
	staticIP = config.get("pairs",cc_host).split(",")[1]
	os.system("sed -i 's/CCIP/%s/g' /etc/puppet/files/cc_deploy.sh" % (staticIP))
	os.system("sed -i 's/NODE/cc/g' /etc/puppet/manifests/site.pp")
	puppet_run.puppet_run(hosts)
	time.sleep(15)
	os.system("sed -i 's/cc/NODE/g' /etc/puppet/manifests/site.pp")
	os.system("sed -i 's/%s/CCIP/g' /etc/puppet/files/cc_deploy.sh" % (staticIP))

if __name__=="__main__":
	cc_install()
