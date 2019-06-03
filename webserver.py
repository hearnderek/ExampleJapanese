#!/usr/bin/python
# coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import subprocess

PORT_NUMBER = 80

web_html = 'load me'
with open('web.html') as wfp:
    web_html = wfp.read()

index_html = 'load me'
with open('index.html') as ifp:
    index_html = ifp.read()

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
            self.wfile.write(output)
        return

    def do_index_get(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(index_html)

    def do_web_get(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()

        # take all values of url parameter 'search'
        search = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('Search', '')
        text = ''

        # Send the html message
        for val in search:
            output = grep_documents(val.decode('utf-8'))
            text += output

        self.wfile.write(web_html.replace('$VALUE',text))
    
    #Handler for the GET requests
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.do_api_get()
        elif self.path.startswith('/web'):
            self.do_web_get()
        else:
            self.do_index_get()
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
