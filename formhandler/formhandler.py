#!/usr/local/bin/python
"""formhandler: sometimes the web interface is an afterthought.
Lillian Lynn Mahoney

Automate the development of a web/CGI script interface to a function.

Tested functional with Python 2.7.6 and Python 3.4.

In a couple of commands, in one CGI script, use a function to:

  1. Provide an HTML form interface for that function.
  2. Provide the HTML-ified evaluation of sending corresponding
     POST/GET fields to aforementioned function(s).

Includes tools for automatically converting data returned from a
function, to HTML, e.g., dict > html, list > html, etc.

I was tired of making and updating  web interfaces to various scripts
I've written at work. Various people use various scripts through super
simple CGI scripts.

DEVELOPER NOTES:
  - Needs some prettification; will probably use BeautifulSoup...
  - Soon I'll include an example which is a SQLITE3 table editor.
  - Will have automatic form validation (for defined argument data
    types).
  - Should mark arg fields as required!
  - Needs kwarg and arg support!

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


# these should all go to config module!
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
FIELD_DESCRIPTION = '''
                    <div class="fhandler-field_desc">
                      <label for="{name}">{label}</label>
                      <p class="fhandler-field_desc-help">{help}</p>
                    </div>
                    '''
SELECT = '''
         <select name="{name}" id="{name}"{required}>
           <optgroup label="{label}&hellip;">
             {options}
           </optgroup>
         </select>
         '''
HTML_INPUT_FIELD = '''
                   <input type="{input type}" 
                          name="{name}"
                          id="{name}"{required}>
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


def get_params():
    """Get all fields send in get/post, use a well organized
    dictionary!

    Uses cgi.FieldStorage() so you can only use this once to get
    your CGI field dictionary.

    Returns:
      dict: POST/GET fields. Key is field name. If value is file, value
        becomes tuple(filename, file contents). Value could also either
        be a string, or a list of values (as with check boxes).

        {
         'name': 'lillian mahoney',
         'resume': ('configured_upload_dir/my_resume.pdf', file_data),
         'availability': ['monday', 'tuesday', 'friday']
        }
        

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


class Field(object):

    def __init__(self, function, name, field_type=None, options=None,
                 label=None, argument=None, required=False, help_text=None):
        """HTML field representation of an argument.

        Extends function argument meta data.

        """

        self.field_type = field_type or 'text'
        self.options = options
        self.argument = argument or name
        self.label = label or var_title(name)
        self.help_text = ('<p>' + help_text + '</p>'
                          if help_text else ' ')

        if self.argument in function.args:
            self.required = True
        else:
            self.required = required

    def __str__(self):

        return self.to_html()

    def to_html(self):
        arg = {
               'name': self.argument,
               'help': self.help_text,
               'type': self.field_type,
               'label': self.label,
               'required': ' required' if self.required else ' ',
              }

        if self.field_type == 'select':
            option = '<option value="%s">%s</option>'
            options = [option % (o, var_title(o)) for o in self.options]
            arg['options'] = '\n'.join(options)

            return (FIELD_DESCRIPTION + SELECT).format(**arg)

        elif self.field_type in ['checkbox', 'radio']:
            items = []

            for option in self.options:
                parts = {
                         'option': option,
                         'list type': self.field_type,
                         'option title': var_title(option),
                        }
                parts.update(arg)
                field = (FIELD_DESCRIPTION + HTML_INPUT_FIELD).format(**parts)
                items.append(field)

            return '\n'.join(items)

        # pattern
        elif self.field_type in ('text', 'file'):
            parts = {'input type': self.field_type}
            parts.update(arg)

            return (FIELD_DESCRIPTION + HTML_INPUT_FIELD).format(**parts)

        else:

            raise Exception(('invalid arg type for %s' % argument_name,
                              arg['type'],))


class FuncPrep(object):

    def __init__(self, function):
        """Prepares a function so that it may be used to generate
        forms with form_handler()/FormHandler().

        Automate the relations between HTML input fields and
        the function arguments themselves.

        Conform meta data about a function, as attributes of that
        function.

        """

        self.function = function
        self.function.name = function.__name__
        self.function.fields = {}

        args, __, kwargs, __ = inspect.getargspec(self.function)
        self.function.args = args or []
        self.function.kwargs = kwargs or {}

    def __call__(self, name, **kwargs):
        """Relate an HTML field to an argument.

        The data is actually primarily about the HTML field itself!

        Args:
            **kwargs: keyword arguments for Field()

        """

        # should use Field()
        field = Field(self.function, name, **kwargs)
        self.function.fields.update({field.argument: field})

        return None


class Form(object):

    def __init__(self, function):
        """HTML form and its resulting page (from function).

        Args:
          function (func): Function to use for generating the HTML form
            and its resulting page.

        """

        self.function = function

        if not hasattr(function, 'fields'):
            relations = FuncPrep(function)

        self.evaluation = None
        self.params = None

    def to_form(self):
        """Returns the HTML input form for a function.

        Returns:
          str: HTML input form, for submitting arguments to this
            very form.

        """

        # Create HTML input labels and respective fields,
        # based on (keyword) argument names and arg_map (above).
        # Create said fields for required_fields and optional_fields.
        fields = []
        kwargs_keys = [k for k in self.function.kwargs]

        for argument_name in (self.function.args + kwargs_keys):

            if argument_name in self.function.fields:
                fields.append(self.function.fields[argument_name].to_html())
            else:
                fields.append(Field(self.function, argument_name).to_html())

        # build form_parts...
        form_parts = {
                      'title': var_title(self.function.name),
                      'fields': '\n'.join(fields),

                      # Section describing this form, based on docstring.
                      'about': docstring_html(self.function) or '',

                      # Function name as hidden field so it may trigger the
                      # evaluation of the function upon form submission!
                      'hidden trigger field': ('<input type="hidden" id="{0}"'
                                               'name="{0}" value="true">'
                                               .format(self.function.name)),
                     }

        return FORM.format(**form_parts)

    def evaluate(self, form):
        """HTML pag eresulting from submitting this form's input form.

        Args:
          form (dict): See get_params().

        Returns:
          None: Sets self.params and self.evaluation.

        """

        # If the function name is not in POST/GET, we're providing
        # the HTML input form.
        if self.function.name not in form:
            self.evaluation = self.to_form()
            self.params = None

            return None

        # Find corellated arguments in mind. Assume text input,
        # unless noted in arg_map
        arg_values = ([form[arg] for arg in self.function.args]
                      if self.function.args else None)
        kwargs = ({k: form[k] for k in self.function.kwargs}
                  if self.function.kwargs else None)

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
                possible_table = iter_dicts_table(evaluation, check=True)

                if possible_table:
                    self.evaluation = possible_table
                    self.params = form

                    return None

        # Evaluation is simply a dictionary! Create a definition list.
        elif isinstance(evaluation, dict):

            pass

        # This SHOULDN'T be possible.
        raise Exception('Unhandled evaluation type!')


class FormHandler(object):

    def __init__(self, *args):
        """Note: move TPL bull over here?"""
        self.functions = args
        self.relations = {}

        for function in args:
            form = FuncPrep(function)
            setattr(self, form.function.name, form)

    def html(self, replacements=None):
        """Just form_handler for multiple functions, while returning
        ONLY the function evaluation on POST/GET.

        """

        form = get_params()
        output = ''

        for function in self.functions:
            handler = Form(function)
            handler.evaluate(form)

            if handler.params:

                return handler.evaluation + BACK_TO_INPUT

            else:
                output += handler.evaluation

        return output

