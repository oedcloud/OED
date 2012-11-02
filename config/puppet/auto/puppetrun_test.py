#!/usr/bin/python

import puppet_run

if __name__=="__main__":
    import os
    import time
    import sys
    host = sys.argv[1]
    os.system("sed -i 's/NODE/transfer/g' /etc/puppet/manifests/site.pp")
    message=puppet_run.puppet_run(host)
    time.sleep(250)
    #os.system("sed -i 's/transfer/ospc/g' /etc/puppet/manifests/site.pp")
    #puppet_run.puppet_run(host)
    #time.sleep(45)
    os.system("sed -i 's/transfer/NODE/g' /etc/puppet/manifests/site.pp")
