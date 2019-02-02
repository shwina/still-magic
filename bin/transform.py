#!/usr/bin/env python

'''
Do pre- and post-transformations required to produce clean LaTeX from Pandoc's Markdown-to-LaTeX.
'''

import sys
import os
import re
from util import usage, get_toc

#-------------------------------------------------------------------------------

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

    def _regexp(self, lines, pat, fmt):
        pat = re.compile(pat)
        def f(match):
            return fmt.format(*match.groups())
        return [pat.sub(f, s) for s in lines]

    def _replace(self, lines, before, after):
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


class PdfToSvg(Base):
    '''
    LaTeX: /figures/FILENAME.svg => /figures/FILENAME.pdf
    '''

    def post(self, lines):
        return self._regexp(lines,
                            r'/figures/(.+)\.svg}',
                            r'/figures/{{{0}}}.pdf}}')


class SpecialCharacters(Base):
    '''
    LaTeX: accented characters replaced by LaTeX escapes.
    '''

    def post(self, lines):
        def _regexpall(s):
            for (raw, latex) in [('é', r"\'{e}"), ('ö', r'\"{o}')]:
                s = s.replace(raw, latex)
            return s
        return [_regexpall(s) for s in lines]

#-------------------------------------------------------------------------------

class CodeBlock(Base):
    '''
    HTML div opening language block: <div class="language-LANG"
    =>
    LaTeX listing with language: \begin{lstlisting}[language=LANG]
    '''

    def pre(self, lines):
        return self._regexp(lines,
                            r'(<div class="language-([^ ]+).*>)',
                            r'==language=={1}=={0}')

    def post(self, lines):
        lines = self._squash(lines)
        lines = self._regexp(lines,
                             r'==language==([^=]+)==\\begin{verbatim}',
                             r'\begin{{lstlisting}}[language={0}]')
        lines = self._replace(lines,
                              r'\begin{lstlisting}[language=text]',
                              r'\begin{lstlisting}[backgroundcolor=\color{verylightgray}]')
        lines = self._replace(lines,
                              r'\begin{verbatim}',
                              r'\begin{lstlisting}')
        lines = self._replace(lines,
                              r'\end{verbatim}',
                              r'\end{lstlisting}')
        return lines

    def _squash(self, lines):
        result = []
        pat = re.compile(r'==language==([^=]+)==')
        language = None
        for line in lines:
            if language:
                if not line.strip():
                    pass
                else:
                    result.append('==language=={}=={}'.format(language, line))
                    language = None
            else:
                m = pat.search(line)
                if m:
                    language = m.group(1)
                else:
                    result.append(line)
        return result

#-------------------------------------------------------------------------------

class BaseRegexp(Base):
    '''
    General HTML-to-temp-to-LaTeX transformation.
    Expects class variable MATCH_HTML, WRITE_TEMP, MATCH_TEMP, WRITE_LATEX
    '''

    def pre(self, lines):
        return self._regexp(lines, self.MATCH_HTML, self.WRITE_TEMP)

    def post(self, lines):
        return self._regexp(lines, self.MATCH_TEMP, self.WRITE_LATEX)


class Citation(BaseRegexp):
    '''
    HTML: hyperlink to multiple bibliography citations
    =>
    LaTeX: \cite{citations}
    '''

    MATCH_HTML = r'<a href="#BIB">([^<]+)</a>'
    WRITE_TEMP = r'==citation=={0}=='
    MATCH_TEMP = r'==citation==([^=]+)=='
    WRITE_LATEX = r'\cite{{{0}}}'


class GlossaryEntry(BaseRegexp):
    '''
    HTML glossary key: <strong id="g:LABEL">TEXT</strong>'
    =>
    LaTeX: \hypertarget{g:LABEL}{TEXT}\label{g:LABEL}
    '''

    MATCH_HTML = r'<strong id="(g:[^"]+)">([^<]+)</strong>'
    WRITE_TEMP = r'<strong>==glossary=={0}=={1}==</strong>'
    MATCH_TEMP = r'==glossary==([^=]+)==([^=]+)=='
    WRITE_LATEX = r'\hypertarget{{{0}}}{{{1}}}\label{{{0}}}'


class CrossRef(BaseRegexp):
    '''
    HTML cross-reference: <a class="xref" href="../SLUG/#s:IDENT">WORD NUMBER</a>
    =>
    LaTeX: WORD~\ref{#s:IDENT}
    '''

    MATCH_HTML = r'<a\s+class="xref"\s+href=".+/.+/#(s:[^"]+)">(.+)\s+([^<]+)</a>'
    WRITE_TEMP = r'==crossref=={0}=={1}=={2}=='
    MATCH_TEMP = r'==crossref==([^=]+)==([^=]+)==([^=]+)=='
    WRITE_LATEX = r'{1}~\ref{{{0}}}'


class Figure(BaseRegexp):
    '''
    HTML figure: <figure id="f:LABEL"> <img src="PATH"> <figcaption>TEXT</figcaption> </figure>
    =>
    LaTeX: \begin{figure}[H]\label{f:LABEL}\centering\includegraphics{PATH}\caption{TEXT}\end{figure}
    '''

    MATCH_HTML = r'<figure +id="(f:.+)"> *<img +src="(.+)"> *<figcaption>(.+)</figcaption> *</figure>'
    WRITE_TEMP = r'<strong>==figure=={0}=={1}=={2}==</strong>'
    MATCH_TEMP = r'==figure==([^=]+)==([^=]+)==([^=]+)=='
    WRITE_LATEX = r'\begin{figure}[H]\label{{{0}}}\centering\includegraphics{{{1}}}\caption{{{2}}}\end{figure}'


class Noindent(BaseRegexp):
    '''
    HTML embedded command comment: <!-- == COMMMAND -->
    =>
    LaTeX command: COMMAND
    '''

    MATCH_HTML = r'<!-- +== noindent +-->'
    WRITE_TEMP = r'==command==noindent=='
    MATCH_TEMP = r'==command==noindent==\n'
    WRITE_LATEX = r'\noindent'


#-------------------------------------------------------------------------------

class BaseStringMatch(Base):
    '''
    General temp-to-LaTeX transformation with pure string matching.
    Expects class variables MATCH_TEMP and WRITE_LATEX.
    '''

    def post(self, lines):
        return self._replace(lines, self.MATCH_TEMP, self.WRITE_LATEX)


class Quote(BaseStringMatch):
    '''
    LaTeX: unindent quotations.
    '''

    MATCH_TEMP = r'\begin{quote}'
    WRITE_LATEX = r'\begin{quote}\setlength{\parindent}{0pt}'


class BibliographyTitle(BaseStringMatch):
    '''
    LaTeX: don't number the bibliography as a chapter.
    '''

    MATCH_TEMP = r'\chapter{Bibliography}'
    WRITE_LATEX = r'\chapter*{Bibliography}'


class Midpoint(BaseStringMatch):
    '''
    Bibliography and the switch to appendices at midpoint.
    '''

    MATCH_TEMP = '==midpoint=='
    WRITE_LATEX = '\\bibliographystyle{abstract}\n\\bibliography{book}\n\\appendix'


class Section(BaseStringMatch):
    '''
    LaTeX: turn sections into chapters.
    '''

    MATCH_TEMP = r'\section'
    WRITE_LATEX = r'\chapter'


class Subsection(BaseStringMatch):
    '''
    LaTeX: turn subsections into sections.
    '''

    MATCH_TEMP = r'\subsection'
    WRITE_LATEX = r'\section'


class Subsubsection(BaseStringMatch):
    '''
    LaTeX: turn subsubsections into subsections.
    '''

    MATCH_TEMP = r'\subsubsection'
    WRITE_LATEX = r'\subsection'


class Newline(BaseStringMatch):
    '''
    LaTeX: represent literal newline properly.
    '''

    MATCH_TEMP = r'\texttt{\n}'
    WRITE_LATEX = r'\texttt{\textbackslash n}'

#-------------------------------------------------------------------------------

# All symmetric handlers.
BOTH = [
    ReplaceInclusion,
    GlossaryEntry,
    CrossRef,
    Figure,
    Noindent,
    CodeBlock,
    Citation
]

# All post-only handlers.
POST = [
    Newline,
    PdfToSvg,
    Quote,
    Section,
    Subsection,
    Subsubsection,
    BibliographyTitle,
    Midpoint,
    SpecialCharacters
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
    for handler in BOTH:
        lines = handler(include_dir).post(lines)
    for handler in POST:
        lines = handler(include_dir).post(lines)
    sys.stdout.writelines(lines)


def get_lines(config_file, source_dir):

    toc = get_toc(config_file)
    result = []

    for filename in _make_filenames(source_dir, toc['lessons']):
        _get_lines(result, filename)

    _get_lines(result, os.path.join(source_dir, 'bib', 'index.html'))

    result.append('==midpoint==\n')

    for filename in _make_filenames(source_dir, toc['extras']):
        _get_lines(result, filename)

    return result


def _make_filenames(source_dir, slugs):
    return [os.path.join(source_dir, s, 'index.html') for s in slugs]


def _get_lines(result, filename):
    with open(filename, 'r') as reader:
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
