#!/usr/bin/env python

'''
Check for unused and undefined links.
'''

import sys
import re
from util import report, usage


TITLE = 'Links'


def main(linksFile, sourceFiles):
    defs = readDefs(linksFile)
    refs = readRefs(sourceFiles)
    report(TITLE, 'unused', defs - refs)
    report(TITLE, 'undefined', refs - defs)


def readDefs(filename):
    pat = re.compile(r'\[(.+)\]:\s+.+')
    result = set()
    with open(filename, 'r') as reader:
        for line in reader:
            m = pat.search(line)
            if not m: continue
            key = m.group(1)
            assert key not in result, \
                'Duplicate key {} in {}'.format(key, filename)
            result.add(key)
    return result


def readRefs(filenames):
    pat = re.compile(r'\[[^\]]+\]\[([^\]]+)\]')
    result = set()
    for f in filenames:
        with open(f, 'r') as reader:
            data = reader.read()
            matches = pat.findall(data)
            result |= set(matches)
    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage('checklinks.py linksFile [filename ...]')
    main(sys.argv[1], sys.argv[2:])
