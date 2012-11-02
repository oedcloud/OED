# Create your views here.
#from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from forms import HostForm
from django.template import RequestContext
from tables import HostTable
from models import Hosts
from ospcdeploy.hosts.tasks import puppet_run,puppet_clean,deploy
from django.http import HttpResponse
from subprocess import Popen, PIPE
import mmap
import os
import sys
import time
import logging
import string
import random
import shutil
import socket

PROJ_ROOT = r"/pxeinstall/httpd/ospcdeploy/"
abs_path = lambda p: os.path.join(PROJ_ROOT,p)
LOG_FILE = abs_path("ospcdeploy.log")
CONFIG_ROOT = r'/pxeinstall/puppet/files'
conf_path = lambda p:os.path.join(CONFIG_ROOT, p)
logger = logging.getLogger("ospcdeploy.hosts.views")


def ospcdeploy(request):    
    extras = []
    #hosts = get_object_or_404(Hosts,hostname=request.POST['hostname'])
    if request.method == 'POST':
        # submit to setting the roles of the hosts
        #logger.info("To update the Hostform.")
        post = request.POST
        if 'refresh' in post:
            form = HostForm() 

        if 'update' in post:
            #logs = readlog()
            try:
                logger.info("To update the Hostform.")
                host = Hosts.objects.get(hostname=post['hostname'])
                form = HostForm(request.POST,instance=host)
                if form.is_valid():
                    logger.info("Hosts has been updated.")
                    form.save()
            except Hosts.DoesNotExist:
                form = HostForm()
                logger.warning("Hostname doesnot exists.")

        #delete the certain items in the Hosts table.  
        if 'delete' in post:
            try:
                logger.info("To delete the certain host in table.")
                host = Hosts.objects.get(hostname=post['hostname'])
                host.delete()
            except Hosts.DoesNotExist:
                #form = HostForm()
                logger.warning("Hostname doesnot exists.")    
            form = HostForm()
            if post['hostname']:
                puppet_clean.delay(post['hostname'])
                logger.info("trigger puppetca clean %s" % post['hostname'])        
                
        # make the config file in the project root for CC and NC (localrc and localnc) 
        if 'config' in post:
            logger.info("To configure localrc and localnc.")
            hosts = Hosts.objects.exclude(role='').order_by('role')
            form = HostForm()
            if hosts.count() > 0:
                confs = configuration(hosts)
                extras = "-----------CC Config-----------\n"
                extras += confs[0] 
                if len(confs) > 1:
                    extras += "\n-----------NC Config-----------\n"
                for conf in confs[1:]:
                    extras += conf

        # deployment phase can be divided into 2 parts: transportation and execution
        if 'deploy' in post:
            logs = None
            cc = []
            nc = []
            flag = 0 
            host_map = {}
            form = HostForm()
            logger.info("To deploy the client hosts.")
            hosts = Hosts.objects.exclude(role='').order_by('role')
            if hosts.count() > 0:
                for host in hosts:
                    if host.role == '1': 
                        if os.path.exists(os.path.join(conf_path(host.hostname),'localrc')):
                            logger.info("CC host %s" % host.hostname)
                            cc.append(host.hostname)
                            host_map["cc"] = cc
                        else:
                            flag = 1
                            logger.error("The config file %s does not exists, plz generate the config file first." % host.hostname )
                            logs = "The config file %s does not exists, plz generate the config file first." % host.hostname

                    if host.role =='2':
                        if os.path.exists(os.path.join(conf_path(host.hostname),'localrc')):
                            logger.info("NC host %s" % host.hostname)
                            nc.append(host.hostname)
                        else:
                            flag = 1
                            logger.error("The config file %s does not exists, plz generate the config file first." % host.hostname )
                            logs = "The config file %s does not exists, plz generate the config file first." % host.hostname

                    if flag == 0:
                        host_map["nc"] = nc
                        deploy.delay(host_map)
                        logger.info("tasks triggered.")
                else:
                    logs = "There is no cc defined."                        
            else: 
                logs = "No hosts got configured."
            if logs == None:
                logs = readlog()
       
        if 'single-config' in post:
            logger.info("To configure localrc and localnc for single host.")
            try:
                cc = Hosts.objects.get(role='1')
                host = Hosts.objects.filter(hostname=post['hostname'])
                confs = configuration(host, [cc.dhcp_ip,cc.static_ip])
                if post['hostname'] == cc.hostname:
                    extras = "-----------CC Config-----------\n"
                else:
                    extras = "-----------NC Config-----------\n"
                extras += confs[0]
                    
            except Hosts.DoesNotExist:
                extras = "Error: can\'t find CC"
                logger.error("CC doesnot exists.")
            form = HostForm()
        
        if 'single-deploy' in post:
            logger.info("To deploy compute node %s" % post['hostname'])
            form = HostForm()
            host_map = {}
            logs = None
            try:
                logger.info("Begin deploy compute node %s" % post['hostname'])
                host = Hosts.objects.get(hostname=post['hostname'])
                flag = 0
                if host.role == '1':
                    if os.path.exists(os.path.join(conf_path(host.hostname),'localrc')):
                        logger.info("CC host %s" % host.hostname)
                        cc = []
                        cc.append(host.hostname)
                        host_map["cc"] = cc
                    else:
                        flag = 1
                        logger.error("The config file localrc does not exists, plz generate the config file first.")
                        logs = "The config file localrc does not exists, plz generate the config file first."
                if host.role == '2':    
                    if os.path.exists(os.path.join(conf_path(host.hostname),'localrc')):
                        host_map["nc"] = host.hostname
                        nc = []
                        nc.append(host.hostname)
                        host_map["nc"] = nc
                    else:
                        flag = 1
                        logger.error("The config file localrc does not exists, plz generate the config file first.")
                        logs = "The config file localrc does not exists, plz generate the config file first."    
                
                if flag == 0:
                    deploy.delay(host_map)
                    logger.info("single task triggered.")
                
            except Hosts.DoesNotExist:
                logs = "The host is invalid."
            if logs == None:
                logs = readlog()      
 
    else:
        form = HostForm()
    
    # bind the object to table
    init_queryset = Hosts.objects.all()
    table = HostTable(
            init_queryset,
            order_by=request.GET.get('sort','hostname'))

    return render_to_response('ospcdeploy.html',locals(),RequestContext(request))

def gen_password(size=20,chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

#gen password for nova, mysql, rabbitmq, swift and xen
#  generator = true:  gen a set of passwd
#  generator = false: fetch/load the passwd directly
def gen_passwdrc(generator = True):
    try:
        if generator:
            with open(conf_path('passwordrc'),'w+') as passwdrc:
                for var in ["RABBIT_PASSWORD","MYSQL_PASSWORD","SWIFT_HASH","SERVICE_TOKEN","ADMIN_PASSWORD","XENAPI_PASSWORD"]:
                    #passwdrc.write(var + '=' + gen_password() + u'\n')
                    passwdrc.write(var + '=' + "nova" + u'\n')
        
        with open(conf_path('passwordrc'),'r') as passwdrc:                    
            return passwdrc.read()   
    except IOError:
        raise 
        logger.error("Failed to open passwordrc file.")
    
def clean_dir(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            os.remove(os.path.join(root, name))

def mk_dir(dirname):
    try:
        logger.info("Making directory %s", dirname)
        os.umask(0)
        os.mkdir(dirname,0777)
    except OSError:
        if os.path.isdir(dirname):
        # We are nearly safe
            pass
        else:
        # There was an error on creation, so make sure we know about it
            raise
            logger.error("Failed to create the client directory")
    logger.info("Copy script file deploy.sh to %s" % dirname)
    shutil.copy2(os.path.join(PROJ_ROOT,"deploy.sh"),dirname)    

def configuration(hosts,cc=None):
    extras = []
    nc = []
    #get_root = lambda p: os.path.join(PROJ_ROOT,p)
    for host in hosts:
        if host.role == '1':
            # clean the config path
            clean_dir(CONFIG_ROOT)
            mk_dir(conf_path(host.hostname))
            cc = [host.dhcp_ip,host.static_ip]
            try:
                with open(os.path.join(conf_path(host.hostname),'localrc'),'w+') as cc_file:
                    extra = '''HOST_IP=%s
MULTI_HOST=1
UPLOAD_LEGACY_TTY=1
MYSQL_HOST=%s
RABBGGIT_HOST=%s
GLANCE_HOSTPORT=%s:9292
SERVICE_HOST=%s
VNCSERVER_LISTEN=0.0.0.0
VNCSERVER_PROXYCLIENT_ADDRESS=%s
''' % (host.dhcp_ip, host.static_ip, host.static_ip, host.static_ip, host.dhcp_ip,host.static_ip)
                    extra += gen_passwdrc() 
                    #extra += tmp
                    cc_file.write(extra)
                    extras.append(extra)
            except IOError, e:
                extras.append("Error: can\'t find file or read data %s due to %s" % (os.path.join(conf_path(host.hostname),'localrc'),e))
         
        if host.role == '2':
            if cc == None:
                extras.append("Error: can\'t find CC")
            else:
                # nc.append(host.dhcp_ip)
                mk_dir(conf_path(host.hostname))
                try:
                    with open(os.path.join(conf_path(host.hostname),'localrc'),'w+') as nc_file:
                        extra = '''HOST_IP=%s
SERVICE_HOST=%s
MULTI_HOST=1
MYSQL_HOST=%s
RABBIT_HOST=%s
GLANCE_HOSTPORT=%s:9292
ENABLED_SERVICES=n-cpu,n-net,n-novnc,n-xvnc
VNCSERVER_LISTEN=0.0.0.0
VNCSERVER_PROXYCLIENT_ADDRESS=%s
''' % (host.static_ip, cc[0], cc[1], cc[1], cc[1],host.static_ip)
                        extra = extra + gen_passwdrc(generator=False)
                        nc_file.write(extra)
                        extras.append(extra)
                except IOError:
                    extras.append("Error: can't find file or read data %s" % os.path.join(conf_path(host.hostname),'localrc'))
    return extras

def tail(filename, n):
    """Returns last n lines from the filename. No exception handling"""
    size = os.path.getsize(filename)
    with open(filename, "rb") as f:
        # for Windows the mmap parameters are different
        fm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
        try:
            for i in xrange(size - 1, -1, -1):
                if fm[i] == '\n':
                    n -= 1
                    if n == -1:
                        break
            return fm[i + 1 if i else 0:].splitlines()
        finally:
            fm.close()

def readlog():
    logs = ''
    try: 
        lines = tail(LOG_FILE,50)
        for line in reversed(lines):
             logs += line + '\n'
    except IOError:
        logs = "Error: can\'t find log file"
    return logs

def getlog(request):
    #log_dir = os.path.join(PROJ_ROOT,'syslog')
    logs = readlog()
   # return render_to_response('getlog.html',locals(),RequestContext(request))
    return HttpResponse(logs)

def clientlog(request):
    logs = ''
    if request.method == "GET":
        req = request.GET 
        host = req['hostname']
        if host: 
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #host = socket.gethostname()
                s.connect((host,8888))
                while 1:
                    log = s.recv(8172)
                    if not log:
                        break
                    logs += log 
            except socket.error, msg:
                s.close()
                s = None
            if not s is None: 
                s.close()
            else:
                logs = " Could not open socket, plz check the port 7777 on client"
    else: 
        logs = "No GET data"
    return render_to_response("logger.html", locals(),RequestContext(request))
             
def hostview(request):
    init_queryset = Hosts.objects.all()
    table = HostTable(
            init_queryset,
            order_by=request.GET.get('sort','hostname'))

    return render_to_response('table.html',{'table': table},RequestContext(request))
