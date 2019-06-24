#!/usr/env/python

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
#day=$(date +'%m%e')

IP = ''               # ip or hostname
USER = ''             # username
PASS = ''             # password
LPATH = ''            # local path
RPATH = ''            # remote path
MODE = 'put'          # put or get



sftp_command(IP, USER, PASS, LPATH, RPATH , MODE)	

