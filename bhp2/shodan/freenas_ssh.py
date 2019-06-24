#!/usr/bin/env python
#
# script to search shodan for freenas servers with port 22 open, attempt to SSH using default credentials
#
import shodan

api = shodan.Shodan("")

# initialize list to hold objects
matchlist = []
filtered = []

# Define class to store results
class ShodanMatch:

    def __init__(self, product, version, port, hostnames, timestamp, domains, data, transport, ip_str):
        self.product = product
        self.version = version
        # self.cpe = cpe
        self.port = port
        self.hostnames = hostnames
        self.timestamp = timestamp
        self.domains = domains
        self.data = data
        self.transport = transport
        self.ip_str = ip_str

    def __str__(self):

        return self.ip_str

# search for freenas and append results as ShodanMatch object into matchlist
try:
    results = api.search("freenas", limit=300)
    print 'Results found: %s' % results['total']
    for result in results['matches']:

        if 'product' in result:
            product = result['product']
        else:
            product = ""
        # cpe = result['cpe']
        if 'version' in result:
            version = result['version']
        else:
            version = ""
        port = result['port']
        if 'hostnames' in result:
            hostnames = result['hostnames']
        else:
            hostnames = ""
        timestamp = result['timestamp']
        if 'domains' in result:
            domains = result['domains']
        else:
            domains = ""
        search_data = result['data']
        transport = result['transport']
        ip_str = result['ip_str']
        m = ShodanMatch(product, version, port, hostnames, timestamp, domains, search_data, transport, ip_str)
        matchlist.append(m)
        print 'IP %s' % ip_str
        # print search_data
        print port
        print ''
except shodan.APIError, e:
    print 'Error: %s' % e


# iterate through matchlist looking for port 22 open
try:
    for m in matchlist:
        if m.port == "22":
            filtered.append(m)
            print 'IP %s' % m.ip_str
            print "Port 22 Open"
        else:
            pass
    if len(filtered) == 0:
        print "None of the search results had port 22 open"
except error as e:
    print 'Error: %s' % e
