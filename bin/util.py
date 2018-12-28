'''
Utilities.
'''

import sys


def report(title, group, values):
    '''Report missing/unused values.'''

    if values:
        print('{}: {}'.format(title, group))
        for v in sorted(values):
            print('  ', v)


def usage(message, status=1):
    print('Usage: {}'.format(message), file=sys.stderr)
    sys.exit(status)
