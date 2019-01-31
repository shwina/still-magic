'''
Utilities.
'''

import sys
import yaml


def get_toc_slugs(config_path, as_set=True):
    '''Read the table of contents, returning a list of slugs.'''
    with open(config_path, 'r') as reader:
        config = yaml.load(reader)
    toc = config['toc']
    result = toc['lessons'] + toc['bib'] + toc['extras']
    if as_set:
        result = set(result)
    return result


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
