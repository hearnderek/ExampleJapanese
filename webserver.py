#!/usr/bin/python
# coding=utf-8
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import subprocess

PORT_NUMBER = 80

def grep_documents(word):
    return subprocess.Popen(["grep", word, '-rh', 'text/'], stdout=subprocess.PIPE).communicate()[0]


#This class will handles any incoming request from the browser 
class base_handler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()

        # take all values of url parameter 'search'
        search = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('search', '')

        # Send the html message
        for val in search:
            output = grep_documents(val.decode('utf-8'))
            self.wfile.write(output.replace('\n','<br><br>'))

        return

try:
    #Create a web server and define the handler to manage incoming requests
    server = HTTPServer(('', PORT_NUMBER), base_handler)
    print 'Started httpserver on port ' , PORT_NUMBER
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
