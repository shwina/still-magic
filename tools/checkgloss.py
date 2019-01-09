#!/usr/bin/env python

'''
Check for unused and undefined glossary entries.
'''

import sys
import re
from util import report, usage


TITLE = 'Glossary Entries'
DEF = re.compile(r'\*\*.+?\*\*{:#(g:.+?)}', re.DOTALL)
REF = re.compile(r'\[.+?\]\(#(g:.+?)\)', re.DOTALL)


def main(filenames):
    defs = set()
    refs = set()
    for path in filenames:
        with open(path, 'r') as reader:
            doc = reader.read()
            defs.update({d for d in DEF.findall(doc)})
            refs.update({r for r in REF.findall(doc)})
    report(TITLE, 'unused', defs - refs)
    report(TITLE, 'undefined', refs - defs)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage('checkgloss.py glossFile [filename ...]')
    main(sys.argv[1:])
