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


def main(srcDir, filenames):
    actual = findFiles(srcDir)
    expected = findMentions(filenames)
    report(TITLE, 'unused', actual - expected)
    report(TITLE, 'missing', expected - actual)


def findFiles(srcDir):
    prefixLen = len(srcDir + '/')
    unprefix = lambda x: x[prefixLen:]
    ignore = lambda x: x.endswith('~') or ('__pycache__' in x)
    return set([unprefix(x)
                for x in glob.iglob('{}/**/*.*'.format(srcDir), recursive=True)
                if not ignore(x)])


def findMentions(filenames):
    result = set()
    for fn in filenames:
        with open(fn, 'r') as reader:
            result |= set(MENTIONS.findall(reader.read()))
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checksrc.py srcDir filename [filename...]')
    main(sys.argv[1], sys.argv[2:])

