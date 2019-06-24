#!/usr/bin/env python

import argparse
import os
import xml.etree.ElementTree
from collections import defaultdict


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def main():

    parser = argparse.ArgumentParser(add_help=True, prog='python script to parse DMARC aggregate reports',
                                     description="python script to parse DMARC aggregate reports",
                                     usage='Use like so: python dmarc_aggregate_parser.py '
                                           '--file report.xml --output parsed.csv')

    parser.add_argument('-f', '--file', action='store', dest='fname', help='raw.xml')
    parser.add_argument('-o', '--output', action='store', dest='outfile', help='output.csv')
    # parser.add_argument('-debug', action='store', dest='debug', help='Turn DEBUG output ON')

    options = parser.parse_args()

    infile = options.fname
    outfile = options.outfile

    if outfile is None:
        outfile = "parsed.csv"
    if os.path.exists(os.path.abspath(outfile)):
        print parser.print_usage()
        print "File already exists, choose a different file name"
    if infile is None:
        print parser.print_usage()
        print "File name is blank. use --file file.txt or absolute path"
    else:
        try:
            t = xml.etree.ElementTree.parse(infile).getroot()
            e = etree_to_dict(t)
            print e
        except Exception as e:
            print parser.print_usage()
            print "Exception: %s" % e


if __name__ == '__main__':
    main()
