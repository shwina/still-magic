'''
Utilities.
'''

import sys
import os
import json
import yaml


def get_toc(config_path):
    '''Read the table of contents and return ToC section.'''
    with open(config_path, 'r') as reader:
        config = yaml.load(reader)
    return config['toc']


def get_sources(config_path, source_dir, with_index=True):
    '''
    Return a list of (slug, filename) pairs from the table of contents,
    including ('index', 'lang/index.md') unless told not to.
    '''
    toc = get_toc(config_path)
    slugs = toc['lessons'] + toc['bib'] + toc['extras']
    result = [(s, os.path.join(source_dir, '{}.md'.format(s))) for s in slugs]
    if with_index:
        result = [('index', os.path.join(source_dir, 'index.md'))] + result
    return result


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
