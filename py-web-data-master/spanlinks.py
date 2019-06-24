#!/usr/bin/env python
import urllib
from BeautifulSoup import *

url = raw_input('Enter - ')

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

tags = soup('td')

l = list()

for tag in tags:
	l.extend(tag.contents[0])			
	

for item in l:
	newlist = [s for s in l if s.isdigit()]
	 

numlist = map(int, newlist)
s = sum(numlist)

print s
