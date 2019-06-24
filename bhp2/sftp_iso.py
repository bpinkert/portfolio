#!/usr/env/python

import threading
import paramiko
import subprocess

def sftp_command(ip, user, passwd, localpath, remotepath, mode):
  transport = paramiko.Transport((ip, 22)),
  transport.connect(username = user, password = passwd)
	sftp = paramiko.SFTPClient.from_transport(transport)
	if mode == 'put':
		sftp.put(localpath, remotepath)
	if mode == 'get':
		sftp.get(remotepath, localpath)
day=$(date +'%m%e')
sftp_command('', '', '', '', '', '')	
       #client.load_host_keys('/home/bpubi/.ssh/known_hosts')
       #client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       # client.connect(ip, username=user, password=passwd)
       # ssh_session = client.get_transport().open_session()
       # if ssh_session.active:
       #     ssh_session.exec_command(command)
       #     print ssh_session.recv(1024)
       # return
