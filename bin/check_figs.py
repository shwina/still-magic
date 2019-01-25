#!/usr/bin/env python

'''Check figures.'''


import sys
import os
import re
from util import report, usage


TITLE = 'Figures'


def main(figure_dir, filenames):
    available = list_figures(figure_dir)
    required = find_references(filenames)
    report(TITLE, 'unused', subtract(available, required))
    report(TITLE, 'undefined', required - available)


def list_figures(figure_dir):
    ignore = lambda x: x.endswith('.xml')
    return set([x for x in os.listdir(figure_dir) if not ignore(x)])


def find_references(filenames):
    pat = re.compile(r'<img\s+src=".+/figures/([^"]+)"')
    result = set()
    for f in filenames:
        with open(f, 'r') as reader:
            data = reader.read()
            result |= set(pat.findall(data))
    return result


def subtract(available, required):
    make_stem = lambda x: x.split('.')[0]
    stemmed = {}
    for filename in available:
        stem = make_stem(filename)
        if stem in stemmed:
            stemmed[stem].add(filename)
        else:
            stemmed[stem] = {filename}
    result = available.copy()
    for req_name in required:
        if req_name in result:
            stem = make_stem(req_name)
            for availName in stemmed[stem]:
                result.remove(availName)
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('Usage: checkfig.py /path/to/figure/directory filename [filename...]')
    main(sys.argv[1], sys.argv[2:])
