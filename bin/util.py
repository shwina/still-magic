'''
Utilities.
'''

import sys
import os
import re
import json
import yaml


CHARACTERS = {
    'ç': r"\c{c}",
    'é': r"\'{e}",
    'ë': r'\"{e}',
    'ö': r'\"{o}'
}
PROSE_FILE_FMT = '_{}/{}.md'            # lesson or appendix (%language, %slug)


def get_toc(config_file):
    '''Read the table of contents and return ToC section.'''
    with open(config_file, 'r') as reader:
        return yaml.load(reader)['toc']


def get_all_docs(config_file, language, with_index=True, remove_code_blocks=True):
    '''
    Return a list of (slug, filename, body, lines) tuples from the table of contents,
    including ('index', 'lang/index.md', lines) unless told not to.
    '''
    result = []
    if with_index:
        result.append(get_doc(language, 'index'))
    toc = get_toc(config_file)
    for section in toc:
        result.extend([get_doc(language, s) for s in toc[section]])
    return result


def get_doc(language, slug, remove_code_blocks=True):
    filename = PROSE_FILE_FMT.format(language, slug)
    with open(filename, 'r') as reader:
        body = reader.read()
    lines = body.split('\n')
    if remove_code_blocks:
        body = re.sub(r'```.+?```', '', body, flags=re.DOTALL)
    return (slug, filename, body, lines)


def get_crossref(filename):
    with open(filename, 'r') as reader:
        return json.load(reader)


def report(title, group, values):
    '''Report missing/unused values.'''
    if values:
        print('{}: {}'.format(title, group))
        for v in sorted(values):
            print('  ', v)


def usage(message, status=1):
    '''Display a usage message.'''
    print('Usage: {}'.format(message), file=sys.stderr)
    sys.exit(status)
