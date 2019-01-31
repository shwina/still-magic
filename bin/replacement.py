#!/usr/bin/env python

'''
Handle replacements in source code before and after Pandoc.
'''

import sys
import os
import re
from util import usage


def main(preprocessing, include_dir):
    if preprocessing:
        pre()
    else:
        post(include_dir)


def pre():
    start = re.compile(r'<div\s+replacement="([^"]+)">')
    end = re.compile(r'</div>')
    echo = True
    for line in sys.stdin:
        if echo:
            m = start.search(line)
            if m:
                echo = False
                sys.stdout.write('==include=={}==\n'.format(m.group(1)))
            else:
                sys.stdout.write(line)
        else:
            m = end.search(line)
            if m:
                echo = True


def post(include_dir):
    pat = re.compile(r'==include==([^=]+)==')
    for line in sys.stdin:
        m = pat.search(line)
        if m:
            copy_file(os.path.join(include_dir, m.group(1)))
        else:
            sys.stdout.write(line)


def copy_file(path):
    with open(path, 'r') as reader:
        data = reader.read()
        sys.stdout.write(data)


if __name__ == '__main__':
    if (len(sys.argv) == 2) and (sys.argv[1] == '--pre'):
        main(True, None)
    elif (len(sys.argv) == 3) and (sys.argv[1] == '--post'):
        main(False, sys.argv[2])
    else:
        usage('replacement.py [--pre | --post include_dir]')
