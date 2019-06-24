import re

file = open('regex_sum_219023', 'r')

numsr = open('numlines.txt', 'r')
#nums = open('numlines.txt', 'w')
#for line in file:
#	if re.findall('([0-9]+)', line):
#		print >> nums, line
		
match = re.findall(r'\d+', numsr)

print match()
