#!/usr/bin/env python

'''Check figures.'''


import sys
import os
import re
from util import report, usage


TITLE = 'Figures'


def main(figDir, filenames):
    available = listFigures(figDir)
    required = findReferences(filenames)
    report(TITLE, 'unused', subtract(available, required))
    report(TITLE, 'undefined', required - available)


def listFigures(figDir):
    ignore = lambda x: x.endswith('.xml')
    return set([x for x in os.listdir(figDir) if not ignore(x)])


def findReferences(filenames):
    pat = re.compile(r'<img\s+src=".+/figures/([^"]+)"')
    result = set()
    for f in filenames:
        with open(f, 'r') as reader:
            data = reader.read()
            result |= set(pat.findall(data))
    return result


def subtract(available, required):
    makeStem = lambda x: x.split('.')[0]
    stemmed = {}
    for filename in available:
        stem = makeStem(filename)
        if stem in stemmed:
            stemmed[stem].add(filename)
        else:
            stemmed[stem] = {filename}
    result = available.copy()
    for reqName in required:
        if reqName in result:
            stem = makeStem(reqName)
            for availName in stemmed[stem]:
                result.remove(availName)
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('Usage: checkfig.py /path/to/figure/directory filename [filename...]')
    main(sys.argv[1], sys.argv[2:])
