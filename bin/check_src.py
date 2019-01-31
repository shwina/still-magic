#!/usr/bin/env python

'''
Check for missing and unused source file inclusions.
'''

import sys
import glob
import re
from util import report, usage


MENTIONS = re.compile(r'{:\s+title="([^"]+)"}')
TITLE = 'Source Files'


def main(src_dir, filenames):
    actual = find_files(src_dir)
    expected = find_mentions(filenames)
    report(TITLE, 'unused', actual - expected)
    report(TITLE, 'missing', expected - actual)


def find_files(src_dir):
    prefix_len = len(src_dir + '/')

    def unprefix(x):
        return x[prefix_len:]

    def ignore(x):
        return x.endswith('~') or ('__pycache__' in x)

    filenames = glob.iglob('{}/**/*.*'.format(src_dir), recursive=True)
    return set([unprefix(x) for x in filenames if not ignore(x)])


def find_mentions(filenames):
    result = set()
    for fn in filenames:
        with open(fn, 'r') as reader:
            result |= set(MENTIONS.findall(reader.read()))
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checksrc.py src_dir filename [filename...]')
    main(sys.argv[1], sys.argv[2:])
