# Check that language is set.  Do NOT set 'LANG', as that would override the platform's LANG setting.
ifndef lang
$(warning Please set 'lang' with 'lang=en' or similar.)
lang=en
endif

# Project stem.
STEM=still-magic

# Tools.
JEKYLL=jekyll
PANDOC=pandoc
LATEX=pdflatex
PYTHON=python

# Language-dependent settings.
DIR_MD=_${lang}
PAGES_MD=$(wildcard ${DIR_MD}/*.md)
BIB_MD=${DIR_MD}/bib.md
DIR_HTML=_site/${lang}
PAGES_HTML=${DIR_HTML}/index.html $(patsubst ${DIR_MD}/%.md,${DIR_HTML}/%/index.html,$(filter-out ${DIR_MD}/index.md,${PAGES_MD}))
DIR_TEX=tex/${lang}
BIB_TEX=${DIR_TEX}/book.bib
ALL_TEX=${DIR_TEX}/all.tex
BOOK_PDF=${DIR_TEX}/${STEM}.pdf

# Controls
all : commands

## commands    : show all commands.
commands :
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g'

## serve       : run a local server.
serve :
	${JEKYLL} serve -I

## site        : build files but do not run a server.
site :
	${JEKYLL} build

## pdf         : generate PDF from LaTeX source.
pdf : ${BOOK_PDF}

## bib         : regenerate the Markdown bibliography from the BibTeX file.
bib : ${BIB_MD}

# ----------------------------------------

# Regenerate PDF once 'all.tex' has been created.
${BOOK_PDF} : ${ALL_TEX}
	cd ${DIR_TEX} \
	&& ${LATEX} -jobname=${STEM} book \
	&& ${LATEX} -jobname=${STEM} book

# Create the unified LaTeX file (separate target to simplify testing).
# + 'sed' to pull glossary entry IDs out into '==g==' blocks (because Pandoc throws them away).
# + 'sed' to pull bibliography entry IDs out into '==b==' blocks (because Pandoc throws them away).
# + 'sed' to stash figure information (because Pandoc...).
# + 'sed' to un-comment embedded LaTeX commands '<!-- == command -->' before Pandoc erases them.
# + 'sed' to insert text signalling language type of code listing.
# ! Pandoc
# - 'tail' to strip out YAML header.
# - 'sed' to add language type flag to code listing environment.
# - 'sed' to restore embedded LaTeX commands (need to strip out the newline Pandoc introduces after the command).
# - 'sed' to restore figures.
# - 'sed' to turn SVG inclusions into PDF inclusions.
# - 'sed' to convert '====' blocks into LaTeX labels.
# - 'python' to convert bibliography citations (because 'sed' can't handle multiple keys).
# - 'sed' to suppress indentation inside quotes (so that callout boxes format correctly).
# - 'sed' to bump section headings back up.
# - 'sed' (twice) to convert 'verbatim' environments
${ALL_TEX} : ${PAGES_HTML} Makefile
	node js/stitch.js _config.yml _site ${lang} \
	| ${PYTHON} bin/replacement.py --pre \
	| sed -E -e 's!<strong id="(g:[^"]+)">([^<]+)</strong>!<strong>==glossary==\1==\2==</strong>!' \
	| sed -E -e 's!<strong id="(b:[^"]+)">([^<]+)</strong>!<strong>==citation==\1==\2==</strong>!' \
	| sed -E -e 's!<figure +id="(.+)"> *<img +src="(.+)"> *<figcaption>(.+)</figcaption> *</figure>!==figure==\1==\2==\3==!' \
	| sed -E -e 's/<!-- +== +(.+) +-->/==command==\1==/' \
	| sed -E -e 's!(<div.+class="language-([^ ]+))!==language==\2==\1!' \
	| ${PANDOC} --wrap=preserve -f html -t latex -o - \
	| tail -n +6 \
	| sed -E -e '/==language==.+==/{N;N;s/\n/ /g;}' \
	| sed -E -e 's!==language==(css)== *\\begin\{verbatim\}!\\begin{lstlisting}!' \
	| sed -E -e 's!==language==(text)== *\\begin\{verbatim\}!\\begin{lstlisting}[backgroundcolor=\\color{verylightgray}]!' \
	| sed -E -e 's!==language==([^=]+)== *\\begin\{verbatim\}!\\begin{lstlisting}[language=\1]!' \
	| sed -E -e 's!\\begin{verbatim}!\\begin{lstlisting}!' \
	| sed -E -e 's!\\end{verbatim}!\\end{lstlisting}!' \
	| sed -E -e '/==command==.+==/{N;s/\n/ /;}' -e 's!==command==(.+)==!\1!' -e s'!\\textbackslash{}!\\!' \
	| sed -E -e 's!==figure==([^=]+)==([^=]+)==([^=]+)==!\\begin{figure}[H]\\label{\1}\\centering\\includegraphics{\2}\\caption{\3}\\end{figure}!' \
	| sed -E -e 's!\.svg}!\.pdf}!' \
	| sed -E -e 's!==citation==([^=]+)==([^=]+)==!\\hypertarget{\1}{\2}\\label{\1}!' \
	| sed -E -e 's!==glossary==([^=]+)==([^=]+)==!\\hypertarget{\1}{\2}\\label{\1}!' \
	| ${PYTHON} bin/cites.py \
	| sed -E -e 's!\\begin{quote}!\\begin{quote}\\setlength{\\parindent}{0pt}!' \
	| sed -E -e 's!\\section!\\chapter!' \
	| sed -E -e 's!\\subsection!\\section!' \
	| sed -E -e 's!\\subsubsection!\\subsection!' \
	| sed -E -e 's!\\texttt\{\\n\}!\\texttt\{\\textbackslash n\}!g' \
	| sed -E -e 's!\\protect\\hyperlink\{([^}]+)\}\{CHAPTER\}!Chapter~\\ref{\1}!g' \
	| ${PYTHON} bin/replacement.py --post _includes \
	> ${ALL_TEX}

# Create all the HTML pages once the Markdown files are up to date.
${PAGES_HTML} : ${PAGES_MD}
	${JEKYLL} build

# Create the bibliography Markdown file from the BibTeX file.
${BIB_MD} : ${BIB_TEX} bin/bib2md.py
	bin/bib2md.py ${lang} < ${DIR_TEX}/book.bib > ${DIR_MD}/bib.md

# Dependencies with HTML file inclusions.
${DIR_HTML}/%/index.html : $(wildcard _includes/%/*.*)

## ----------------------------------------

## check       : check everything.
check :
	@make lang=${lang} check_cites
	@make lang=${lang} check_figs
	@make lang=${lang} check_gloss
	@make lang=${lang} check_links
	@make lang=${lang} check_src
	@make lang=${lang} check_toc

## check_cites : list all missing or unused bibliography entries.
check_cites : ${BIB_MD}
	@bin/check_cites.py ${DIR_MD}/bib.md ${PAGES_MD}

## check_figs  : list all missing or unused figures.
check_figs :
	@bin/check_figs.py figures ${PAGES_MD}

## check_gloss : check that all glossary entries are defined and used.
check_gloss :
	@bin/check_gloss.py ${PAGES_MD}

## check_links : check that all external links are defined and used.
check_links :
	@bin/check_links.py _config.yml _includes/links.md ${PAGES_MD} _includes/contributing.md

## check_src   : check source file inclusion references.
check_src :
	@bin/check_src.py src ${PAGES_MD}

## check_toc   : check consistency of tables of contents.
check_toc :
	@bin/check_toc.py _config.yml ${PAGES_MD}

## ----------------------------------------

## spelling    : compare words against saved list.
spelling :
	@cat ${PAGES_MD} | bin/uncode.py | aspell list | sort | uniq | comm -2 -3 - .words

## undone      : which files have not yet been done?
undone :
	@grep -l 'undone: true' _en/*.md

## words       : count words in finished files.
words :
	@for filename in $$(fgrep -L 'undone: true' ${PAGES_MD}); do printf '%6d %s\n' $$(cat $$filename | bin/uncode.py | wc -w) $$filename; done | sort -n -r
	@printf '%6d %s\n' $$(cat ${PAGES_MD} | bin/uncode.py | wc -w) 'total'

## ----------------------------------------

## clean       : clean up junk files.
clean :
	@rm -r -f _site dist bin/__pycache__
	@rm -r -f tex/*/all.tex tex/*/*.aux tex/*/*.bbl tex/*/*.blg tex/*/*.log tex/*/*.out tex/*/*.toc
	@find . -name '*~' -delete
	@find . -name .DS_Store -prune -delete

## settings    : show macro values.
settings :
	@echo "JEKYLL=${JEKYLL}"
	@echo "DIR_MD=${DIR_MD}"
	@echo "PAGES_MD=${PAGES_MD}"
	@echo "BIB_MD=${BIB_MD}"
	@echo "DIR_HTML=${DIR_HTML}"
	@echo "PAGES_HTML=${PAGES_HTML}"
	@echo "DIR_TEX=${DIR_TEX}"
	@echo "BIB_TEX=${BIB_TEX}"
	@echo "ALL_TEX=${ALL_TEX}"
	@echo "BOOK_PDF=${BOOK_PDF}"
