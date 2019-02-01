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

    def _sub(self, lines, before, after):
        return [s.sub(before, after) for s in lines]

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
        return self.replace(lines,
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
        return self.replace(lines,
                            r'==language==([^=]+)==',
                            r'\begin{{lstlisting}}[language={0}]')


class PdfToSvg(Base):
    '''
    LaTeX: /figures/FILENAME.svg => /figures/FILENAME.pdf
    '''

    def post(self, lines):
        return self._replace(lines,
                             r'/figures/(.+)\.svg}',
                             r'/figures/{{{0}}}.pdf}')

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
            result.append(pat.sub(fixup, line))
        return result


class Quote(Base):
    '''
    LaTeX: unindent quotations.
    '''

    def post(self, lines):
        self._sub(lines, r'\begin{quote}', r'\begin{quote}\setlength{\parindent}{0pt}')


class Section(Base):
    '''
    LaTeX: turn sections into chapters.
    '''

    def post(self, lines):
        self._sub(lines, r'\section', r'\chapter')


class Subsection(Base):
    '''
    LaTeX: turn subsections into sections.
    '''

    def post(self, lines):
        self._sub(lines, r'\subsection', r'\section')


class Subsubsection(Base):
    '''
    LaTeX: turn subsubsections into subsections.
    '''

    def post(self, lines):
        self._sub(lines, r'\subsubsection', r'\subsection')


class Newline(Base):
    '''
    LaTeX: represent literal newline properly.
    '''

    def post(self, lines):
        self._sub(lines, r'\texttt{\n}', r'\texttt{\textbackslash n}')

    
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
    Chapter,
    Section,
    Subsection,
    Subsubsection,
    Newline
]

def main(phase):
    '''
    Apply all pre or post handlers.
    '''

    lines = sys.stdin.readlines()

    handlers = BOTH
    if phase == 'post':
        handlers = reversed(handlers)
    for cls in handlers:
        lines = getattr(cls(), phase)(lines)

    if phase == 'post':
        for cls in POST:
            lines = cls().post(lines)

    sys.stdout.writelines(lines)


if __name__ == '__main__':
    if (len(sys.argv) != 2) or (sys.argv[1] not in ['pre', 'post']):
        usage('transform.py [pre | post]')
    main(sys.argv[1])
