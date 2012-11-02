#!/usr/bin/python

import commands

def exec_ssh_cmd(target, cmd, user="root"):
	"""
	"""
	ssh_cmd_prefix = "ssh -o StrictHostKeyChecking=no -T root"
	return exec_cmd("%s@%s 'sudo -u %s sh -c \"%s\"'" % (ssh_cmd_prefix, target, user, cmd))

def exec_cmd(cmd):
	"""
	"""
	result  = commands.getstatusoutput(cmd)
	print result

if __name__=="__main__":
	conf = "ni hao\nworld"
	exec_ssh_cmd("nova80.sh.intel.com","echo %s > /tmp/test.txt" % (conf))
