import urllib
import xml.etree.ElementTree as ET

url = 'http://python-data.dr-chuck.net/comments_219025.xml'
uh = urllib.urlopen(url)
data = uh.read()
tree = ET.fromstring(data)

results = tree.findall('.//count')
   
print results

tot = 0

for count in results:
    val = count.text
    tot = tot + int(val)
    print val
    

print val, tot