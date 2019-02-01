#!/usr/bin/env python

'''
Do pre- and post-transformations required to produce clean LaTeX from Pandoc's Markdown-to-LaTeX.
'''

import sys
import os
import re
from util import usage, get_toc_slugs


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
        return result

    def _sub(self, lines, before, after):
        return [s.replace(before, after) for s in lines]


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
        return result

    def post(self, lines):
        pat = re.compile(r'==include==([^=]+)==')
        result = []
        for line in lines:
            m = pat.search(line)
            if m:
                filename = os.path.join(self.include_dir, m.group(1))
                with open(filename, 'r') as reader:
                    content = reader.readlines()
                    result.extend(content)
            else:
                result.append(line)
        return result


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
    '''
    HTML embedded command comment: <!-- == COMMMAND -->
    =>
    LaTeX command: COMMAND
    '''

    def pre(self, lines):
        return self._replace(lines,
                             r'<!-- +== +(.+) +-->',
                             r'==command=={{{0}}}==')

    def post(self, lines):
        return self._replace(lines,
                             r'==command==([^=]+)==',
                             r'{{{0}}}')


class Language(Base):
    '''
    HTML div opening language block: <div class="language-LANG"
    =>
    LaTeX listing with language: \begin{lstlisting}[language=LANG]
    '''

    def pre(self, lines):
        return self._replace(lines,
                             r'<div.+class="language-([^ ]+)',
                             r'==language=={{{0}}}==')

    def post(self, lines):
        return self._replace(lines,
                             r'==language==([^=]+)==',
                             r'\begin{{lstlisting}}[language={0}]')


class PdfToSvg(Base):
    '''
    LaTeX: /figures/FILENAME.svg => /figures/FILENAME.pdf
    '''

    def post(self, lines):
        return self._replace(lines,
                             r'/figures/(.+)\.svg}',
                             r'/figures/{{{0}}}.pdf}}')

class Citation(Base):
    '''
    LaTeX: hyperlink to multiple bibliography citations => hyperlink to each.
    '''

    def post(self, lines):
        def _fixup(match):
            keys = [s.strip() for s in match.group(1).split(',')]
            return '[' + ','.join(['\\hyperlink{{b:{}}}{{{}}}'.format(k, k) for k in keys]) + ']'

        pat = re.compile(r'\\hyperlink{BIB}{([^}]+)}')
        result = []
        for line in lines:
            result.append(pat.sub(_fixup, line))
        return result


class Quote(Base):
    '''
    LaTeX: unindent quotations.
    '''

    def post(self, lines):
        return self._sub(lines, r'\begin{quote}', r'\begin{quote}\setlength{\parindent}{0pt}')


class Section(Base):
    '''
    LaTeX: turn sections into chapters.
    '''

    def post(self, lines):
        return self._sub(lines, r'\section', r'\chapter')


class Subsection(Base):
    '''
    LaTeX: turn subsections into sections.
    '''

    def post(self, lines):
        return self._sub(lines, r'\subsection', r'\section')


class Subsubsection(Base):
    '''
    LaTeX: turn subsubsections into subsections.
    '''

    def post(self, lines):
        return self._sub(lines, r'\subsubsection', r'\subsection')


class Newline(Base):
    '''
    LaTeX: represent literal newline properly.
    '''

    def post(self, lines):
        return self._sub(lines, r'\texttt{\n}', r'\texttt{\textbackslash n}')

    
# All symmetric handlers in pre order.
BOTH = [
    ReplaceInclusion,
    GlossaryEntry,
    BibliographyEntry,
    Figure,
    Command,
    Language
]

# All post-only handlers in execution order.
POST = [
    PdfToSvg,
    Citation,
    Quote,
    Section,
    Subsection,
    Subsubsection,
    Newline
]

def pre_process(config_file, source_dir, include_dir):
    '''
    Apply all pre-processing handlers.
    '''
    lines = get_lines(config_file, source_dir)
    for handler in BOTH:
        lines = handler(include_dir).pre(lines)
    sys.stdout.writelines(lines)


def post_process(include_dir):
    '''
    Apply all post-processing handlers.
    '''
    lines = sys.stdin.readlines()
    for handler in reversed(BOTH):
        lines = handler(include_dir).post(lines)
    for handler in POST:
        lines = handler(include_dir).post(lines)
    sys.stdout.writelines(lines)


def get_lines(config_file, source_dir):
    slugs = get_toc_slugs(config_file, as_set=False)
    filenames = [os.path.join(source_dir, 'index.html')] \
        + [os.path.join(source_dir, s, 'index.html') for s in slugs]
    result = []
    for f in filenames:
        with open(f, 'r') as reader:
            lines = reader.readlines()
            lines = keep_main(lines)
            result.extend(lines)
    return result


def keep_main(lines):
    start = end = None
    for (i, line) in enumerate(lines):
        if '<!-- begin: main -->' in line:
            start = i
        elif '<!-- end: main -->' in line:
            end = i
            break
    return lines[start:end+1]


if __name__ == '__main__':
    USAGE = 'transform.py --pre config_file source_dir include_dir OR transform.py --post include_dir'
    if len(sys.argv) < 2:
        usage(USAGE)
    if sys.argv[1] == '--pre':
        if len(sys.argv) != 5:
            usage(USAGE)
        else:
            pre_process(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == '--post':
        if len(sys.argv) != 3:
            usage(USAGE)
        post_process(sys.argv[2])
    else:
        usage(USAGE)
