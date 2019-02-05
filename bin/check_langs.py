#!/usr/bin/env python

import sys
import os
from util import get_sources, report, usage


def main(config_file, source_dir):
    result = set()
    for (slug, filename) in get_sources(config_file, source_dir):
        with open(filename, 'r') as reader:
            in_block = False
            for (i, line) in enumerate(reader):
                if not line.startswith('```'):
                    pass
                elif in_block:
                    in_block = False
                else:
                    in_block = True
                    if line.strip() == '```':
                        result.add('{} {:4d}'.format(filename, i+1))
    report('Code Blocks', 'no language', result)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage('check_langs.py config_file source_dir')
    main(sys.argv[1], sys.argv[2])
