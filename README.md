formhandler
===========

Sometimes the web interface is an afterthought.

I've learned what I /really/ want from a web framework: as little work or involvement on my part as possible. So that's what formhandler does.

In ONE command you can have a CGI script which will act as the HTML input form (for sending data to function), and then it will also handle post/get data--utilized for evaluating form input, and providing HTML output from the evaluation. All (mostly) auto-magically.

# Get started:

1. Launch testhttpd.py
2. Open http://127.0.0.1:8080/test.py in a web browser.
3. Open test.py in a file editor to see what's going on!

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

... which will process form input (and output the HTML-friendly evaluation of both make_uppercase and reflect), plus provide us a form like this:

```html
<form enctype="multipart/form-data" method="post">
<fieldset>
<legend>Make Uppercase</legend>
<input type="hidden" name="make_uppercase" id="make_uppercase" value="true"><section class="form-help">
<pre>
Test function for converting a string to uppercase.

Here is another test paragraph.

Args:
  s (str): string to make uppercase.</pre>
</section>
<label for="s">S:</label>
<input type="text" name="s" id="s"><br>
<input type="submit" value="Process: Make Uppercase">
</fieldset>
</form>

<form enctype="multipart/form-data" method="post">
<fieldset>
<legend>Reflect</legend>
<input type="hidden" name="reflect" id="reflect" value="true"><section class="form-help">
<pre>
Simply display an image from path.

Lets formhandler do the image saving part.

upload_file (cgi.file_item?)
save_directory (str): the directory in which the file goes.</pre>
</section>
<label for="upload_file">Upload File:</label>
<input type="file" name="upload_file" id="upload_file"><br>

<label for="save_directory">Save Directory</label>
<select name="save_directory" id="save_directory">
<option value="uploads">Uploads</option>
<option value="resources">Resources</option>
</select><input type="submit" value="Process: Reflect">
</fieldset>
</form>
```

There is currently no real thought put into templating.
