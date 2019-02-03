'''
Utilities.
'''

import sys
import yaml


def get_toc(config_path):
    '''Read the table of contents and return ToC section.'''
    with open(config_path, 'r') as reader:
        config = yaml.load(reader)
    return config['toc']


def get_toc_slugs(config_path):
    '''Return a set of all slugs in the ToC.'''
    toc = get_toc(config_path)
    return set(toc['lessons'] + toc['bib'] + toc['extras'])


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
