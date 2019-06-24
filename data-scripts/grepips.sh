#!/bin/bash
#
#
# grep file information, one argument, usually a file name
#
# usage: grepips [file] 
# removes duplicate results and sends matches to STDOUT
grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' $1 | sort | uniq

