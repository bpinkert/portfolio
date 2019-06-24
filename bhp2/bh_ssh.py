#!/home/bpubi/Devel/bhp/py2.7.3/bin/python2.7

import threading
import paramiko
import subprocess
import getopt
import sys

# define global variables
target_Host 		= ""
userName 		= ""
userPass 	= ""
remCom 	= "" 


# def server_loop():
       
#         # if no target is defined we listen on all interfaces
#         target = "0.0.0.0"
                
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server.bind((target,port))
        
#         server.listen(5)        
        
#         while True:
#                 client_socket, addr = server.accept()
                
#                 # spin off a thread to handle our new client
#                 client_thread = threading.Thread(target=client_handler,args=(client_socket,))
#                 client_thread.start()

def usage():
        print "SSH Command"
        print
        print "Usage: bh_ssh.py -t host -u user -p password -c command" 
        print "-t --target   		   - target host ip address"
        print "-u --user                  - user for target host authentication"
        print "-p --password              - password for target host authentication"
        print "-c --command=COMMAND       - command to execute"
        print "-h --help		   - help "
        print 
        print
        print "Examples: "
        print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
        print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
        print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
        print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
        sys.exit(0)

def ssh_connect(ip, user, passwd, command):
        client = paramiko.SSHClient()
       #client.load_host_keys('/home/bpubi/.ssh/known_hosts')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, password=passwd)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.exec_command(command)
            print ssh_session.recv(1024)
        else: 
        	print ('Inactive')


def main():
    parser = optparse.OptionParser('usage %prog "+ "-t target_host -u username -p password -c command')
    parser.add_option('-t', dest='target_host', type='string', help='target ip address or hostname')
    parser.add_option('-u', dest='username', type='string', help='username on target system')
    parser.add_option('-p', dest='password', type='string', help='password on target system')
    parser.add_option('-c', dest='command', type='string', help='command to run on target system')

    (options, args) = parser.parse_args()
    target_Host = options.target_host
    userName = options.username
    userPass = options.password
    remCom = options.command


if target_Host == None:
    print parser.usage
        exit(0)
elif userName == None:
  	print parser.usage
    	exit(0)
elif userPass == None:
    print parser.usage
    	exit(0)
elif remCom == None:
    print parser.usage
    	exit(0)
else:
    ssh_connect(target_Host, userName, userPass, remCom)





# ssh_command('triode.pulsedmedia.com', 'pparker', '5X66j5maZh', 'scp ')
