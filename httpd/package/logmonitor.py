import SocketServer
import re
from collections import deque

logfile = r'/opt/inst-deploy.log'
rule = re.compile(r'^[^+*]',re.MULTILINE)

def tail(fileobj, n=100):
    'Return the last n lines of a file'
    return deque(fileobj, n)

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print self.client_address, 'connected!'

    def handle(self):
        try:
            with open(logfile,'r+') as log:
                for line in tail(log,n=25000):	
		    if re.search(rule,line):
                        self.request.sendall(line)
        except IOError, e:
            print "Failed to open file %s" % e
            return 

    def finish(self):
        print self.client_address, 'disconnected!'

#server host is a tuple ('host', port)
server = SocketServer.TCPServer(('', 8888), EchoRequestHandler)
server.serve_forever()
