#!/usr/bin/env python
#
# Python script to audit SSL configurations
# via openssl installation
#
#

import argparse
import os
import subprocess
import ssl
import socket

def checkTLS12(target, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(s)
    ssl_sock.connect((target, int(port)))
    if ssl_sock.cipher():
        print "TLS1.2 Enabled"
        c = ssl_sock.cipher()[0]
        print "Cipher: %s"% c
        return True
    else:
        return False

def checkTLS11(target, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(s)
    ssl_sock.connect((target, int(port)))
    if ssl_sock.cipher():
        print "TLS1.1 Enabled"
        c = ssl_sock.cipher()[0]
        print "Cipher: %s"% c
        return True
    else:
        return False

def checkTLS1(target, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(s)
    ssl_sock.connect((target, int(port)))
    if ssl_sock.cipher():
        print "TLS1.0 Enabled"
        c = ssl_sock.cipher()[0]
        print "Cipher: %s"% c
        return True
    else:
        return False

# def checkSSL3(target, port):
#     context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     ssl_sock = context.wrap_socket(s)
#     ssl_sock.connect((target, int(port)))
#     if ssl_sock.cipher():
#         print "SSL3 Enabled"
#         c = ssl_sock.cipher()[1]
#         print "Cipher: %s"% c
#         return True
#     else:
#         return False
#
# def checkSSL2(target, port):
#     context = ssl.SSLContext(ssl.PROTOCOL_SSLv2)
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     ssl_sock = context.wrap_socket(s)
#     ssl_sock.connect((target, int(port)))
#     if ssl_sock.cipher():
#         print "SSL2 Enabled"
#         c = ssl_sock.cipher()[1]
#         print "Cipher: %s"% c
#         return True
#     else:
#         return False


def checkIPTLS12(target, port):
    command = 'openssl s_client -connect %s:%s -tls1_2'%(str(target),str(port))
    try:
        subprocess.check_output(command)
        runCheck = subprocess.Popen(command, stdout=subprocess.PIPE)
        lines = runCheck.stdout.readlines()
        # if lines[39].startswith('SSL handshake'):
        #     if lines[39].endswith('written 0 bytes\n'):
        #         print lines[39]
        #         return False
        #     else:
        #         print lines[39]
        #         return True
        for line in lines:
            if line != '':
                if line.startswith('SSL handshake'):
                    if line.endswith('written 0 bytes\n'):
                        return False
                    else:
                        return True
        else:
            pass
    except Exception as e:
        print "Exception: %s" % e
        return False


def checkIPTLS11(target, port):
    command = 'openssl s_client -connect %s:%s -tls1_1'%(str(target),str(port))
    try:
        subprocess.check_output(command)
        runCheck = subprocess.Popen(command, stdout=subprocess.PIPE)
        while True:
            line = runCheck.stdout.readline()
            if line != '':
                if line.startswith('SSL handshake'):
                    if line.endswith('written 0 bytes'):
                        return False
                    else:
                        return True
            else:
                break
    except Exception as e:
        # print "Exception: %s" % e
        return False


def checkIPTLS1(target, port):
    command = 'openssl s_client -connect %s:%s -tls1'%(str(target),str(port))
    try:
        subprocess.check_output(command)
        runCheck = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if runCheck.stderr:
            print "Error: TLS1.0 Disabled"
            return False
        else:
            lines = runCheck.stdout.readlines()
            if lines != '':
                if lines[39].startswith('SSL handshake'):
                    if lines[39].endswith('written 0 bytes'):
                        print "TLS1.0 Disabled"
                        return False
                    else:
                        return True
            else:
                pass
    except Exception as e:
        print "TLS1.0 Disabled"
        return False


def openssl_installed():
    if os.name == 'nt':
        try:
            subprocess.check_output(['openssl', 'exit'])
            print "OpenSSL is installed"
        except Exception as e:
            print "Exception: %s" % e
            print "OpenSSL is likely not installed"
            print "Download OpenSSL for Windows and include in path to continue"
    else:
        try:
            subprocess.check_output(['which', 'openssl'])
            print "OpenSSL is installed"
            return True
        except Exception as e:
            print "Exception: %s" % e
            print "OpenSSL is likely not installed"
            print "Run apt-get install openssl on debian/ubuntu systems"

def main():

    parser = argparse.ArgumentParser(add_help = True, prog='python script to check OpenSSL configuration', description = "Python script to audit SSL configuration", usage='Use like so: python openssl_audit.py --url https://www.google.com')

    parser.add_argument('--url', action='store', dest='url', help='--url www.google.com')
    parser.add_argument('--ip', action='store', dest='ip', help='--ip 192.168.1.1')
    parser.add_argument('--port', action='store', dest='port', help='--port 443')
    # parser.add_argument('-debug', action='store', dest='debug', help='Turn DEBUG output ON')

    options = parser.parse_args()

    auditURL = options.url
    auditPort = options.port
    auditIP = options.ip

    if auditURL == None:
        if auditIP == None:
            print parser.print_usage()
            print "URL is blank. use --url example.com"
        else:
            openssl_installed()
            print "Placeholder for IP support"
    elif auditPort == None:
        print parser.print_usage()
        print "Port is blank. use --port 443"
    else:
        checkTLS1(auditURL, auditPort)
        checkTLS11(auditURL, auditPort)
        checkTLS12(auditURL, auditPort)

if __name__ == '__main__':
    main()