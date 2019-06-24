#!/usr/bin/env python
import os
import re
import argparse

class color:
    ALERT = '\033[0m'

def match_IP(text):
    ip_candidates = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", text)
    if ip_candidates:
        return ip_candidates

def parseHeaders(filename):
    linelist = list()
    iplist = list()
    counter = 0
    fullpath = os.path.abspath(filename)
    if os.path.exists(fullpath):
        file_object = open(fullpath, "r")
        for line in file_object:
            linelist.append(line)
            # print "Appended %s to list"%line
        for line in linelist:
            s = match_IP(line)
            if s:
                iplist.append(s)
                # print s
        for line in linelist:
            if str(line).startswith('From: '):
                print line
                domain = str(line.split('@')[1])[:-2]
                print "Source Domain: %s\n"%domain
            if str(line).startswith('Date: '):
                print line
            if str(line).startswith('Subject: '):
                print line
            if str(line).startswith('To: '):
                print line
            if str(line).startswith('x-originating-ip'):
                print "******Source IP Address %s"%line
            if str(line).startswith('X-Originating-IP'):
                print "******Source IP Address %s"%line

        for line in iplist:
            print "%s %s https://who.is/whois-ip/ip-address/%s"%(counter,iplist[counter],str(iplist[counter]).lstrip('[').lstrip("'").rstrip("]").rstrip("'"))
            counter +=1


    else:
        print "File does not exist, check spelling"

def main():

    parser = argparse.ArgumentParser(add_help = True, prog='python script to check email headers for originating ip', description = "Python script to check email headers", usage='Use like so: python parse_Emailheaders.py --file headers.txt')

    parser.add_argument('--file', action='store', dest='fname', help='headers.txt')
    # parser.add_argument('--port', action='store', dest='port', help='--port 443')
    # parser.add_argument('-debug', action='store', dest='debug', help='Turn DEBUG output ON')

    options = parser.parse_args()

    filename = options.fname


    if filename == None:
        print parser.print_usage()
        print "File name is blank. use --file file.txt or absolute path"
    else:
        parseHeaders(filename)

if __name__ == '__main__':
    main()