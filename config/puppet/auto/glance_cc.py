#!/usr/bin/python

import ConfigParser
import os
import time
import puppet_run

def glance_cc_install():
	config = ConfigParser.RawConfigParser()
	config.read("deploy.conf")
	cc_host = config.get("cc","cc")
	glance_cc_host = config.get("glance_cc","glance_cc")
	glance_cc_deploy(cc_host,glance_cc_host,cc_host,config)

def glance_cc_deploy(target, glance_cc_host, cc_host, config):
	glanceIP = config.get("pairs", glance_cc_host).split(",")[1]
	ccIP = config.get("pairs", cc_host).split(",")[1]
	os.system("sed -i 's/GLANCEIP/%s/g' /etc/puppet/files/glance_cc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/CCIP/%s/g' /etc/puppet/files/glance_cc_deploy.sh" % (ccIP))
	os.system("sed -i 's/NODE/glance_cc/g' /etc/puppet/manifests/site.pp")
	puppet_run.puppet_run(target)
	time.sleep(15)
	os.system("sed -i 's/glance_cc/NODE/g' /etc/puppet/manifests/site.pp")
	os.system("sed -i 's/%s/GLANCEIP/' /etc/puppet/files/glance_cc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/%s/CCIP/g' /etc/puppet/files/glance_cc_deploy.sh" % (ccIP))

if __name__=="__main__":
	glance_cc_install()
