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

    def _replace(self, lines, pat, fmt):
        pat = re.compile(pat)
        result = []
        for line in lines:
            m = pat.search(line)
            if m:
                line = fmt.format(*m.groups())
            result.append(line)

    def _get_file(self, accum, path):
        with open(path, 'r') as reader:
            for line in reader:
                accum.append(line)


class ReplaceInclusion(Base):
    '''
    HTML file inclusion marker: <div markdown="1" replacement="path-to-file.tex">...</div>
    =>
    LaTeX: content of file
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


class GlossaryEntry(Base):
    '''
    HTML glossary key: <strong id="g:LABEL">TEXT</strong>'
    =>
    LaTeX: \hypertarget{g:LABEL}{TEXT}\label{g:LABEL}
    '''

    def pre(self, lines):
        return self._replace(lines,
                             r'<strong id="(g:[^"]+)">([^<]+)</strong>',
                             r'<strong>==glossary=={0}=={1}==</strong>')

    def post(self, lines):
        return self._replace(lines,
                             r'==glossary==([^=]+)==([^=]+)==',
                             r'\hypertarget{{{0}}}{{{1}}}\label{{{0}}}')


class BibliographyEntry(Base):
    '''
    HTML bibliography key: <strong id="b:LABEL">TEXT</strong>'
    =>
    LaTeX: \hypertarget{b:LABEL}{TEXT}\label{g:LABEL}
    '''

    def pre(self, lines):
        return self._replace(lines,
                             r'<strong id="(b:[^"]+)">([^<]+)</strong>',
                             r'<strong>==citation=={0}=={1}==</strong>')

    def post(self, lines):
        return self._replace(lines,
                             r'==citation==([^=]+)==([^=]+)==',
                             r'\hypertarget{{{0}}}{{{1}}}\label{{{0}}}')


class Figure(Base):
    '''
    HTML figure: <figure id="f:LABEL"> <img src="PATH"> <figcaption>TEXT</figcaption> </figure>
    =>
    LaTeX: \begin{figure}[H]\label{f:LABEL}\centering\includegraphics{PATH}\caption{TEXT}\end{figure}
    '''

    def pre(self, lines):
        return self._replace(lines,
                             r'<figure +id="(f:.+)"> *<img +src="(.+)"> *<figcaption>(.+)</figcaption> *</figure>',
                             r'<strong>==figure=={0}=={1}=={2}==</strong>')

    def post(self, lines):
        return self._replace(lines,
                             r'==figure==([^=]+)==([^=]+)==([^=]+)==',
                             r'\begin{figure}[H]\label{{{0}}}\centering\includegraphics{{{1}}}\caption{{{2}}}\end{figure}')


class Command(Base):

    def pre(self, lines):
        return self._replace(lines,
                             r'<!-- +== +(.+) +-->',
                             r'==command=={{{0}}}==')

    def post(self, lines):
        return self.replace(lines,
                            r'==command==([^=]+)==',
                            r'{{{0}}}')


class Language(Base):

    def pre(self, lines):
        return self._replace(lines,
                             r'<div.+class="language-([^ ]+)',
                             r'==language=={{{0}}}==')

    def post(self, lines):
        return self.replace(lines,
                            r'==language==([^=]+)==',
                            r'\begin{{lstlisting}}[language={0}]')


# All handlers in pre order.
HANDLERS = [
    ReplaceInclusion,
    GlossaryEntry,
    BibliographyEntry,
    Figure,
    Command,
    Language
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
