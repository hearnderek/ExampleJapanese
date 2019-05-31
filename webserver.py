#!/usr/bin/python
# coding=utf-8
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import subprocess

PORT_NUMBER = 80

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        search = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('search', '')

        # Send the html message
        for val in search:
            decoded =  val.decode('utf-8')
            output = subprocess.Popen(["grep", decoded, '-rh', 'text/'], stdout=subprocess.PIPE).communicate()[0]
            self.wfile.write(output.replace('\n','<br><br>'))

        return

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
