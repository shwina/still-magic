#!/usr/bin/env python

'''
Check for unused or missing files compared to table of contents in YAML configuration.
'''

import sys
import re
import yaml
from util import report, usage


TITLE = 'Table of Contents'


def main(configPath, chapterFiles):
    configToc = read_config_toc(configPath)
    filesToc = normalize(chapterFiles) - {'index'}
    report(TITLE, 'missing',  configToc - filesToc)
    report(TITLE, 'unused', filesToc - configToc)


def read_config_toc(configPath):
    with open(configPath, 'r') as reader:
        config = yaml.load(reader)
    toc = config['toc']
    return {x.strip('/') for x in set(toc['lessons']) | set(toc['bib']) | set(toc['extras'])}


def normalize(filenames):
    return set([f.split('/')[1].split('.')[0] for f in filenames])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage('checkfiles /path/to/config /path/to/chapterfiles...')
    main(sys.argv[1], sys.argv[2:])
