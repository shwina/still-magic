#!/usr/bin/env python

'''
Check that all cross-references resolve.
'''

import sys
import os
import re
from util import get_crossref, get_source_filenames, report

def main(config_file, source_dir, toc_file):
    pat = re.compile(r'\[([^\]]+)\]\(#REF\)')
    crossref = set(get_crossref(toc_file).keys())
    result = set()
    for filename in get_source_filenames(config_file, source_dir):
        with open(filename, 'r') as reader:
            for line in reader:
                for actual in pat.findall(line):
                    if actual not in crossref:
                        result.add('{}: {}'.format(filename, actual))
    report('Cross References', 'missing', result)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage('check_crossref.py config_file source_dir toc_file')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
