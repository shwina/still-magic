#!/usr/bin/env python

'''
Check for unused or missing files compared to table of contents in YAML configuration.
'''

import sys
import re
from util import readToc, report, usage


TITLE = 'Table of Contents'


def main(configPath, chapterFiles):
    configToc = readToc(configPath)
    filesToc = normalize(chapterFiles) - {'index'}
    report(TITLE, 'missing',  configToc - filesToc)
    report(TITLE, 'unused', filesToc - configToc)


def normalize(filenames):
    return set([f.split('/')[1].split('.')[0] for f in filenames])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checkfiles /path/to/config /path/to/chapterfiles...')
    main(sys.argv[1], sys.argv[2:])
