#!/usr/bin/env python
import socket
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect( ('www.savantdigital.net', 80) )
