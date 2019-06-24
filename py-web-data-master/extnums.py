import re

numlines = open('numlines.txt')
matches = re.findall('([0-9]+)', numlines, re.DOTALL)
print matches
