#!/usr/local/bin/python
"""For testing purposes only, don't seriously use this as your
primary HTTPD.

Seriously.

I mean, I'm pretty sure you can make the server execute itself, y'know?

"""


import os
import sys
import webbrowser

try:
    from CGIHTTPServer import CGIHTTPRequestHandler
    from BaseHTTPServer import HTTPServer

except ImportError:
    from http.server import HTTPServer, CGIHTTPRequestHandler


LISTEN_ADDRESS = ''
LISTEN_PORT = 8080
PUBLIC_DIRECTORY = 'www'
CGI_DIRECTORIES = ['/', 'resources']


class Handler(CGIHTTPRequestHandler):
    cgi_directories = CGI_DIRECTORIES


listen_info = (LISTEN_ADDRESS, LISTEN_PORT)
httpd = HTTPServer(listen_info, Handler)

if not LISTEN_ADDRESS:
    listen_info = ('localhost', LISTEN_PORT)

webbrowser.open('http://%s:%s/test.py' % listen_info)
httpd.serve_forever()

