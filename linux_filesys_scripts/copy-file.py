#!/usr/bin/env python
# Description: copy file from one source to destination
# Params:
# 1) Source File 
# 2) Destination File
#
#
import shutil
import os
import subprocess
#from pathlib import Path
import popen
import optparse

def copyfileImg(source, dest,  buffer_size=1024*1024):
	"""
	Copy an image file from source to dest, both source and dest must be 
	file-lie objects, anything with a read or write method.

	This will be used to copy files from buffer to file
	"""	
	while 1:
		copy_buffer = source.read(buffer_size)
		if not copy_buffer:
			break
		dest.write(copy_buffer)

def copyFile(source, dest):
	with open(source, 'rb') as src, open(dest, 'wb') as dst:
		copyfileImg(src, dst)

 
def main():
    parser = optparse.OptionParser('usage %prog -S <src> + -D <dst>')
    parser.add_option('-S', dest='srcfile', type='string', help='source file location')
    parser.add_option('-D', dest='dstfile', type='string', help='dest file location')

    (options, args) = parser.parse_args()
    srcFile = options.srcfile
    dstFile = options.dstfile
    if dstFile == None:
        print parser.usage
        exit(0)
    elif srcFile == None:
    	print parser.usage
    	exit(0) 
    else:
        copyFile(srcFile, dstFile)

if __name__ == '__main__':
    main()

