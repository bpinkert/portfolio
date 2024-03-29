#!/usr/bin/env python
#
import os
import sys
import argparse


def add_docsummary(file_list, directory):
	'''

	'''
	os.chdir(directory)
	base_dir = ''
	description = ''
	author = ''
	path = directory.split('/')
	curdir = path[0]
	bslash = "\\"
	path_len = len(path[1:])
	package = ''
	subpack_list = ['actions', 'vault', 'assets', 'overlays']
	# for file in file_list:
	# 	file_abspath = os.path.abspath(file)
	# 	path_split = file_abspath.split('/')
	# 	subpack_dir = path_split[-2]
	# 	for s in subpack_list:
	# 		if s == subpack_dir:
	# 			subpackage == s
	# 		else:
	# 			subpackage = None			 
	if path_len >= 3:
		if path[-3] != base_dir and path[-3] != None:
			if path[-2] != base_dir and path[-1] != base_dir:
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub2 + bslash + sub1
			elif path[-1] != base_dir:
				sub1 = path[-1]
				package += curdir + bslash + sub1
			elif curdir != base_dir:
				package += curdir 
			else:
				package = 'Champ'
	elif path_len == 2:
		if path[-2] != base_dir and path[-1] != base_dir:
			sub1 = path[-1]
			package += curdir + bslash + sub1 
		elif curdir != base_dir:
			package += curdir
		else:
			package = 'Champ'
	elif path_len == 1:
		if path[-1] != base_dir and curdir != base_dir:
			package += curdir
		else:
			package = 'Champ'
	for file in file_list:
		file_abspath = os.path.abspath(file)
		path_split = file_abspath.split('/')
		subpack_dir = path_split[-2]
		for s in subpack_list:
			if subpack_dir == s:
				subpackage = subpack_dir
				print subpackage
			else:
				subpackage = None
			with open(file, 'r') as original: 
				data = original.read()
				# print file
				line1 = data[0:6]
				line2 = data[6:10]
				remainder = data[6:]
				# print remainder
				original.close()
				if line2 != '/**\n':
					if subpackage == None:
						with open(file, 'w') as modified:
							docsummary = '<?php\n/**\n * %s\n *\n * %s\n *\n * @author %s\n * @package %s\n */\n' % (file,description,author,package) 
							modified.write(docsummary + remainder)
							modified.close()
							print "File modified: %s\n" % file
							print subpackage
					else:
						with open(file, 'w') as modified:
							docsummary = '<?php\n/**\n * %s\n *\n * %s\n *\n * @author %s\n * @package %s\n * @subpackage %s\n */\n' % (file,description,author,package,subpackage) 
							modified.write(docsummary + remainder)
							modified.close()
							print "File modified: %s\n" % file
							print subpackage
				else:
					pass


def get_phpfiles(dir):
	'''
	initialize list file_list
	check that dir is a real path
	list files in dir
	get last 4 letters of each filename in dir 
	if file-ext is .php append filename to file_list
	return file_list
	'''
	file_list = list()
	if os.path.isdir(dir) == True:
		filecounter = 0
		files = os.listdir(dir)
		for file in files:
			filecounter += 1
			last4 = file[-4:] 
			if last4 == '.php':
				file_list.append(file)
			else:
				pass
		return file_list

def main():
	parser = argparse.ArgumentParser(add_help = True, prog='', description = '', usage='')    
	parser.add_argument( '-d', '--directory', action='store', dest='phpdir')
	parser.add_argument( '-f', '--file', action='store', dest='phpfile')

	options = parser.parse_args()

	if len(sys.argv)==0:
		parser.print_help()
		sys.exit(1)

	directory = os.path.abspath(options.phpdir)
	try:
		phpfiles = get_phpfiles(directory)
		add_docsummary(phpfiles,directory)
	except Exception as e:
		print "Exception %s" % e


if __name__ == '__main__':
    main()
