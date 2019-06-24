import pythonwhois
import argparse
import sys
import os
import datetime
import re


domains = []
available = []
unavailable = []

def cleanURL(url):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    if urls > 1:    
        available.append(urls)

def readinDomains(domains_list):
    for domainName in domains_list.read().splitlines():
        cleaned = str(cleanURL(domainName))
        print cleaned
        available.append(cleaned)

def grabTLD(url):
    info = urlparse(url)
    url_elements = info.path.split('.')
    tld = url_elements[-1:]

def run():   
    for dom in available:
        if dom is not None and dom != '':
            details = pythonwhois.get_whois(dom)
            if details['contacts']['registrant'] is None:
                unavailable.append(dom)
            else:
                available.append(dom)



def printAvailability():
    print "-----------------------------"
    print "Unavailable Domains: "
    print "-----------------------------"
    for un in unavailable:
        print un
    print "\n"
    print "-----------------------------"
    print "Available Domains: "
    print "-----------------------------"
    for av in available:
        print av

def main():    
    '''
    Argument Parser: 
    '''
    parser = argparse.ArgumentParser(add_help=True, usage='check_domains.py [-d] <singledomain> [-i] <domainlist> or [-r] <TLD Search Expression>')

    parser.add_argument('-d', action='store', dest='single_domain', help='-d example.com')
    parser.add_argument('-i', action='store', dest='domains_txt', help='-i ~/Documents/domainsfile.txt [ABS PATH] (every line will have domain with differemt TLDs like .com .org .net)')
    parser.add_argument('-r', action='store', dest='domains_regex', help='-r google.* (will print out each available domain with different endings)')
    # parser.add_argument('-debug', action='store', dest='debug', help='Turn DEBUG output ON')

    options = parser.parse_args()

    if len(sys.argv)==0:
        parser.print_help()
        sys.exit(1)

    one_dom = options.single_domain
    dom_txt = options.domains_txt
    dom_reg = options.domains_regex 
    
    if one_dom != None:
        try:    
            cleaned = cleanURL(one_dom)
            run() 
            printAvailability()
        except Exception as e:
            print e
            

    if dom_txt != None:
        try:
            with open(dom_txt, 'r') as f:
                readinDomains(f)
                run()
                printAvailability()
        except Exception as e:
            print e    
            
    # if len(domains_regex) > 0:
    #     try:
    #         pass

if __name__ == '__main__':
    main()