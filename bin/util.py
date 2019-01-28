'''
Utilities.
'''

import sys
import yaml


def get_toc_slugs(config_path):
    '''Read the table of contents, returning a set of slugs.'''
    with open(config_path, 'r') as reader:
        config = yaml.load(reader)
    toc = config['toc']
    return set(toc['lessons']) | set(toc['bib']) | set(toc['extras'])


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
