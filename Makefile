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
BIB_TEX=${DIR_TEX}/${STEM}.bib
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
	&& ${LATEX} ${STEM} \
	&& ${LATEX} ${STEM}

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
	| sed -E -e 's!<strong id="(g:[^"]+)">([^<]+)</strong>!<strong>==g==\1==g==\2==g==</strong>!' \
	| sed -E -e 's!<strong id="(b:[^"]+)">([^<]+)</strong>!<strong>==b==\1==b==\2==b==</strong>!' \
	| sed -E -e 's!<figure +id="(.+)"> *<img +src="(.+)"> *<figcaption>(.+)</figcaption> *</figure>!==f==\1==\2==\3==!' \
	| sed -E -e 's/<!-- +== +(.+) +-->/==c==\1==/' \
	| sed -E -e 's!(<div.+class="language-([^ ]+))!==l==\2==\1!' \
	| ${PANDOC} --wrap=preserve -f html -t latex -o - \
	| tail -n +6 \
	| sed -E -e '/==l==.+==/{N;N;s/\n/ /g;}' \
	| sed -E -e 's!==l==(css)== *\\begin\{verbatim\}!\\begin{lstlisting}!' \
	| sed -E -e 's!==l==(text)== *\\begin\{verbatim\}!\\begin{lstlisting}[backgroundcolor=\\color{verylightgray}]!' \
	| sed -E -e 's!==l==([^=]+)== *\\begin\{verbatim\}!\\begin{lstlisting}[language=\1]!' \
	| sed -E -e 's!\\begin{verbatim}!\\begin{lstlisting}!' \
	| sed -E -e 's!\\end{verbatim}!\\end{lstlisting}!' \
	| sed -E -e '/==c==.+==/{N;s/\n/ /;}' -e 's!==c==(.+)==!\1!' -e s'!\\textbackslash{}!\\!' \
	| sed -E -e 's!==f==([^=]+)==([^=]+)==([^=]+)==!\\begin{figure}[H]\\label{\1}\\centering\\includegraphics{\2}\\caption{\3}\\end{figure}!' \
	| sed -E -e 's!\.svg}!\.pdf}!' \
	| sed -E -e 's!==b==([^=]+)==b==([^=]+)==b==!\\hypertarget{\1}{\2}\\label{\1}!' \
	| sed -E -e 's!==g==([^=]+)==g==([^=]+)==g==!\\hypertarget{\1}{\2}\\label{\1}!' \
	| ${PYTHON} tools/cites.py \
	| sed -E -e 's!\\begin{quote}!\\begin{quote}\\setlength{\\parindent}{0pt}!' \
	| sed -E -e 's!\\section!\\chapter!' \
	| sed -E -e 's!\\subsection!\\section!' \
	| sed -E -e 's!\\subsubsection!\\subsection!' \
	> ${ALL_TEX}

# Create all the HTML pages once the Markdown files are up to date.
${PAGES_HTML} : ${PAGES_MD}
	${JEKYLL} build

# Create the bibliography Markdown file from the BibTeX file.
${BIB_MD} : ${BIB_TEX}
	tools/bib2md.py ${lang} < ${DIR_TEX}/${STEM}.bib > ${DIR_MD}/bib.md

## ----------------------------------------

## check       : check everything.
check :
	@make lang=${lang} checkcites
	@make lang=${lang} checkfigs
	@make lang=${lang} checkgloss
	@make lang=${lang} checklinks
	@make lang=${lang} checksrc
	@make lang=${lang} checktoc

## checkcites  : list all missing or unused bibliography entries.
checkcites : ${BIB_MD}
	@tools/checkcites.py ${DIR_MD}/bib.md ${PAGES_MD}

## checkfigs   : list all missing or unused figures.
checkfigs :
	@tools/checkfigs.py figures ${PAGES_MD}

## checkgloss  : check that all glossary entries are defined and used.
checkgloss :
	@tools/checkgloss.py ${PAGES_MD}

## checklinks  : check that all links are defined and used.
checklinks :
	@tools/checklinks.py _config.yml _includes/links.md ${PAGES_MD} _includes/contributing.md

## checksrc    : check source file inclusion references.
checksrc :
	@tools/checksrc.py src ${PAGES_MD}

## checktoc    : check consistency of tables of contents.
checktoc :
	@tools/checktoc.py _config.yml ${PAGES_MD}

## ----------------------------------------

## spelling    : compare words against saved list.
spelling :
	@cat ${PAGES_MD} | tools/uncode.py | aspell list | sort | uniq | comm -2 -3 - .words

## undone      : which files have not yet been done?
undone :
	@grep -l 'undone: true' _en/*.md

## words       : count words in finished files.
words :
	@wc -w $$(fgrep -L 'undone: true' _en/*.md) | sort -n -r

## ----------------------------------------

## clean       : clean up junk files.
clean :
	@rm -r -f _site dist tools/__pycache__
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
