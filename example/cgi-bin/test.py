#! /usr/bin/env python
# example/test.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of FormHandler and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Demo/example CGI script to show developers how to use FormHandler.

This belongs to the example/ directory of the FormHandler project. See
README.asciidoc for more details.

Right now it has two forms: one which takes a string and converts
lowercase letters to uppercase ones, and another which takes an
image from upload/POST and displays it to the user.

"""

from formhandler.tpl import template
from formhandler.formhandler import FormHandler
import os


def make_uppercase(s):
    """Test function for converting a string to uppercase.

    Here is another test paragraph.

    Args:
      s (list): list containing string to make uppercase.

    """

    return s.upper()


def reflect(upload_file, save_directory):
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
handler = FormHandler(reflect, make_uppercase)
handler.reflect('upload_file', field_type='file',
                label='File to upload&hellip;')
handler.reflect('save_directory', field_type='select',
                options=['uploads', 'resources'],
                help_text='The directory to upload to.')
handler.make_uppercase('s', label='Text to transform')

# Output content/page
replacements = {'title': 'Demo Form'}
content = handler.html(replacements)

print('Content-Type: text/html\n')
print(content)

