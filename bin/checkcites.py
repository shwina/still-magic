#!/usr/bin/env python

import sys
import re

def main():
    bibFile, sourceFiles = sys.argv[1], sys.argv[2:]
    defined = getKeys(bibFile)
    used = getRefs(sourceFiles)
    report('unused', defined - used)
    report('undefined', used - defined)


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


def report(title, keys):
    if keys:
        print(title, ', '.join(sorted(keys)))


if __name__ == '__main__':
    main()
