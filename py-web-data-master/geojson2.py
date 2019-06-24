import json
import urllib

serviceurl = 'http://python-data.dr-chuck.net/geojson?'

address = raw_input('Enter location: ')

url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
# url = urllib.urlencode('address')
# print 'Retrieving', url
uh = urllib.urlopen(url)
data = uh.read()

info = json.loads(data)

print 'Place ID %s' % info['results'][0]['place_id']
