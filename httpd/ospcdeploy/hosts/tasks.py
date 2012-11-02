from celery.task import task
from celery.task.sets import subtask
import logging
import os
from subprocess import Popen, PIPE
import time
from shutil import move,rmtree

logger = logging.getLogger("ospcdeploy.hosts.tasks")
printlog = lambda string: logger.info(string)
run_cmd = lambda cmd: Popen(cmd,stdout=PIPE, stderr=PIPE,shell=True) 
PROJ_ROOT = r"/pxeinstall/httpd/ospcdeploy/"
abs_path = lambda p: os.path.join(PROJ_ROOT,p)
CONFIG_ROOT = abs_path("config")
conf_path = lambda hostname: os.path.join(CONFIG_ROOT,hostname)

@task(ignore_result=True)
def puppet_run(host):
    uid = run_cmd("id")
    printlog(uid.communicate()[0])
    printlog("puppetrun to client host %s" % host)
    host+=".sh.intel.com"
    printlog("sudo /usr/sbin/puppetrun -p 10 --debug --host %s" % host)
    p = run_cmd("sudo /usr/sbin/puppetrun -p 10 --debug --host %s" % host)
    printlog(p.communicate()[0])

@task(ignore_result=True)
def puppet_clean(host):
    printlog("About to run puppetca clean %s" % host)
    host+=".sh.intel.com"
    printlog("sudo /usr/sbin/puppetca clean %s" % host)
    p = run_cmd("sudo /usr/sbin/puppetca clean %s" % host)
    printlog(p.communicate()[0])

def transfer(host):
    #new file transfer should be added in transfer.pp
    #new cmd should be added in ospc.sh
    printlog("copy config files. ")
    if os.path.exists(abs_path("localrc")):
        p = run_cmd("sudo cp %s /pxeinstall/puppet/files" % abs_path("localrc"))
        printlog(p.communicate()[0])
    else:
        printlog("localrc does not exist.")
    if os.path.exists(abs_path("localnc")):
        p = run_cmd("sudo cp %s /pxeinstall/puppet/files" % abs_path("localnc"))
        printlog(p.communicate()[0])
    else:
        printlog("localrc does not exist.")

    #printlog("copy localrc")
    #printlog(run_cmd("sudo sed -i 's/NODE/transfer/g' /etc/puppet/manifests/site.pp"))
    #printlog("begin to transfer files to host %s" % host)
    #time.sleep(250)
    #ret = subtask(callback).delay(host)
    #time.sleep(250)
    #if ret.ready():
    #    printlog("succeeded to transfer files.")
    #else:
    #    printlog("failed to transfer files with error msg %s " % host)
    #printlog(run_cmd("sudo sed -i 's/transfer/NODE/g' /etc/puppet/manifests/site.pp"))
    printlog("end function transfer()")

#clean the config dir from scratch
def clean_dir(path):
    for root, dirs, files in os.walk(path):
        try:
            for name in files:
                os.remove(os.path.join(root, name))
        except OSError, err:
            printlog('Error removing files in folder' % root)

#find certain hostname in deploy.pp file
def checkfile(words, path):
    with open(path,'r') as file:
        return file.read().find(words)

#move the src file to the dst folder
# src: source folder
# dst: dst folder
def transfer_configs(src,dst):
    try:
        if os.path.isdir(dst):
            rmtree(dst)
        move(src, dst)
    except OSError, err:
        if os.path.isdir(dst):
           pass
        else:
            printlog('Error moving %s to %s: %s' % (src, dst, err))


#for transfer localrc deploy file and execute install.sh 
@task(ignore_result=True)
def deploy(hosts, callback=puppet_run):
    puppet_dir = r'/pxeinstall/puppet/files'
    if isinstance(hosts, dict):
        #printlog(run_cmd("sudo sed -i 's/NODE/transfer/g' /etc/puppet/manifests/site.pp"))
        #for host in hosts["cc"] + hosts["nc"]:
        #    subtask(callback).delay(host)
        #printlog(run_cmd("sudo sed -i 's/transfer/NODE/g' /etc/puppet/manifests/site.pp"))
        #printlog("copy config files. ")
        #if os.path.exists(conf_path("localrc")):
            #clean the former config files
        #    try:
        #        clean_dir(puppet_folder)
        #        os.rename(conf_path("localrc"),os.path.join(puppet_folder,'localrc'))
        #    except OSError, err:
        #        pass
        #        printlog("Failed to move localrc to puppet folder with err %s " % err)
            #p = run_cmd("sudo cp %s /pxeinstall/puppet/files" % conf_path("localrc"))
            #printlog(p.communicate()[0])
        #else:
        #    printlog("localrc does not exist.")
        
        #if os.path.exists(conf_path("localnc")):
        #    p = run_cmd("sudo cp %s /pxeinstall/puppet/files" % abs_path("localnc"))
        #    printlog(p.communicate()[0])
        #else:
        #    printlog("localnc does not exist.")
        puppet_path = lambda hostname: os.path.join(puppet_dir,hostname)

        if hosts.has_key("cc"):
            printlog("copy config files... ")
#            clean_dir(puppet_dir)
#            transfer_configs(conf_path(hosts["cc"][0]),puppet_path(hosts["cc"][0]))
            
            printlog("add node cc to deploy.pp")
            if checkfile(hosts["cc"][0],r"/etc/puppet/manifests/deploy.pp") == -1:
                printlog(run_cmd("sudo echo -e node \"'%s.sh.intel.com'\" '{ \n  include deploy\n}' >> /etc/puppet/manifests/deploy.pp" % hosts["cc"][0]))

            ret = subtask(callback).delay(hosts["cc"][0])
            time.sleep(250)
            if ret.ready():
                printlog("succeeded to deploy cc.")
            else:
                printlog("failed to deploy cc on host %s " % hosts["cc"][0])
        
        if hosts.has_key("nc"):
            for host in hosts["nc"]:
                printlog("copy config file localnc_%s. " % host)
#                transfer_configs(conf_path(host),puppet_path(host))

                if checkfile(host,r"/etc/puppet/manifests/deploy.pp") == -1:
                    printlog(run_cmd("sudo echo -e node \"'%s.sh.intel.com'\" '{ \n  include deploy\n}' >> /etc/puppet/manifests/deploy.pp" % host))
                ret = subtask(callback).delay(host)
                if ret.ready():
                    printlog("succeeded to deploy nc on host %s." % host)
                else:
                    printlog("failed to deploy nc on host %s. " % host)
    else:
        printlog("hosts dict is incorrect. ")

