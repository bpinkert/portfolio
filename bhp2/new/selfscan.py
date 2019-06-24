#!/usr/bin/env python
import os
import socket
import netifaces as ni

# user and path variables


renv = os.environ
path = renv['PATH']
home = renv['HOME']
ruser = renv['USER']
rdir = os.getcwd()
rshell = renv['SHELL']

# parse available executables

rb = os.popen('ls /bin').read()
rbin = rb.split('\n')
sb = os.popen('ls /sbin').read()
sbin = sb.split('\n')

# networking 
p = os.popen('hostname')
rhost = p.read()

inf = ni.ifaddresses('wlan0')
rip = inf[2][0]['addr']
rnm = inf[2][0]['netmask']
rmac = inf[17][0]['addr'] 
# print results 

print "Path:\n " + path
print "Home Dir: " + home
print "User: " + ruser
print "Shell: " + rshell
print "LAN IP: " + rip  
print "MAC ADDY: " + rmac
print "Hostname: " + rhost 