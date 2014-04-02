#!/usr/local/bin/python
"""Form handler: sometimes the web interface is an afterthought.
Lillian Lynn Mahoney

PURPOSE:
  Pipe input from web form to a Python function, pipe output back to a
  web page. Make this process require as little code as possible.

  Includes tools for automatically converting data returned from a
  function, to HTML, e.g., dict > html, list > html, etc.

RECOMMENDATIONS:
  Do not even consider formhandler in your development process. Then,
  make a single function which acts as the interface/form handler, to
  be utilized with formhandler.

DEVELOPER NOTES:
  - Makes heavy usage of the "cgi" module.

USAGE/EXAPMLES:
  >>>

BONUS:
  Includes tool for editing parts of the template, an example
  tool which edits an SQLITE database/table.

"""

import os
import cgi
import cgitb; cgitb.enable()
import inspect
from cStringIO import StringIO


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

    """

    html = StringIO()
    html.write('<section class="form-help">')
    html.write('<pre>')
    html.write(inspect.getdoc(function))
    html.write('</pre>')
    html.write('</section>')

    return html.getvalue()


def iter_dicts_table(iter_dicts):
    """Convert an iterable sequence of dictionaries (all of which with
    identical keys) to an HTML table.

    Args:
      iter_dicts: an iterable sequence (list, tuple) of dictionaries,
        dictionaries having identical keys.

    Returns:
      str|None: HTML tabular representation of a Python iterable sequence of
        dictionaries which share identical keys. Returns None if table
        is not consistent (dictionary keys).

    """

    # first check key consistency
    first_keys = iter_dicts[0].keys()

    for d in evaluation:

        if d.keys() != first_keys:

            return None

    html = StringIO()
    keys = ['<td>%(' + key + ')s</td>' for key in iter_dicts[0]]
    row = '<tr>' + ''.join(keys) + '</tr>'
    html.write('<table>')

    for d in iter_dicts:
        html.write(row % d)

    html.write('</table>')

    return html.getvalue()


# The juice ###################################################################


class FormHandler(object):

    def __init__(self, function, argument_types=None):
        self.function = function
        self.name = function.__name__
        self.argument_types = argument_types or {}

        args, __, kwargs, __ = inspect.getargspec(function)
        self.args = args or []
        self.kwargs = kwargs or {}

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

        for argument in self.args + self.kwargs.keys():
            # text input is the default kind of argument
            argument_type = self.argument_types.get(argument, 'text')

            # <select>?
            if type(argument_type) is type(list()):
                option = '<option value="%s">%s</option>'
                options = [option % (o, o.title()) for o in argument_type]
                options = '\n'.join(options)
                select = '<select name="{0}" id="{0}">\n{1}\n</select>'
                label = '<label for="{0}">' + var_title(argument) + '</label>'
                new_field = (label + '\n' + select).format(argument, options)

            elif argument_type in ('text', 'file'):
                html_input_field = ('<label for="{0}">{1}:</label>\n'
                                    '<input type="{2}" name="{0}" id="{0}">'
                                    '<br>\n')
                new_field = html_input_field.format(argument,
                                                    var_title(argument),
                                                    argument_type)

            else:
                raise Exception('invalid argument type')

            fields.append(new_field)

        fields = '\n'.join(fields)

        # The about section describing this form, based on docstring.
        about = docstring_html(self.function)

        # Function name as a hidden field so that it may trigger the
        # evaluation of the function upon form submission!
        hidden_trigger_field = ('<input type="hidden" name="{0}" id="{0}" '
                                'value="true">').format(self.name)

        # Put all the pieces together...
        form = StringIO()
        form.write('<form enctype="multipart/form-data" method="post">')
        form.write('<fieldset>')
        form.write('<legend>' + title + '</legend>')
        form.write(hidden_trigger_field)

        if about:
            form.write(about)

        if fields:
            form.write(fields)

        form.write('<input type="submit" value="Process: %s">' % title)
        form.write('</fieldset>')
        form.write('</form>')

        return form.getvalue()

    def evaluate(self, form):

        # If the function name is not in POST/GET, we're providing
        # the HTML input form.
        if not form.getvalue(self.name):

            return self.to_form(), None

        # Find corellated arguments in mind. Assume text input,
        # unless noted in arg_map
        arg_values = ([file_or_text(form, arg) for arg in self.args]
                      if self.args else None)
        kwargs = ({k: file_or_text(form, k) for k in self.kwargs}
                   if self.kwargs else None)

        # REQUIRED field missing in POST/GET.
        if None in arg_values:
            missing_args = list()

            for i, value in enumerate(arg_values):

                if value is None:
                    missing_args.append(self.args[i])

            message = ('<p><strong><strong>Error:</strong> missing '
                       'arguments: %s.' % ', '.join(missing_args))

            return message, form

        if arg_values and kwargs:
            evaluation = self.function(*arg_values, **kwargs)
        elif arg_values:
            evaluation = self.function(*arg_values)
        elif kwargs:
            evaluation = self.function(**kwargs)

        # Now we must analyze the evaluation of the function, in order
        # to properly format the results to HTML.
        evaluation_type = type(evaluation)
        eval_is = lambda x: evaluation_type is type(x())

        # ... Evaluation is a string; just use paragraph formatting.
        if eval_is(str):

            return paragraphs(evaluation), form

        # ... Evaluation is iterable sequence; further options below...
        elif eval_is(list) or eval_type(tuple):

            # Evaluation is an iterable sequence of dictionaries?
            if type(evaluation[0]) is type(dict()):
                possible_table = iter_dicts_table(evaluation)

                if possible_table:

                    return possible_table, form

        # Evaluation is simply a dictionary! Create a definition list.
        elif eval_is(dict):
            pass

        # This SHOULDN'T be possible.
        raise Exception('IDK how this is possible!')


def file_or_text(form, form_field):
    """Will return a cgi.fileitem or the corresponding string
    for form_field in form.

    Args:
      form (cgi.FieldStorage): the current cgi field storage
        session.
      form_field (str): grab this field's value.

    Returns:
      str|fileitem: returns string if text field, returns cgi
        module fileitem if a file.

    """

    if not form.getvalue(form_field):

        return None

    fileitem = form[form_field]

    if not fileitem.filename:

        return form.getvalue(form_field)

    return fileitem


def form_handler(*functions, **kwargs):
    """Just form_handler for multiple functions, while returning
    ONLY the function evaluation on POST/GET.

    Args:
      **kwargs: function_name: dictionary. Dictionary is argument
        to type mapping...

    """

    form = cgi.FieldStorage()
    output = ''

    for function in functions:
        handler = FormHandler(function)
        handler.argument_types = kwargs.get(handler.name, {})
        evaluation, post_get = handler.evaluate(form)

        if post_get:
            back_to_input = ('<form><input type="submit" '
                             'value="Back to Form"></form>')

            return evaluation + back_to_input

        else:
            output += evaluation

    return output


