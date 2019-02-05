#!/usr/bin/env python

'''
Check that all anchors on level-2 headings are properly formatted and include the chapter slug.
'''

import sys
import os
import re
from util import get_sources, report


TITLE = 'Anchors'


def main(config_file, source_dir):
    header_pat = re.compile(r'^##\s+[^{]+{([^}]+)}\s*$')
    target_pat = re.compile(r'#s:([^-]+)')
    result = set()
    for (slug, filename) in get_sources(config_file, source_dir):
        with open(filename, 'r') as reader:
            for line in reader:
                anchor = header_pat.search(line)
                if not anchor:
                    continue
                m = target_pat.search(anchor.group(1))
                if (not m) or (m.group(1) != slug):
                    result.add('{}: "{}"'.format(slug, anchor.group(1)))
    report(TITLE, 'mismatched', result)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage('check_anchors.py config_file source_dir')
    main(sys.argv[1], sys.argv[2])
