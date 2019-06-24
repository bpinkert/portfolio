#!/usr/bin/env python
#
# script to search shodan for freenas servers with port 22 open, attempt to SSH using default credentials
#
import shodan
import argparse

api = shodan.Shodan("")

matchlist = []
filtered = []

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


def filter_ports(matchlist, ports):
    global filtered

    portslist = ports.split(',')
    if len(portslist) is 1:
        try:
            for m in matchlist:
                if m.port == "%s" % portslist[0]:
                    print 'IP %s' % m.ip_str
                    print "Port %s is open" % portslist[0]
                    filtered.append(m)
                else:
                    pass
            if len(filtered) is 0:
                print "None of the search results had port %s open" % portslist[0]
        finally:
            return filtered
    else:
        try:
            for m in matchlist:
                for port in portslist:
                    if m.port is "%s" % port:
                        print 'IP %s' % m.ip_str
                        print "Port %s is open" % portslist[0]
                        filtered.append(m)
                    else:
                        pass
            if len(filtered) is 0:
                print "None of the search results had port %s open" % portslist[0]
        finally:
            return filtered


def parse_search(querystring, querylimit, queryoffset):
    global matchlist

    try:
        results = api.search(query=querystring, limit=querylimit, offset=queryoffset)
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

        return matchlist

def main():
    parser = argparse.ArgumentParser(add_help=True, prog='Program to search and filter shodan platform',
                                     description="Program to search and filter shodan platform",
                                     usage='Use like so: python shodan_search.py --query freenas --ports 22,80,8080 '
                                           '--limit 300 --offset 300')

    parser.add_argument('--query', action='store', dest='query', help='eg: freenas ')
    parser.add_argument('--ports', action='store', dest='ports', help='eg: 22  OR 22,23,24,25')
    parser.add_argument('--limit', action='store', dest='limit', help='limit the amount of results')
    parser.add_argument('--offset', action='store', dest='offset', help='start from the x result to continue previous '
                                                                        'search')
    # parser.add_argument('-debug', action='store', dest='debug', help='Turn DEBUG output ON')

    options = parser.parse_args()

    querystring = options.query
    openports = options.ports
    querylimit = options.limit
    queryoffset = options.offset

    if querystring is None:
        print parser.usage
        print "Query cannot be blank"

    if queryoffset and querylimit and openports is None:
        print "Query limited to 100 results"
        print "Ports were not specified, listing all results"
        parse_search(querystring, querylimit=100, queryoffset=0)
    elif queryoffset and querylimit is None:
        if openports:
            print "Query limited to 100 results"
            print "Filtering for ports: %s" % openports
            p = parse_search(querystring, querylimit=100, queryoffset=0)
            filter_ports(matchlist=p, ports=openports)
        else:
            print "Query limited to 100 results"
            print "Ports were not specified, listing all results"
            parse_search(querystring, querylimit=100, queryoffset=0)
    elif querylimit and not queryoffset:
        if openports:
            print "Query limited to %s results" % querylimit
            print "Filtering for ports: %s" % openports
            p = parse_search(querystring, querylimit=int(querylimit), queryoffset=0)
            filter_ports(matchlist=p, ports=openports)
        else:
            print "Query limited to %s results" % querylimit
            print "Ports were not specified, listing all results"
            parse_search(querystring, querylimit=int(querylimit), queryoffset=0)
    elif queryoffset and not querylimit:
        if openports:
            print "Query limited to 100 results"
            print "Query offset is %s" % queryoffset
            print "Filtering for ports: %s" % openports
            p = parse_search(querystring, querylimit=100, queryoffset=int(queryoffset))
            filter_ports(matchlist=p, ports=openports)
        else:
            print "Query limited to 100 results"
            print "Query offset is %s" % queryoffset
            print "Ports were not specified, listing all results"
            parse_search(querystring, querylimit=100, queryoffset=int(queryoffset))
    elif queryoffset and querylimit:
        if openports:
            print "Query limited to %s results" % querylimit
            print "Query offset is %s" % queryoffset
            print "Filtering for ports: %s" % openports
            p = parse_search(querystring, querylimit=int(querylimit), queryoffset=int(queryoffset))
            filter_ports(matchlist=p, ports=openports)
        else:
            print "Query limited to %s results" % querylimit
            print "Query offset is %s" % queryoffset
            print "Ports were not specified, listing all results"
            parse_search(querystring, querylimit=int(querylimit), queryoffset=int(queryoffset))


if __name__ == '__main__':
    main()