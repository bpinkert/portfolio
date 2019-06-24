#!/bin/bash python

import re
info = open('regex_sum_219023')
dats=info.read()
print sum(map(int,re.findall(r"\b\d+\b",dats)))
