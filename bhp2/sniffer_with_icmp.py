#!/usr/bin/env python
import socket

import os
import struct
from ctypes import *

# host to listen on
host = "192.168.2.119"

# our IP header
class ICMP(Structure):
	_fields_ = [
		("type", 			c_ubyte),
		("code",			c_ubyte),
		("checksum",		c_ushort),
		("unused",			c_ushort),
		("next_hop_mtu",	c_ushort),
	]

	def __new__(self, socket_buffer):
		"""Return copied buffer contents."""
		return self.from_buffer_copy(socket_buffer)

	def __init__(self, socket_buffer):
		"""Pass init in ICMP."""
		pass


	print "Protocol: %s %s -> %s" % (icmp_header.protocol, icmp_header.src_address, icmp_header.dst_address)

	# if it's ICMP, we want it
	if ip_header.protocol == "ICMP":

		# calculate where our ICMP packet starts
		offset = ip_header.ih1 * 4
		buf = raw_buffer[offset:offset + sizeof(ICMP)]

		# create our ICMP structure
		icmp_header = ICMP(buf)

		print "ICMP -> %d Code: %d" % (icmp_header.type, icmp_header.code)

# 	# handle CTRL-C
# except KeyboardInterrupt:

# 	# if we're using windows, turn off promiscuous mode
# 	if os.name == "nt":
# 		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
