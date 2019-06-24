#!/home/bpubi/Devel/bhp/py2.7.3/bin/python2.7

import threading
import paramiko
import subprocess

class RemCom:
	def ssh_command(ip, user, privkey, command):
	        client = paramiko.SSHClient()
	        client.load_host_keys('/home/bpubi/.ssh/known_hosts')
	        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	        client.connect(ip, username=user, key_filename=privkey)
	        ssh_session = client.get_transport().open_session()
	        try: 
	        	if ssh_session.active:
	            		ssh_session.exec_command(command)
	            	print ssh_session.recv(1024)
	        	return 
	    	except Exception as e:
		    	print e.message, e.args	
		    	print command

	ssh_command('', '', '', '')
