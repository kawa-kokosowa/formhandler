#!/usr/local/bin/python
"""formhandler: sometimes the web interface is an afterthought.
Lillian Lynn Mahoney

Automate the development of a web/CGI script interface to a
function.

  1. Generates HTML forms: the HTML form(s) the CGI script provides
     utilizes data about the functions (introspection) to create
     the HTML form(s) (input interface to functions).
  2. Handles form(s) data: Each POST/GET field from the aforementioned
     form(s) is sent to its respective function and argument.
  3. Presents evaluations: the evaluation(s) of step #2 is then
     HTML-ified, and returned (output interface).

SUMMARY:
  Pipe input from web form to a Python function, pipe output back to a
  web page. Make this process require as little code as possible.

  Includes tools for automatically converting data returned from a
  function, to HTML, e.g., dict > html, list > html, etc.

DEVELOPER NOTES:
  - Needs some prettification; will probably use BeautifulSoup...
  - Soon I'll include an example which is a SQLITE3 table editor.
  - Will have automatic form validation (for defined argument data
    types).

"""

import os
import cgi
import cgitb; cgitb.enable()
import inspect

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


# CONFIG/CONSTANTS ############################################################


FORM = '''
       <form enctype="multipart/form-data" method="post" class="formhandler">
         <fieldset>
           <legend>{title}</legend>
           {about}
           {hidden trigger field}
           {fields}
           <input type="submit" value="submit">
         </fieldset>
       </form>
       '''
SELECT = '''
         <label for="{name}">{title}</label>
         <select name="{name}" id="{name}">
           {options}
         </select>
         '''
HTML_INPUT_FIELD = '''
                   <label for="{name}">
                     {title}
                   </label>
                   <input type="{input type}" 
                          name="{name}"
                          id="{name}">
                   '''
FORM_DESCRIPTION = '''
                   <section class="form-help">
                     <pre>{0}</pre>
                   </section>
                   '''
BACK_TO_INPUT = '''
                <form class="formhandler">
                  <input type="submit" value="Back to Form">
                </form>
                '''
ERROR_MISSING_ARGS = '<p><strong>Error:</strong> missing arguments: %s.</p>'


# GENERIC PYTHON DATA > HTML ##################################################


# Python variable name to user-friendly name.
var_title = lambda s: s.replace('_', ' ').title()


# Simply convert a string into HTML paragraphs.
paragraphs = lambda s: '\n\n'.join(['<p>%s</p>' % p for p in s.split('\n\n')])


def docstring_html(function):
    """Makes some nice HTML out of a function's DocString, attempting
    Google's style guide (see: my code!).

    A work in progress. I will try to use someone else's library
    for this!

    Boilerplate--AT THE MOMENT! Will be an actual parser in the future.

    """

    return FORM_DESCRIPTION.format(inspect.getdoc(function))


def iter_dicts_table(iter_dicts, classes=None, check=False):
    """Convert an iterable sequence of dictionaries (all of which with
    identical keys) to an HTML table.

    Args:
      iter_dicts (iter): an iterable sequence (list, tuple) of
        dictionaries, dictionaries having identical keys.
      classes (str): Is the substitute for <table class="%s">.
      check (bool): check for key consistency!

    Returns:
      str|None: HTML tabular representation of a Python iterable sequence of
        dictionaries which share identical keys. Returns None if table
        is not consistent (dictionary keys).

    """

    # check key consistency
    if check:
        first_keys = iter_dicts[0].keys()

        for d in iter_dicts:

            if d.keys() != first_keys:

                return None

    table_parts = {}
    table_parts['classes'] = ' class="%s"' % classes if classes else ''
    table_parts['thead'] = ''.join(['<th>%s</th>' % k for k in iter_dicts[0]])

    # tbody
    keys = ['<td>%(' + key + ')s</td>' for key in iter_dicts[0]]
    row = '<tr>' + ''.join(keys) + '</tr>'
    table_parts['tbody'] = '\n'.join([row % d for d in iter_dicts])

    return '''
           <table{classes}>
             <thead>
               <tr>{thead}</tr>
             </thead>
             <tbody>
               {tbody}
             </tbody>
           </table>
           '''.format(**table_parts)


# The juice ###################################################################


class FormHandler(object):

    def __init__(self, function):
        """Automate HTML interfaces to Python functions.

        function (func): the function to interface with. I suggest you
          assign function.field_types, since the default field type
          is a text input field.

        """

        self.function = function
        self.name = function.__name__

        if hasattr(function, 'field_types'):
            self.field_types = function.field_types
        else:
            self.field_types = {}

        args, __, kwargs, __ = inspect.getargspec(function)
        self.args = args or []
        self.kwargs = kwargs or {}

        self.evaluation = None
        self.params = None

    def to_form(self):
        """Returns the HTML input form for a function.

        Returns:
          str: HTML input form, for submitting arguments to a python
            function, via POST/GET.

        """

        # Form configuration/pre-setup.
        title = var_title(self.name)

        # Create HTML input labels and respective fields,
        # based on (keyword) argument names and arg_map (above).
        # Create said fields for required_fields and optional_fields.
        fields = []

        for argument in self.args + [k for k in self.kwargs]:
            # argument_type may be 'text', 'file', or a Python list,
            # representing options in a select field.
            arg = {
                   'name': argument,
                   'title': var_title(argument),
                   'type': self.field_types.get(argument, 'text'),
                  }

            if isinstance(arg['type'], list):
                # could denote select, checkbox, radio
                # in first element!
                # build <select> <options> from the list
                # denoted as the argument type
                # first element must be what type of choice selection
                list_type = arg['type'][0]
                options = arg['type'][1:]

                if list_type == 'select':
                    option = '<option value="%s">%s</option>'
                    options = [option % (o, var_title(o)) for o in options]
                    arg['options'] = '\n'.join(options)
                    fields.append(SELECT.format(**arg))

                elif list_type in ['checkbox', 'radio']:
                    items = []

                    for option in options:
                        parts = {
                                 'option': option,
                                 'list type': list_type,
                                 'option title': var_title(option),
                                }
                        parts.update(arg)
                        field = '''
                                <label for="{option}">
                                  <input type="{list type}" id="{option}"
                                         name="{name}" value="{option}">
                                  {option title}
                                </label>
                                '''.format(**parts)
                        items.append(field)

                    fields.append('\n'.join(items))

            elif arg['type'] in ('text', 'file'):
                parts = {'input type': arg['type']}
                parts.update(arg)
                fields.append(HTML_INPUT_FIELD.format(**parts))

            else:

                raise Exception('invalid argument type')

        # build form_parts...
        form_parts = {
                      'title': title or '',
                      'fields': '\n'.join(fields),

                      # Section describing this form, based on docstring.
                      'about': docstring_html(self.function) or '',

                      # Function name as hidden field so it may trigger the
                      # evaluation of the function upon form submission!
                      'hidden trigger field': ('<input type="hidden" id="{0}"'
                                               'name="{0}" value="true">'
                                               .format(self.name)),
                     }

        return FORM.format(**form_parts)

    def evaluate(self, form):
        """Evaluate function data and parse as HTML.

        Args:
          Form: see get_params().

        Returns:
          None: sets self.params, self.evaluation

        """

        # If the function name is not in POST/GET, we're providing
        # the HTML input form.
        if self.name not in form:
            self.evaluation = self.to_form()
            self.params = None

            return None

        # Find corellated arguments in mind. Assume text input,
        # unless noted in arg_map
        arg_values = ([form[arg] for arg in self.args]
                      if self.args else None)
        kwargs = ({k: form[k] for k in self.kwargs}
                  if self.kwargs else None)

        # REQUIRED field missing in POST/GET.
        if None in arg_values:
            missing_args = list()

            for i, value in enumerate(arg_values):

                if value is None:
                    missing_args.append(self.args[i])

            message = ERROR_MISSING_ARGS % ', '.join(missing_args)
            self.evaluation = message
            self.params = form

            return None

        if arg_values and kwargs:
            evaluation = self.function(*arg_values, **kwargs)
        elif arg_values:
            evaluation = self.function(*arg_values)
        elif kwargs:
            evaluation = self.function(**kwargs)

        # Now we must analyze the evaluation of the function, in order
        # to properly format the results to HTML.

        # ... Evaluation is a string; just use paragraph formatting.
        if isinstance(evaluation, str):
            self.evaluation = paragraphs(evaluation)
            self.params = form

            return None

        # ... Evaluation is iterable sequence; further options below...
        elif (isinstance(evaluation, list)
              or isinstance(evaluation, tuple)):

            # Evaluation is an iterable sequence of dictionaries?
            if isinstance(evaluation[0], dict):
                possible_table = iter_dicts_table(evaluation)

                if possible_table:
                    self.evaluation = paragraphs(evaluation)
                    self.params = form

                    return None

        # Evaluation is simply a dictionary! Create a definition list.
        elif isinstance(evaluation, dict):

            pass

        # This SHOULDN'T be possible.
        raise Exception('Unhandled evaluation type!')


def get_params():
    """Get all fields send in get/post, use a well organized
    dictionary!

    """

    params = {}
    fields = cgi.FieldStorage() 

    for param in fields.keys():

        if fields[param].filename:
            params[param] = (fields[param].filename, fields[param].file.read())

            continue

        item = fields.getvalue(param)

        if isinstance(item, list) or isinstance(item, str):
            params[param] = item

    return params


def form_handler(*args):
    """Just form_handler for multiple functions, while returning
    ONLY the function evaluation on POST/GET.

    Args:
      *args: functions to be interfaced with.

    """

    form = get_params()
    output = ''

    for function in args:
        handler = FormHandler(function)
        handler.evaluate(form)

        if handler.params:

            return handler.evaluation + BACK_TO_INPUT

        else:
            output += handler.evaluation

    return output
