#!/usr/bin/env python

import sys
import os
import re
import yaml
from string import ascii_uppercase


SECTION_PAT = re.compile(r'^##\s+.+\s+\{#(s:.+)\}', re.MULTILINE)


def main(config_file, source_dir):
    with open(config_file, 'r') as reader:
        config = yaml.load(reader)
    lessons = config['toc']['lessons']
    extras = config['toc']['extras']
    keyed = {**dict(zip(lessons, ['Chapter {}'.format(str(i)) for i in range(1, len(lessons) + 1)])),
             **dict(zip(extras, ['Appendix {}'.format(c) for c in ascii_uppercase[:len(extras)]]))}
    result = {'s:{}'.format(k) : (k, keyed[k]) for k in keyed}
    [result.update(process(source_dir, k, keyed[k][1])) for k in keyed]
    print(result)


def process(source_dir, slug, base):
    filename = os.path.join(source_dir, '{}.md'.format(slug))
    with open(filename, 'r') as reader:
        content = reader.read()
    headings = SECTION_PAT.findall(content)
    numbered = zip(headings, range(1, len(headings) + 1))
    return {h : (slug, 'Section {}.{}'.format(base, i)) for (h, i) in numbered}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage('make_toc.py config_file source_dir')
    main(sys.argv[1], sys.argv[2])
