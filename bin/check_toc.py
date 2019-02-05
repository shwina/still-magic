#!/usr/bin/env python

'''
Check for unused or missing files vs. table of contents in configuration.
'''

import sys
import re
from util import get_sources, report, usage


TITLE = 'Table of Contents'


def main(config_path, source_files):
    config_toc = {slug for (slug, filename) in get_sources(config_path, '', False)}
    files_toc = normalize(source_files) - {'index'}
    report(TITLE, 'missing',  config_toc - files_toc)
    report(TITLE, 'unused', files_toc - config_toc)


def normalize(filenames):
    return set([f.split('/')[1].split('.')[0] for f in filenames])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checkfiles /path/to/config /path/to/chapterfiles...')
    main(sys.argv[1], sys.argv[2:])
