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

Say we want a web interace for these functions (see: test.py):

```python
def make_uppercase(s):
    """This description shows up in the form."""
    return s.upper()

def reflect(upload_file, save_directory=None):
    """Simply display an uploaded image."""

    if save_directory and save_directory in ('resources', 'uploads'):
        path = os.path.join(save_directory, upload_file.filename)
    else:
        path = upload_file.filename

    with file(path, 'wb') as f:
        f.write(upload_file.file.read())

    return '<img src="/%s" alt="user uploaded file" />' % path
```

All we have to to is:

```python
# overrides default input types; a list is <select>
types = {'upload_file': 'file', 'save_directory': ['uploads', 'resources'],}
print 'Content-Type: text/html\n'
print form_handler(make_uppercase, reflect, reflect=types)
```

... which will process form input (and output the HTML-friendly evaluation of both make_uppercase and reflect), plus provide us an HTML input form when no POST/GET data is present.

