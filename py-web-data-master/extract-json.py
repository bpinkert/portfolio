#!/usr/bin/env python
import urllib
import json
import re
import np

final=[]


url = raw_input('Enter location: ')

# url = urllib.urlencode('address')
# print 'Retrieving', url
uh = urllib.urlopen(url)
data = ''' uh.read() '''

info = json.loads(data)

infod = dict()
	
for line in data:
	line = line.strip()
	y = re.findall('([0-9]+)',line)


print 'User count:', len(info)

for item in info:
    print 'Name', item['name']
    print 'Id', item['id']
    print 'Attribute', item['x']


