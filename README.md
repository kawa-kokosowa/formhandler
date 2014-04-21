formhandler
===========

Tested functional with Python 2.7.6 and Python 3.4.

Automate the development of a web/CGI script interface to a function.

In a couple of commands, in one CGI script, use a function to:

1. Provide an HTML form interface for that function.
2. Provide the HTML-ified evaluation of sending corresponding POST/GET fields to aforementioned function(s).

Includes tools for automatically converting data returned from a function, to HTML, e.g., dict > html, list > html, etc.

Written because I hate making "web interfaces" for data automation stuff at work (I do business logistics automation). Allowing you to use function(s) to generate HTML input form(s) AND handle displaying function output to the user, with one command.

# Get started:

1. python setup.py install
2. Launch testhttpd.py. This acts as a temporary testing web server. It should launch http://localhost:8080/ in a new web browser tab.
3. Open test.py in a file editor to see what's going on!

Note: you may need to chmod +X the proper cgi scripts. I also may need to change file headers to #!/usr/bin/python. You need to create the uploads and resources directory for the demo. Just make demo directory.

# Example Usage

Just view the source of test.py!

