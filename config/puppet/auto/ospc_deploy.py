#!/usr/bin/python

import ConfigParser
import time
import os
import stat

def puppet_run(hosts):
	if not isinstance(hosts,list):
		os.system("puppetrun -p 10 --host %s" % (hosts))
	else:
		for host in hosts:
			os.system("puppetrun -p 10 --host %s" % (host))

def ospc_deploy():
	config = ConfigParser.RawConfigParser()
	config.read("deploy.conf")
	cc_host = config.get("cc","cc")
	glance_cc_host = config.get("glance_cc","glance_cc")
	portal_host = config.get("portal","portal")
	hosts = config.get("all","clients").split(",")
	
	filename = "/pxeserver/nfsroot/clientInfo/infoInstall"
	lastModified = os.stat(filename)[stat.ST_MTIME]
	print "install cc..."
	cc_deploy(cc_host,hosts,config)
	lastModified = fileState(lastModified,filename)
	print "install cc finished"
	print "wait 30 seconds for the pre-puppetrun ask time out..."
	time.sleep(30)
	print "install glance cc..."
	glance_cc_deploy(cc_host,glance_cc_host,cc_host,config)
	lastModified = fileState(lastModified,filename)
	print "install glance cc finished"
	print "wait 30 seconds..."
	time.sleep(30)
	print "install glance nc"
	glance_nc_deploy(hosts,glance_cc_host,cc_host,config)
	lastModified = fileState(lastModified,filename)
	time.sleep(20)
	print "install glance nc finished"
	print "wait 30 seconds..."
	time.sleep(30)
	print "install portal"
	portal_deploy(portal_host)
	lastModified = fileState(lastModified,filename)
	print "install portal finished"
	print "wait 30 seconds..."
	time.sleep(30)
	print "start tomcat service..."
	tomcat_deploy(portal_host,cc_host.split(".")[0]+":"+glance_cc_host.split(".")[0]+":"+portal_host.split(".")[0])
	lastModified = fileState(lastModified,filename)
	print "tomcat service started"
	
	

def fileState(lastModified,filename):
	tmpModified = 0
	while 1:
		tmpModified = os.stat(filename)[stat.ST_MTIME]
		if tmpModified > lastModified:
			break
		else:
			time.sleep(20)
	return tmpModified

def cc_deploy(cc_host, hosts, config):
	staticIP = config.get("pairs",cc_host).split(",")[1]
	os.system("sed -i 's/CCIP/%s/g' /etc/puppet/files/cc_deploy.sh" % (staticIP))
	os.system("sed -i 's/NODE/cc/g' /etc/puppet/manifests/site.pp")
	puppet_run(hosts)
	time.sleep(30)
	os.system("sed -i 's/cc/NODE/g' /etc/puppet/manifests/site.pp")
	os.system("sed -i 's/%s/CCIP/g' /etc/puppet/files/cc_deploy.sh" % (staticIP))

def glance_cc_deploy(target, glance_cc_host, cc_host, config):
	glanceIP = config.get("pairs", glance_cc_host).split(",")[1]
	ccIP = config.get("pairs", cc_host).split(",")[1]
	os.system("sed -i 's/GLANCEIP/%s/g' /etc/puppet/files/glance_cc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/CCIP/%s/g' /etc/puppet/files/glance_cc_deploy.sh" % (ccIP))
	os.system("sed -i 's/NODE/glance_cc/g' /etc/puppet/manifests/site.pp")
	puppet_run(target)
	time.sleep(30)
	os.system("sed -i 's/glance_cc/NODE/g' /etc/puppet/manifests/site.pp")
	os.system("sed -i 's/%s/GLANCEIP/' /etc/puppet/files/glance_cc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/%s/CCIP/g' /etc/puppet/files/glance_cc_deploy.sh" % (ccIP))

def glance_nc_deploy(hosts, glance_cc_host, cc_host, config):
	glanceIP = config.get("pairs", glance_cc_host).split(",")[1]
	confstr = ""
	for host in hosts:
		confstr += host.split(".")[0]+","+config.get("pairs",host)+"*"
	os.system("sed -i 's/CONFIG/%s/g' /etc/puppet/files/glance_nc_deploy.sh" % (confstr.rstrip("*")))
	os.system("sed -i 's/GLANCEIP/%s/g' /etc/puppet/files/glance_nc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/NODE/glance_nc/g' /etc/puppet/manifests/site.pp")
	puppet_run(cc_host)
	time.sleep(30)
	os.system("sed -i 's/%s/CONFIG/g' /etc/puppet/files/glance_nc_deploy.sh" % (confstr.rstrip("*")))
	os.system("sed -i 's/%s/GLANCEIP/g' /etc/puppet/files/glance_nc_deploy.sh" % (glanceIP))
	os.system("sed -i 's/glance_nc/NODE/g' /etc/puppet/manifests/site.pp")
	tmpHosts = hosts[:]
	tmpHosts.remove(cc_host)
	if tmpHosts:
		os.system("sed -i -e '5 s/^/#/' /etc/puppet/files/glance_cc_deploy.sh")
		glance_cc_deploy(tmpHosts, glance_cc_host, cc_host, config)
		os.system("sed -i -e '5 s/#//' /etc/puppet/files/glance_cc_deploy.sh")

def portal_deploy(host):
	os.system("sed -i 's/NODE/portal/g' /etc/puppet/manifests/site.pp")
	puppet_run(host)
	time.sleep(30)
	os.system("sed -i 's/portal/NODE/g' /etc/puppet/manifests/site.pp")

def tomcat_deploy(portal_host,hostnames):
	os.system("sed -i 's/HOSTNAME/%s/g' /etc/puppet/files/tomcat_deploy.sh" % (hostnames))
	os.system("sed -i 's/NODE/tomcat/g' /etc/puppet/manifests/site.pp")
	puppet_run(portal_host)
	time.sleep(30)
	os.system("sed -i 's/%s/HOSTNAME/g' /etc/puppet/files/tomcat_deploy.sh" % (hostnames))
	os.system("sed -i 's/tomcat/NODE/g' /etc/puppet/manifests/site.pp")

if __name__ == "__main__":
	ospc_deploy()
