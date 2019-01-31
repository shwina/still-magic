#!/usr/bin/env python

import sys
import os
import re
from util import get_toc_slugs, report


TITLE = 'Anchors'


def main(config_file, source_dir):
    header_pat = re.compile(r'^##\s+[^}]+{([^}]+)}\s*$')
    target_pat = re.compile(r'#s:([^-]+)')
    slugs = get_toc_slugs(config_file)
    result = set()
    for slug in slugs:
        path = os.path.join(source_dir, slug + '.md')
        with open(path, 'r') as reader:
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
