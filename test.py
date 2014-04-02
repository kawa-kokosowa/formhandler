#!/usr/local/bin/python
"""An example of formhandler's capabilities.

"""

from formhandler import form_handler
import os


# TEST!
def make_uppercase(s):
    """Test function for converting a string to uppercase.

    Here is another test paragraph.

    Args:
      s (str): string to make uppercase.

    """

    return s.upper()


# Test!
def reflect(upload_file, save_directory=None):
    """Simply display an image from path.

    Lets formhandler do the image saving part.

    upload_file (cgi.file_item?)
    save_directory (str): the directory in which the file goes.

    """

    if save_directory and save_directory in ('resources', 'uploads'):
        path = os.path.join(save_directory, upload_file.filename)
    else:
        path = upload_file.filename

    with file(path, 'wb') as f:
        f.write(upload_file.file.read())

    return '<img src="/%s" alt="user uploaded file" />' % path


# Test!
types = {'upload_file': 'file', 'save_directory': ['uploads', 'resources'],}
print 'Content-Type: text/html\n'
print form_handler(make_uppercase, reflect, reflect=types)

