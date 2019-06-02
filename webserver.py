#!/usr/bin/python
# coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import subprocess

PORT_NUMBER = 80
web_html = 'load me'
mobile_html = 'load me'
with open('web.html') as wfp:
    web_html = wfp.read()
with open('mobile.html') as mfp:
    mobile_html = mfp.read()


def grep_documents(word):
    return subprocess.Popen(["grep", word, '-rh', 'text/'], stdout=subprocess.PIPE).communicate()[0]


#This class will handles any incoming request from the browser 
class base_handler(BaseHTTPRequestHandler):

    def do_404(self):
        self.send_response(404)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        return

    def do_api_get(self):
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

    def do_web_get(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(web_html)
        return
    
    def do_mobile_get(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(mobile_html)
        return

    #Handler for the GET requests
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.do_api_get()
        elif self.path.startswith('/web'):
            self.do_web_get()
        elif self.path.startswith('/m'):
            self.do_mobile_get()
        else:
            self.do_404()
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
