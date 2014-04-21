#!/usr/local/bin/python3.4
"""Project proposal manager.

An example of formhandler's capabilities.

"""

from formhandler.tpl import template
import sqlite3


def add_proposal(client_name, client_phone, client_email, client_relation,
                 organization_name, **kwargs):

            return client_name


# Test!
reflect.field_types = {'upload_file': 'file',
                       'save_directory': ['select', 'uploads', 'resources'],}
content = template(reflect, make_uppercase,
                   replacements={'title': 'Demo Form'})

# Output!
print('Content-Type: text/html\n')
print(content)

