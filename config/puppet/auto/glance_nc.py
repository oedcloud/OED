#!/usr/bin/python

import ConfigParser
import os
import time
import puppet_run
import glance_cc

def glance_nc_install():
	config = ConfigParser.RawConfigParser()
	config.read("deploy.conf")
	cc_host = config.get("cc","cc")
	hosts = config.get("all","clients").split(",")
	glance_cc_host = config.get("glance_cc","glance_cc")
	glance_nc_deploy(hosts,glance_cc_host,cc_host,config)

def glance_nc_deploy(hosts, glance_cc_host, cc_host, config):
	glanceIP = config.get("pairs",glance_cc_host).split(",")[1]
	confstr = ""
	for host in hosts:
		confstr += host.split(".")[0]+","+config.get("pairs",host)+"*"
	os.system("sed -i 's/CONFIG/%s/g' /etc/puppet/files/glance_nc_deploy.sh" % (confstr.rstrip("*")))
	os.system("sed -i 's/GLANCEIP/%s/g' /etc/puppet/files/glance_nc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/NODE/glance_nc/g' /etc/puppet/manifests/site.pp")
	puppet_run.puppet_run(cc_host)
	time.sleep(30)
	os.system("sed -i 's/%s/CONFIG/g' /etc/puppet/files/glance_nc_deploy.sh" % (confstr.rstrip("*")))
	os.system("sed -i 's/%s/GLANCEIP/g' /etc/puppet/files/glance_nc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/glance_nc/NODE/g' /etc/puppet/manifests/site.pp")
	tmpHosts = hosts[:]
	tmpHosts.remove(cc_host)
	if tmpHosts:
		glance_cc.glance_cc_deploy(tmpHosts, glance_cc_host, cc_host, config)

if __name__=="__main__":
	glance_nc_install()
