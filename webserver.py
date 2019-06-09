#!/usr/bin/python
# coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import subprocess

PORT_NUMBER = 80

# could just use lists, but hey let's use this dictionary for O(1) lookups
banned_words = {'wlwmanifest.xml':0, 'index.php':0}
banned_ips_file = 'banned_ips'
banned_ips = {}

try:
    with open(banned_ips_file, 'r') as bifp:
        for line in bifp:
            banned_ips[line.strip()]=0
except:
    pass

web_html = 'load me'
with open('web.html') as wfp:
    web_html = wfp.read()

index_html = 'load me'
with open('index.html') as ifp:
    index_html = ifp.read()

def get_line_weight (line):

    weight = line[0:4]
    print(weight)
    if weight.isdigit():
        return float(weight)
    else:
        return 0

    

def grep_documents(word):
    output = subprocess.Popen(["grep", word, '-rh', 'text/'], stdout=subprocess.PIPE).communicate()[0]
    split = output.split("\n")
    split.sort()
    return "\n".join(split)

def grep_word_list(word):
    output = subprocess.Popen(["grep", word, 'wordlist.txt'], stdout=subprocess.PIPE).communicate()[0]
    split = output.split("\n")
    # split.sort()
    return "\n".join(split)

#This class will handles any incoming request from the browser 
class base_handler(BaseHTTPRequestHandler):


    def do_403(self):
        self.send_response(403)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        return
    
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

    def do_api_word_get(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()

        # take all values of url parameter 'search'
        search = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('search', '')

        # Send the html message
        for val in search:
            output = grep_word_list(val.decode('utf-8'))
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
        word = ''
        reading = ''

        # Send the html message
        for val in search:
            word = val
            doc_grep = grep_documents(val.decode('utf-8'))
            text += doc_grep
            word_grep = grep_word_list(val.decode('utf-8'))
            reading += word_grep

        self.wfile.write(web_html.replace('$VALUE',text).replace('$WORD',word).replace('$READING',reading))
    
    #Handler for the GET requests
    def do_GET(self):
        # Anti hacker fun
        if self.client_address[0] in banned_ips:
            self.do_403()
            return

        if self.path.split('/')[-1] in banned_words:
            banned_ips[self.client_address[0]] = 0
            with open(banned_ips_file, 'a') as bip:
                bip.write(self.client_address[0] + '\n')
                
            self.do_403()
            return

        if self.path.startswith('/api/'):
            self.do_api_get()
        elif self.path.startswith('/web'):
            self.do_web_get()
        elif self.path.startswith('/word'):
            self.do_api_word_get()
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
