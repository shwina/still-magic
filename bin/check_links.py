#!/usr/bin/env python

'''
Check for unused and undefined links.
'''

import sys
import re
from util import get_sources, report, usage


LINKS_TITLE = 'Links'


def main(config_file, source_dir, links_file):
    source_files = [filename for (slug, filename) in get_sources(config_file, source_dir)]
    defs = read_defs(links_file)
    link_refs, internal_refs = read_refs(source_files)
    report(LINKS_TITLE, 'unused', defs - link_refs)
    report(LINKS_TITLE, 'undefined', link_refs - defs)


def read_defs(filename):
    pat = re.compile(r'\[(.+)\]:\s+.+')
    result = set()
    with open(filename, 'r') as reader:
        for line in reader:
            m = pat.search(line)
            if not m:
                continue
            key = m.group(1)
            assert key not in result, \
                'Duplicate key {} in {}'.format(key, filename)
            result.add(key)
    return result


def read_refs(filenames):
    code_pat = re.compile(r'```.+?```', re.DOTALL)
    link_pat = re.compile(r'\[[^\]]+\]\[([^\]]+)\]')
    internal_pat = re.compile(r'\[[^\]]+\]\(\.\.?/([^/)]+)[^)]*\)')
    links = set()
    internals = set()
    for f in filenames:
        with open(f, 'r') as reader:
            raw = reader.read()
            cooked = code_pat.sub('', raw)
            links |= set(link_pat.findall(cooked))
            internals |= set(internal_pat.findall(cooked))
    return links, internals


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage('checklinks.py config_file source_dir links_file')
    main(sys.argv[1], sys.argv[2], sys.argv[3])
