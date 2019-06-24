#!/usr/bin/env python
#
import os
import sys
import argparse
import re


def add_docsummary(file_list, directory):
	'''

	'''
	os.chdir(directory)
	base_dir = ''
	description = 'Description PH'
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
	if path_len >= 6:
		if path[-6] != base_dir and path[-6] != None:
			if path[-5] != base_dir and path[-4] != base_dir:
				sub5 = path[-5]
				sub4 = path[-4]
				sub3 = path[-3]
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub5 + bslash + sub4 + bslash + sub3 + bslash + sub2 + bslash + sub1
			elif path[-4] != base_dir:
				sub4 = path[-4]
				sub3 = path[-3]
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub4 + bslash + sub3 + bslash + sub2 + bslash + sub1
			elif path[-3] != base_dir:
				sub3 = path[-3]
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub3 + bslash + sub2 + bslash + sub1
			elif path[-2] != base_dir:
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub2 + bslash + sub1
			elif path[-1] != base_dir:
				sub1 = path[-1]
				package += curdir + bslash + sub1 
			else:
				pass
	elif path_len == 5:
		if path[-5] != base_dir and path[-5] != None:
			if path[-4] != base_dir and path[-3] != base_dir:
				sub4 = path[-4]
				sub3 = path[-3]
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub4 + bslash + sub3 + bslash + sub2 + bslash + sub1
			elif path[-3] != base_dir:
				sub3 = path[-3]
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub3 + bslash + sub2 + bslash + sub1
			elif path[-2] != base_dir:
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub2 + bslash + sub1
			elif path[-1] != base_dir:
				sub1 = path[-1]
				package += curdir + bslash + sub1 
			else:
				pass
	elif path_len == 4:
		if path[-4] != base_dir and path[-4] != None:
			if path[-3] != base_dir and path[-2] != base_dir:
				sub3 = path[-3]
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub3 + bslash + sub2 + bslash + sub1
			elif path[-2] != base_dir:
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub2 + bslash + sub1
			elif path[-1] != base_dir:
				sub1 = path[-1]
				package += curdir + bslash + sub1 
			else:
				pass
	elif path_len == 3:
		if path[-3] != base_dir and path[-3] != None:
			if path[-2] != base_dir and path[-1] != base_dir:
				sub2 = path[-2]
				sub1 = path[-1]
				package += curdir + bslash + sub2 + bslash + sub1
			elif path[-1] != base_dir:
				sub1 = path[-1]
				package += curdir + bslash + sub1
			else:
				pass
	elif path_len == 2:
		if path[-2] != base_dir and path[-1] != base_dir:
			sub1 = path[-1]
			package += curdir + bslash + sub1 
		elif curdir != base_dir:
			package += curdir
		else:
			pass
	elif path_len == 1:
		if path[-1] != base_dir and curdir != base_dir:
			package += curdir
		else:
			pass
	for file in file_list:
		file_abspath = os.path.abspath(file)
		path_split = file_abspath.split('/')
		# subpack_dir = path_split[-2]
		# for s in subpack_list:
		# 	if subpack_dir == s:
		# 		subpackage = subpack_dir
		# 		if path_split[-3] != base_dir:
		# 			subpackage = subpack_dir
		# 			if path_split[-4] != base_dir:
		# 				package = path_split[-4]
		# 			else:
		# 				package = path_split[-3]
		# 		else:
		# 			subpackage = subpack_dir
		# 		if path_split[-4] != base_dir:
		# 			subpackage = subpack_dir
		# 			if path_split[-5] != base_dir:
		# 				package = path_split[-5]
		# 			else:
		# 				package = path_split[-4]
		# 		else:
		# 			subpackage = subpack_dir
		# 	else:
				# subpackage = None
		with open(file, 'r') as original: 
			data = original.read()
			# print file
			line1 = data[0:6]
			line2 = data[6:10]
			remainder = data[6:]
			# print remainder
			original.close()
			if line2 != '/**\n':
				# if subpackage == None:
				with open(file, 'w') as modified:
					docsummary = '<?php\n/**\n * %s\n *\n * %s\n *\n * @author %s\n * @package %s\n */\n' % (file,description,author,package) 
					modified.write(docsummary + remainder)
					modified.close()
					print "File modified: %s\n" % file
				# else:
				# 	with open(file, 'w') as modified:
				# 		subp_len = len(subpackage)
				# 		spackage = package[:-subp_len]
				# 		print package
				# 		docsummary = '<?php\n/**\n * %s\n *\n * %s\n *\n * @author %s\n * @package %s\n * @subpackage %s\n */\n' % (file,description,author,package,spackage) 
				# 		modified.write(docsummary + remainder)
				# 		modified.close()
				# 		print "File modified: %s\n" % file
			else:
				pass

def add_function_bloc(file_list, directory):
	f_regex = re.compile('function\s\w+')
	p_regex = re.compile('\$\w+')
	func_list = ()
	param_dict = {}
	line_list = ()
	os.chdir(directory)
	for file in file_list:
		file_abspath = os.path.abspath(file)
		path_split = file_abspath.split('/')
		with open(file, 'r') as original:
			data = original.readlines()
			for line in data:
				func = f_regex.findall(line)
				# print func
				if func != None:
					func_name = func[0].split(' ')[1]
					# func_list.append(func_name)
					print func_name
					params = p_regex.findall(line)
					param_list = ()
					for param in params:
						param_list.append(param)
						print param
					param_dict[func_name] = param_list
					line_list.append('/**\n')
					line_list.append('* %s') % func_name
					for param in param_list:
						line_list.append('* @param %s') % param
					line_list.append('*/')
					line_list.append(line)
					original.close()
				elif func == None:
					line_list.append(line)
					original.close()

				# all_lines = ''
				# for item in line_list:
				# 	all_lines += item
				# if subpackage == None:
		with open(file, 'w') as modified:
			modified.writelines(line_list)
			modified.close()
			print "File modified: %s\n" % file
			# else:
			# 	with open(file, 'w') as modified:
			# 		subp_len = len(subpackage)
			# 		spackage = package[:-subp_len]
			# 		print package
			# 		docsummary = '<?php\n/**\n * %s\n *\n * %s\n *\n * @author %s\n * @package %s\n * @subpackage %s\n */\n' % (file,description,author,package,spackage)
			# 		modified.write(docsummary + remainder)
			# 		modified.close()
			# 		print "File modified: %s\n" % file


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
	parser = argparse.ArgumentParser(add_help = True, prog='prepend_dev', description = 'Prepend all files in a directory with php docblocks with correct package', usage='python prepend_phpfiles.py -d [directory]')    
	parser.add_argument( '-d', '--directory', action='store', dest='phpdir')
	parser.add_argument( '-f', '--file', action='store', dest='phpfile')

	options = parser.parse_args()

	if len(sys.argv)==0:
		parser.print_help()
		sys.exit(1)
	# if options.phpfile == None:
	# 	parser.print_help()

	if options.phpdir != None:
		directory = os.path.abspath(options.phpdir)
		try:
			# file = os.path.abspath(options.phpfile)
			# f = file.split('/')
			# directory = '/'
			# f.pop(0)
			# for direct in f:
			# 	directory += direct
			# 	directory += '/'
			phpfiles = get_phpfiles(directory)
			add_docsummary(phpfiles,directory)
			phpfiles2 = get_phpfiles(directory)
			add_function_bloc(phpfiles2,directory)
		except Exception as e:
			print "Exception %s" % e 
	# else:
	# 	directory = os.path.abspath(options.phpdir)
	# 	try:
	# 		phpfiles = get_phpfiles(directory)
	# 		add_docsummary(phpfiles,directory)
	# 	except Exception as e:
	# 		print "Exception %s" % e


if __name__ == '__main__':
    main()
