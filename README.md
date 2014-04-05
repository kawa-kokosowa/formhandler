funcform
===========

Sometimes the web interface is an afterthought.

I've learned what I /really/ want from a web framework: as little work or involvement on my part as possible. So that's what funcform does.

This builds input forms from a function and then handles the POST/GET data, rendering the evaluation as HTML.

# Get started:

1. Launch testhttpd.py
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
print funcform(make_uppercase, reflect, reflect=types)
```

... which will process form input (and output the HTML-friendly evaluation of both make_uppercase and reflect), plus provide us an HTML input form when no POST/GET data is present.

