import subprocess
import os
import optparse


def runvpn(fileName):
	'''	
	This function changes directory and starts
	openvpn on file in directory
	'''
	d = os.path.dirname(fileName)
	os.chdir(d)
	subprocess.call(["sudo","openvpn",fileName])

def main():
    parser = optparse.OptionParser('usage %prog "+ "-F <OpenVPN conf file name>')
    parser.add_option('-F', dest='fileName', type='string', help='specify OpenVPN conf file name')

    (options, args) = parser.parse_args()
    fileName = options.fileName
    if fileName == None:
        print parser.usage
        exit(0)
    else:
        runvpn(fileName)


if __name__ == '__main__':
    main()