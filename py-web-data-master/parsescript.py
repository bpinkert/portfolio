import re

file = open('regex_sum_219023', 'r')
ints = [int(s) for s in file.split() if s.isdigit()]
print ints

#for line in file:
#	if re.findall('([0-9]+)', line):
#		print line
