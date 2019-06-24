#!/usr/bin/env python
numberlist = []

def generate_numbers(start_num,end_num):
        global numberlist

        start = int(start_num)
        end = int(end_num)
        while end > start:
                print start
                numberlist.append(start)
                start +=1

generate_numbers(10000000, 99999999)
print numberlist
# the above command will generate all 8-digit passwords excluding 00000001 through 09999999, append all combinations to
# a list and then print the list

# attempt to generate the missing 00000001 through 09999999 by prepending 0s
# def generate_lownumbs(start_num, end_num):
#         start = str(start_num)
#         end = str(end_num)
#         while int(end) > int(start):
#                 while len(start) < 8:
#                         s = str(start)
#                         s = '0' + s
#                 print s
#                 start_num+=1
#
#generate_lownumbs(1,10000000)

