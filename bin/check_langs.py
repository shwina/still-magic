#!/usr/bin/env python

import sys
import os
from util import get_toc_slugs, report, usage


def main(config_file, source_dir):
    slugs = get_toc_slugs(config_file)
    result = set()
    for slug in slugs:
        path = os.path.join(source_dir, slug + '.md')
        with open(path, 'r') as reader:
            in_block = False
            for (i, line) in enumerate(reader):
                if not line.startswith('```'):
                    pass
                elif in_block:
                    in_block = False
                else:
                    in_block = True
                    if line.strip() == '```':
                        result.add('{} {:4d}'.format(path, i+1))
    report('Code Blocks', 'no language', result)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage('check_langs.py config_file source_dir')
    main(sys.argv[1], sys.argv[2])
