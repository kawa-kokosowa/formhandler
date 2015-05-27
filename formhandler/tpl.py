"""tpl: super simple templater.
Lillian Lynn Mahoney

"""

import os


TEMPLATE_ROOT = 'tpl'


def template(content, head_filename=None, foot_filename=None,
             replacements=None):
    """A simple way to generate forms.

    Args:
      head_filename (str):
      foot_filename (str):
      replacements (dict): {find: replace}; requiers at least "content"
        and likely that header uses "title".

    """

    head_filename = head_filename or 'head-default.html'
    foot_filename = foot_filename or 'foot-default.html'
    head = open(os.path.join(TEMPLATE_ROOT, head_filename)).read()
    foot = open(os.path.join(TEMPLATE_ROOT, foot_filename)).read()
    pieces = {
              'title': '',
              'within head': '',
             }

    if replacements:
        pieces.update(replacements)

    pieces['head'] = head.format(**pieces)
    pieces['foot'] = foot.format(**pieces)
    pieces['content'] = content

    return '''
           {head}

           <section id="content" class="content">

             <h1>{title}</h1>
             {content}

           </section>

           {foot}
           '''.format(**pieces)

