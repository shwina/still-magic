#!/usr/bin/env python

'''
Do pre- and post-transformations required to produce clean LaTeX from Pandoc's Markdown-to-LaTeX.
'''

import sys
from util import usage


class Base(object):
    '''
    Base transformation does nothing in either pre or post phase.
    '''

    def __init__(self, include_dir):
        self.include_dir = include_dir

    def pre(self, lines):
        return lines

    def post(self, lines):
        return lines

    def _get_file(self, accum, path):
        with open(path, 'r') as reader:
            for line in reader:
                accum.append(line)


class ReplaceInclusion(Base):
    '''
    Replace '<div markdown="1" replacement="ghp/mathjax-1.tex">...</div>' with named file.
    '''

    def pre(self, lines):
        start = re.compile(r'<div\s+replacement="([^"]+)">')
        end = re.compile(r'</div>')
        echo = True
        result = []
        for line in lines:
            if echo:
                m = start.search(line)
                if m:
                    echo = False
                    result.append('==include=={}==\n'.format(m.group(1)))
                else:
                    result.append(line)
            else:
                m = end.search(line)
                if m:
                    echo = True

    def post(self, lines):
        pat = re.compile(r'==include==([^=]+)==')
        for line in lines:
            m = pat.search(line)
            if m:
                self._get_file(lines, os.path.join(self.include_dir, m.group(1)))
            else:
                lines.append(line)


# All handlers in pre order.
HANDLERS = [
    Base
]


def main(phase):
    '''
    Apply all pre or post handlers.
    '''
    handlers = HANDLERS
    if phase == 'post':
        handlers.reverse()
    lines = sys.stdin.readlines()
    for cls in HANDLERS:
        h = cls()
        lines = getattr(h, phase)(lines)
    sys.stdout.writelines(lines)


if __name__ == '__main__':
    if (len(sys.argv) != 2) or (sys.argv[1] not in ['pre', 'post']):
        usage('transform.py [pre | post]')
    main(sys.argv[1])
