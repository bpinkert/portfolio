#!/usr/bin/env python
# Description: use linux dd function to copy device file to .raw image
#
# Params: 
# -dev device file: in /dev/sda format (copy the entire partition, not /dev/sda1 if you want the entire OS)
# -img output image location: in file path like /home/user/Downloads/filename.raw
import optparse
import subprocess
import argparse
import time
import sys
import os

def copydev(device, outfile):
	# command = "sudo dd if=%s of=%s bs=512" % (device, outfile)
	# try:
	# 	a = subprocess.Popen([command], shell=True).communicate()[0]
	# except Exception as e:
	#     print e.message, e.args	
	#     print command
	try:
		command = "sudo dd if=%s of=%s bs=512 & pid=$!" % (device, outfile)
		c = subprocess.Popen([command], shell=True).communicate()[0] 
		# while True:
		# 	s = subprocess.Popen(['kill -s USR1 $pid; wait 30'])
		# 	time.sleep(60)
	except Exception as e:
		print e.message, e.args
		print command

def main():
    # parser = optparse.OptionParser('usage %prog -S <src> + -D <dst>')
    # parser.add_option('-S', dest='devfile', type='string', help='udev file path')
    # parser.add_option('-D', dest='dstfile', type='string', help='dest file location')

    parser = argparse.ArgumentParser(add_help = True, prog='python script to utilize linux dd command', description = "Python script to copy a /dev/sda device file to file.raw image format.     User should have sudo permissions to ensure proper usage", usage='Use like so: python dd_img.py -dev /dev/sda -img /tmp/sda1.raw')

    parser.add_argument('-dev', action='store', dest='devfile', help='eg: /dev/sda | COPY WHOLE partition for DR')
    parser.add_argument('-img', action='store', dest='imgfile', help='eg: /home/user/Backup/sda.raw | full path is best')
    # parser.add_argument('-debug', action='store', dest='debug', help='Turn DEBUG output ON')

    options = parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    devFile = options.devfile
    imgFile = options.imgfile
    in_fd = open(str(devFile), 'r')  
    out_fd = open(str(imgFile), 'wb')
    if devFile == None:
        print options.print_usage
    elif imgFile == None:
    	print options.print_usage
    else:
        copydev(devFile, imgFile)

if __name__ == '__main__':
    main()