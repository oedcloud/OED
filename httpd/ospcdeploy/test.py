import os
import sys

rel = lambda p: os.path.join(os.pardir,p)

root =  os.getcwd()
print os.pardir
print rel('localrc')
print rel('config')
print os.path.join(rel('config'),'localrc')
