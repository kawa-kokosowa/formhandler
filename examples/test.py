#!/usr/local/bin/python3.4
"""An example of formhandler's capabilities.

"""

from formhandler.tpl import template
from formhandler.formhandler import FuncPrep
import os


# TEST!
def make_uppercase(s):
    """Test function for converting a string to uppercase.

    Here is another test paragraph.

    Args:
      s (list): list containing string to make uppercase.

    """

    return s.upper()


def reflect(upload_file, save_directory=None):
    """Simply display an image from path.

    Lets formhandler do the image saving part.

    Will create directories if not exist...

    Args:
      upload_file (cgi.file_item?)
      save_directory (str): the directory in which the file goes.

    """

    filename, file_contents = upload_file

    if save_directory and save_directory in ('resources', 'uploads'):

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        path = os.path.join(save_directory, filename)

    else:
        path = filename

    with open(path, 'wb') as f:
        f.write(file_contents)

    return '<img src="/%s" alt="user uploaded file" />' % path


# Configure HTML/argument relations
funcprep = FuncPrep(reflect)
funcprep('upload_file', field_type='file', label='File to upload&hellip;')
funcprep('save_directory', field_type='select',
         options=['uploads', 'resources'])

funcprep = FuncPrep(make_uppercase)
funcprep('s', label='Text to transform')

# Output!
content = template(reflect, make_uppercase,
                   replacements={'title': 'Demo Form'})
print('Content-Type: text/html\n')
print(content)

