#!/usr/bin/env python

'''
Check for unused and undefined citations.
'''

import sys
import re
from util import report, usage


TITLE = 'Citations'


def main(bib_file, source_files):
    defined = get_keys(bib_file)
    used = get_refs(source_files)
    report(TITLE, 'unused', defined - used)
    report(TITLE, 'undefined', used - defined)


def get_keys(filename):
    pat = re.compile(r'{:#b:([^}]+)}')
    data = open(filename, 'r').read()
    keys = pat.findall(data)
    return set(keys)


def get_refs(filenames):
    key_pat = re.compile(r'\[([^\]]+)\]\(#BIB\)')
    title_pat = re.compile(r'/bib/#b:([^\)]+)')
    result = set()
    for f in filenames:
        with open(f, 'r') as reader:
            data = reader.read()
            cites = [x.split(',') for x in key_pat.findall(data)]
            result |= set([key for sublist in cites for key in sublist])
            result |= set(title_pat.findall(data))
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checkcites.py bib_file source_file [source_file ...]')
    main(sys.argv[1], sys.argv[2:])
