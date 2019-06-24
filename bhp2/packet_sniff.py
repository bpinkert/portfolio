!/usr/bin/env python
import socket
import os

# host to listen on
host = "127.0.0.1"

# create raw socket and bind to interface
if os.name == "nt":
	socket_protocol = socket.IPPROTO_IP
else:
	socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 80))

# capture IP headers
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

# if using windows, we need to set an IOCTL for promiscuous mode
if os.name == "nt":
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# read in a single packet
packet = sniffer.recvfrom(65565)

print packet
# if we're using windows turn off promiscuous mode
if os.name =="nt":
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
