#!/usr/bin/env python
# tool to generate a dictionary for brute-forcing alpha-numeric passwords that contain symbols
# 79 total characters
charlist = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '!', '#', '$', '%', '&', '*', '+', '-', '.', '/', '<', '=', '>', '?', '@', '^', '~'
]

passlist = []

class PasswordGenerator:
    global charlist
    global passlist

    def __init__(self, minlen, maxlen):
        self.__minlen = minlen
        self.__maxlen = maxlen
        self.__charlist = charlist

    def genpass(self,passlength):


    def incrementer(self):
        minimum = self.__minlen
        maximum = self.__maxlen
        charset = self.__charlist

        for l in range(minimum,maximum):



    def run(self):

def main():

    parser = argparse.ArgumentParser(add_help = True,
             prog='tool to generate a dictionary for brute-forcing alpha-numeric passwords that contain symbols',
                                     description="Python script to generate a wordlist or dictionary",
                                     usage='Use like so: python gen_dictionary.py --min 0 --max 10 '
                                           '--out dictionary.txt')

    parser.add_argument('--min', action='store', dest='min', help='minimum length of dictionary')
    parser.add_argument('--max', action='store', dest='max', help='maximum length of dictionary')
    parser.add_argument('--out', action='store', dest='out', help='output file destination')

    options = parser.parse_args()

    minlen = options.min
    maxlen = options.max
    outfile = options.out

    if minlen is None:
        print parser.print_usage()
        print "Minimum Length cannot be none. use --min [0-9]"
    if maxlen is None:
        print parser.print_usage()
        print "Maximum Length cannot be none. use --max [0-9]"
        print "WARNING - max length of 9 generates more than 119 quadrillion possibilities and may crash the computer"
    if outfile is None:
        print parser.print_usage()
        print "Outfile cannot be non. use --out absolute or relative path"

if __name__ == '__main__':
    main()
