#!/usr/bin/env python

'''
Check for unused or missing files compared to table of contents in YAML configuration.
'''

import sys
import re
from util import get_toc_slugs, report, usage


TITLE = 'Table of Contents'


def main(config_path, source_files):
    config_toc = get_toc_slugs(config_path)
    files_toc = normalize(source_files) - {'index'}
    report(TITLE, 'missing',  config_toc - files_toc)
    report(TITLE, 'unused', files_toc - config_toc)


def normalize(filenames):
    return set([f.split('/')[1].split('.')[0] for f in filenames])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checkfiles /path/to/config /path/to/chapterfiles...')
    main(sys.argv[1], sys.argv[2:])
