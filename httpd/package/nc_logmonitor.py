#!/usr/bin/python

import os
import time

#logfile=r'/opt/inst-deploy.log'
logfile=r'/tmp/tmp.txt'

def nc_transport(line):
    hostname = os.popen("hostname").read().rstrip()
    os.system("telnet 192.168.1.1 3337 &")
    time.sleep(5)
    os.system('echo "%s:%s" | nc 192.168.1.1 9999' % (hostname,line))

def log_read():
    try:
        with open(logfile, 'r+') as log:
            while 1:
                data = log.readline()
                print data
                if not data:
                    break
                else:
                    nc_transport(data)
    except IOError, e:
        print "Failed to open file %s" % e
        return

if __name__=="__main__":
    #hostname = os.popen("hostname").read().rstrip()
    #print hostname
    log_read()
