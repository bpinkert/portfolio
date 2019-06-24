#!/usr/bin/env python
import re
import np
text = open('text_numbers.txt')
final = []
for line in text:
    line = line.strip()
    y = re.findall('([0-9]+)',line)

    if len(y) > 0:
         lineVal = sum(map(int, y))
         final.append(lineVal)
         print "line sum = {0}".format(lineVal)
print "Final sum = {0}".format(np.sum(final))
