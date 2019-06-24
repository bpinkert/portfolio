#!/home/bpubi/Devel/bhp/py2.7.3/bin/python2.7

import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, password=passwd)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.exec_command(command)
            print ssh_session.recv(1024)
        return
    

def reverse_Tunnel(ip, user, passwd, lport):
		rclient = paramiko.SSHClient()
		rclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		rclient.connect(ip, username=user, password=passwd)
		rssh_session = rclient.get_transport().open_session()
		if rssh_session.active:
			rcommand = "ssh -fN -R %s:localhost:22" % lport
			print rcommand
			rssh_session.exec_command(rcommand)
			print rssh_session.recv(1024)
		return

reverse_Tunnel('', '', '', '')