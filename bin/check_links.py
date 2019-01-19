#!/usr/bin/env python

'''
Check for unused and undefined links.
'''

import sys
import re
from util import readToc, report, usage


LINKS_TITLE = 'Links'
INTERNAL_TITLE = 'Internal References'


def main(configFile, linksFile, sourceFiles):
    toc = readToc(configFile)
    defs = readDefs(linksFile)
    linkRefs, internalRefs = readRefs(sourceFiles)
    report(LINKS_TITLE, 'unused', defs - linkRefs)
    report(LINKS_TITLE, 'undefined', linkRefs - defs)
    report(INTERNAL_TITLE, 'undefined', internalRefs - toc)


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
    linkPat = re.compile(r'\[[^\]]+\]\[([^\]]+)\]')
    internalPat = re.compile(r'\[[^\]]+\]\(\.\.?/([^)]+)\)')
    links = set()
    internals = set()
    for f in filenames:
        with open(f, 'r') as reader:
            data = reader.read()
            links |= set(linkPat.findall(data))
            internals |= set([x.rstrip('/') for x in internalPat.findall(data)])
    return links, internals


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checklinks.py configFile linksFile [filename ...]')
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
