#!/usr/local/bin/python
"""For testing purposes only, don't seriously use this as your
primary HTTPD.

Seriously.

I mean, I'm pretty sure you can make the server execute itself, y'know?

"""


import os
import sys
import webbrowser
import SocketServer
import BaseHTTPServer
import CGIHTTPServer


LISTEN_ADDRESS = ''
LISTEN_PORT = 8080
PUBLIC_DIRECTORY = 'www'


class ThreadingCGIServer(SocketServer.ThreadingMixIn,
                   BaseHTTPServer.HTTPServer):

    pass


def httpd():
    """THIS IS A TOY. It is only here so users may test parsed
    contents before making them public.

    """

    handler = CGIHTTPServer.CGIHTTPRequestHandler
    handler.cgi_directories = ['/', 'resources']
    listen_info = (LISTEN_ADDRESS, LISTEN_PORT)
    server = ThreadingCGIServer(listen_info, handler)

    if not LISTEN_ADDRESS:
        listen_info = ('localhost', LISTEN_PORT)

    webbrowser.open('http://%s:%s/test.py' % listen_info)

    try:

        while 1:
            sys.stdout.flush()
            server.handle_request()

    except KeyboardInterrupt:
        print "Finished"


httpd()

