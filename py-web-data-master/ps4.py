import re
file = open('numlines.txt', 'r')
ints = re.findall(r'\d+', 'file')
print ints 
