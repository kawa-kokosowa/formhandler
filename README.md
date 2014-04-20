formhandler
===========

Automate the development of a web/CGI script interface to a
function.

  1. Generates HTML forms: the HTML form(s) the CGI script provides utilizes data about the functions (introspection) to create the HTML form(s) (input interface to functions).
  2. Handles form(s) data: Each POST/GET field from the aforementioned form(s) is sent to its respective function and argument.
  3. Presents evaluations: the evaluation(s) of step #2 is then HTML-ified, and returned (output interface).

# In other words...

Pipe input from web form to a Python function, pipe output back to a web page. Make this process require as little code as possible.

Includes tools for automatically converting data returned from a function, to HTML, e.g., dict > html, list > html, etc.

# Get started:

1. Launch testhttpd.py. This acts as a temporary testing web server.
2. Open http://127.0.0.1:8080/test.py in a web browser.
3. Open test.py in a file editor to see what's going on!

Note: you may need to chmod +X the proper cgi scripts. I also may need to change file headers to #!/usr/bin/python. You need to create the uploads and resources directory for the demo. Just make demo directory.

# Example Usage

Just view the source of test.py!

