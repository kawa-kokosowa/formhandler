#!/usr/local/bin/python
# example/testhttpd.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of FormHandler and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Server the current directory via a debugging CGI/HTTP server.

Don't use this as your primary HTTPD. Once you run testhttpd.py it
should open the correct URI for test.py in a new tab of your web
browser.

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

