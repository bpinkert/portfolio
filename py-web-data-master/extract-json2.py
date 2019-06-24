import json
import urllib
import re

url = raw_input('Enter location: ')

# url = urllib.urlencode('address')
# print 'Retrieving', url
uh = urllib.urlopen(url)
data = uh.read()

info = json.loads(data)

counts = info['comments'][0]['count']
data2 = []

for line in info:
    data2.append(info['comments'][0-49]['count'])
    
print data2