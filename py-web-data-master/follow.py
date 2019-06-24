#!/usr/bin/env python
import urllib
from BeautifulSoup import *

url = raw_input('Enter URL:')
#count = raw_input('Enter Count:')
#pos = raw_input('Enter Position:')

counti = 4
posi = 3

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

tags = soup('a')

y = 0

while y < counti:
	y + 1
	next = tags[posi]
	print next 
	follow = urllib.urlopen(next).read()
	BeautifulSoup(follow)

 
