#!/usr/bin/python

import os
import time
import threading

class NcListen(threading.Thread):
	def __init__(self):
		super(NcListen,self).__init__()
	def run(self):
		while 1:
			os.system("nc -l 6666 >> /etc/puppet/client/client")

if __name__=="__main__":
	nl = NcListen()
	nl.start()
