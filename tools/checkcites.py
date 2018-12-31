#!/usr/bin/env python

'''
Check for unused and undefined citations.
'''

import sys
import re
from util import report, usage


TITLE = 'Citations'


def main(bibFile, sourceFiles):
    defined = getKeys(bibFile)
    used = getRefs(sourceFiles)
    report(TITLE, 'unused', defined - used)
    report(TITLE, 'undefined', used - defined)


def getKeys(filename):
    pat = re.compile(r'{:#b:([^}]+)}')
    data = open(filename, 'r').read()
    keys = pat.findall(data)
    return set(keys)


def getRefs(filenames):
    keyPat = re.compile(r'\[([^\]]+)\]\(#BIB\)')
    titlePat = re.compile(r'/bib/#b:([^\)]+)')
    result = set()
    for f in filenames:
        with open(f, 'r') as reader:
            data = reader.read()
            cites = [x.split(',') for x in keyPat.findall(data)]
            result |= set([key for sublist in cites for key in sublist])
            result |= set(titlePat.findall(data))
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checkcites.py bibFile sourceFile [sourceFile ...]')
    main(sys.argv[1], sys.argv[2:])
