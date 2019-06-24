#!/usr/bin/env python
# from http://www.primalsecurity.net/pyfu-leveraging-python-and-bash-for-automation/
import sys, os, optparse
from cymruwhois import Client

def look(iplost):
	c=Client() # create instance of client class
	try:
		if ips != None:
			r = c.lookupmany_dict(iplist) # uses lookupmany_dict() function to pass in a list of IPs
			for ip in iplist:
				net = r[ip].prefix; owner = r[ip].owner; cc = r[ip].cc # gets network info from dict
				line = '%-20s # - %15s (%s) - %s' % (net,ip,cc,owner) # formats the line to print
				print line
	except:pass

def checkFile(ips): #check that we can read file
	if not os.path.isfile(ips):
		print '[-] ' + ips + ' does not exist.'
		sys.exit(0)
	if not os.access(ips, os.R_OK):
		print '[-] ' + ips + ' access denied.'
		sys.exit(0)
	print '[+] Querying from: ' +ips

def main():
	parser = optparse.OptionParser('%prog -r <file_with_IPs> || -i <IP>')
	parser.add_option('-r', dest='ips', type='string', help='specify a target file with IPs')
	parser.add_option('-i', dest='ip', type='string', help='specify a target IP address')
	(options, args) = parser.parse_args()
	ip = options.ip # Assigns a -i <IP> to variable 'ip'
	global ips; ips = options.ips # Assigns a -r <fileName> to variable 'ips'
	if (ips == None) and (ip == None): # if arguments aren't given
		print parser.usage
		sys.exit(0)
	if ips != None: # execute if ips has a value
		checkFile(ips)
		iplist = []
		for line in open(ips, 'r')
