#!/usr/bin/env python
import socket
import os

# host to listen on
host = "10.128.100.100"

# create raw socket and bind to interface
if os.name == "nt":
	socket_protocol = socket.IPPROTO_IP
else:
	socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# capture IP headers
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

# if using windows, we need to set an IOCTL for promiscuous mode
if os.name == "nt":
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# read in a single packet
print sniffer.recvfrom(65565)

# if we're using windows turn off promiscuous mode
if os.name =="nt":
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)