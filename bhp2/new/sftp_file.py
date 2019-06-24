#!/home/bpubi/Devel/bhp/py2.7.3/bin/python2.7

import threading
import paramiko
import subprocess

def sftp_command(ip, user, passwd, localpath, remotepath, mode):
        transport = paramiko.Transport((ip, 22))
	transport.connect(username = user, password = passwd)
	sftp = paramiko.SFTPClient.from_transport(transport)
	if mode == 'put':
		sftp.put(localpath, remotepath)
	if mode == 'get':
		sftp.get(remotepath, localpath)

sftp_command('', '', '', '', '', '')	
       