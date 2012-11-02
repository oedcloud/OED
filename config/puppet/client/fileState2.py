#!/usr/bin/python

import os
import time
import threading

class FileState(threading.Thread):
	def __init__(self,filename):
		super(FileState,self).__init__()
		self.name = filename
	def run(self):
		while 1:
			dirlist = os.listdir(self.name)
			if not len(dirlist)==0:
				os.system("puppetca -as")
				print "update cert"
			time.sleep(3)

class NcListen(threading.Thread):
	def __init__(self):
		super(NcListen,self).__init__()
	def run(self):
		while 1:
			os.system("nc -l 6666 >> /etc/puppet/client_info")
			time.sleep(5)

if __name__ == "__main__":
	os.system("echo /dev/null > /etc/puppet/client_info")
	os.system("sh /etc/puppet/re_cert.sh")
	fs = FileState("/var/lib/puppet/ssl/ca/requests/")
	nl = NcListen()
	fs.start()
	nl.start()
