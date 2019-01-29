# Still Magic

> It's still magic even if you know how it's done.
>
> -- Terry Pratchett

[![Build Status](https://travis-ci.org/merely-useful/still-magic.svg?branch=master)](https://travis-ci.org/merely-useful/still-magic)

---

## Overall Design

-   Markdown source files for each human language are in a [collection][jekyll-collections] named after the language.
    -   E.g., `_en` for English.

-   Use underscores rather than dashes in filenames, e.g., `a_b.md`.
    -   Need underscores for Python source files that are being loaded.
    -   Might as well be consistent.

-   Every file has a unique slug.  Using the English version as an example:
    -   Entry in Jekyll configuration's table of contents is `slug`.
    -   File's name is `_en/slug.md`.
    -   File's auto-generated slug is `slug`.
    -   Generated HTML is `_site/en/slug/index.html`.
    -   Chapter ID is `s:slug` and section IDs are `s:slug-something`.
    -   Figure IDs are `f:slug-something`.
    -   Source for all diagrams for the file are in `./figures/slug.xml` (a [draw.io][draw-io] drawing).
    -   PNG, SVG, and PDF versions of diagrams are in `./figures/slug_something.suffix`.

-   Every Markdown file's YAML must contain one field:
    -   `title`: the file's title.

-   Lessons must also contain:
    -   `questions`: a point-form list of motivating questions (lessons only).
    -   `objectives`: a point-form list of learning objectives (lessons only).
    -   `keypoints`: a point-form list of key points for a cheat sheet (lessons only).

-   The `index.md` file for each language (e.g., `_en/index.md`) must also contain:
    -   `root: true` to control formatting properly.
    -   `permalink: "/en/"` (or whatever the language is) to override the default output path defined in `_config.yml`.

-   Goal was to use pure Jekyll to create HTML for GitHub Pages without pre-processing and committing generated files.
    -   Came close but failed.
    -   Need to regenerate table of contents in `./_data/toc.json` with a compilation step because Jekyll won't extract and list headings within files.
    -   Then use `{% raw %}{% include x key="s:whatever" %}{% endraw %}` to reference by key (where `x` stands for "cross-reference").
    -   Since we have to do that, we use `{% raw %}{% include g key="g:whatever" text="term" %}{% endraw %}` for glossary references
        and `{% raw %}{% include b key="b:first,b:second" %}{% endraw %}` for bibliographic citations.

-   Some inclusions loop over the table of contents to match slugs to files because Jekyll doesn't support lookup by key in collections.

-   Use the JavaScript in `./js/site.js` to patch up classes for tables and create table of contents for each page.

-   All-in-one HTML version generated dynamically by JavaScript so as not to require pre-commit compilation.
    -   `all/lang.html` is a placeholder that goes into `_site/lang/all/index.html` (for each language `lang`).
    -   `./js/stitch.js` runs in this file, loads all the other files dynamically, and stitches them together.

-   Use Pandoc with pre- and post-processing to convert Markdown to LaTeX to build PDF.
    -   Most of the pre/post-processing uses `sed` directly in `Makefile`.
    -   Easier for newcomers to understand and maintain than a custom Pandoc template.

-   We use a script to regenerate the Markdown bibliography (e.g., `_en/bib.md`) from the BibTeX source (e.g., `tex/en/book.bib`).
    -   Yeah, this is also a server-side compilation step...

-   External links are `[text][link-name]`, where `link-name` is a key in `./_includes/links.md`
    -   `./_includes/links.md` is included explicitly at the bottom of every Markdown file because including it in the template doesn't work.

## Typography

-   If you would like to add code fragments,
    please put the source in `src/chapter/long-name.ext`.
    Include it in a left-justified, triple-backquoted code block:
    use `python` for Python, `r` for R, `shell` for shell commands, `html` for HTML,
    and `text` for output (including error output), YAML, and and other things.

-   If you want to leave out sections of code,
    use `# ...explanation...` (i.e., a comment with triple dots enclosing the text)
    in the Markdown file.

-   If you would like to add or fix a diagram, please:
    1.  Edit the XML file in `./figures/` corresponding to the chapter using [draw.io][draw-io].
    2.  Select the drawing and export as SVG with a 4-pixel boundary and transparency turned on,
        but *without* including the diagram source in the exported SVG.
    3.  Export a second time as PDF (selection only, cropped).
        We have tried automating the SVG-to-PDF conversion with various tools,
        but the results have been unsatisfying.
    4.  Edit the Markdown file and include an HTML `figure` element with an ID
        containing (in order) an `img` element with a `src` attribute but nothing else
        and a `figcaption` element with the figure's label.
        **These elements all have to be on one line**
        so that the `sed` magic in the Makefile that gets around Pandoc's handling of figures
        can find and translate the elements correctly.

-   If you need to embed a one-line LaTeX command in a Markdown file and have it passed through,
    format it as an HTML comment with a double equals sign and then the command.
    (We do not include one here because it will be interpreted literally,
    as this mechanism's implementation is rather crude).

-   When all else fails, put `<div markdown="1" replacement="something.tex">` in the Markdown file
    and a corresponding `</div>` after the block of Markdown that's to be replaced by
    the LaTeX inclusion.
    This can be used for complex tables,
    for displaying MathJax,
    and so on.

## Layout

-   `./README.md`: this file.
    -   Not processed by Jekyll.
-   `./CITATION.md`, `./CONDUCT.md`, `./LICENSE.md`: how to cite, code of conduct, and license respectively.
    -   Not processed by Jekyll.
    -   Redundant (information is also in `_en/filename.md`) but people expect to find these in the root directory.
-   `Makefile`: re-build everything.
    -   `make` prints a list of targets.
    -   Can regenerate HTML and PDF, check file consistency, count words, etc.
    -   Use `make lang=xx` to run commands for a particular human language (e.g., `make lang=en` to build the English version).
-   `_config.yml`: Jekyll configuration file.
    -   Simple values defined at the top (e.g., `title` and `subtitle`).
    -   `toc` is table of contents, and has three sub-keys:
        -   `lessons` for the main body.
        -   `bib` for the bibliography (single entry).
        -   `extras` for appendices.
        -    Each entry must match a file's slug.
    -   Read about [Jekyll collections][jekyll-collections] to understand the following:
        -   The use of `output: true` to force output.
        -   The use of `permalink: /:collection/:title/` to turn `_en/something.md` into `_site/en/something/index.html`.
        -   The use of `defaults` to specify the `lesson` layout for all the files in `_en`.
            -   Except `toc.json`, which uses `layout: none`.
-   `./_data/toc.json`: JSON-formatted table of contents data.
    -   FIXME: should be done by language.
-   `./_en/`: English-language collection of Markdown files.
-   `./_includes/`: inclusions
    -   `./_includes/b`, `./_includes/g`, and `./_includes/x` handle bibliographic citations, glossary entries, and cross-references respectively.
    -   `./_includes/contributing.md`: how to contribute (included in several places).
    -   `./_includes/disclaimer.html`: temporary disclaimer about files being under development.
    -   `./_includes/foot.html`: everything needed in the foot of the page.
    -   `./_includes/head.html`: everything needed in the head of the page that doesn't depend on configuration variables.
    -   `./_includes/links.md`: table of Markdown-formatted links.
    -   `./_includes/listblock.html`: displays a point-form list of lesson metadata (e.g., questions or key points).
    -   `./_includes/summary.html`: summarizes metadata from all lessons (e.g., creates a page of learning objectives).
    -   `./_includes/toc-bib.html`: display the bibliography in the table of contents.
    -   `./_includes/toc-section.html`: display lessons or extras in the table of contents.
    -   `./_includes/toc.html`: display the entire table of contents.
    -   `./_includes/lesson/file.ext`: an inclusion for `lesson`.
-   `./_layouts/`: page layouts.
    -   `./_layouts/default.html`: base layout (used directly only for the overall index page for the whole site).
    -   `./_layouts/lesson.html`: derived layout for all lesson pages.
-   `./_site/`: if present, holds the HTML pages generated by Jekyll.
-   `./all/`: holds the placeholder files used for the all-in-one versions of the site (per language).
    -   E.g., `./all/en.html` becomes `_site/en/all/index.html`.
    -   Placed here rather than in the language directory `_en` because it needs to be handled specially.
-   `./bin/`: scripts used to build and check the site.
    -   `./bin/bib2md.py`: convert BibTeX bibliography to Markdown.
    -   `./bin/check_chars.py`: check for non-7-bit characters in files.
    -   `./bin/check_cites.py`: check for unused and undefined bibliographic citations.
    -   `./bin/check_figs.py`: check for unused and missing figures.
    -   `./bin/check_gloss.py`: check for unused and undefined glossary entries.
    -   `./bin/check_links.py`: check for unused and undefined links in `./_includes/links.md`.
    -   `./bin/check_src.py`: check for unused and missing source files in `./src/`.
    -   `./bin/check_toc.py`: check for unused or missing files compared to table of contents in `./_config.yml`.
    -   `./bin/cites.py`: handle citations during Markdown-to-LaTeX transformation (because `sed` can't do this one step).
    -   `./bin/uncode.py`: remove code blocks (used in counting words).
    -   `./bin/util.py`: utilities used by other scripts.
-   `./css/`: CSS files
    -   `./css/bootstrap.min.css`: [Bootstrap 4][bootstrap]
    -   `./css/tango.css`: [Pygments Tango theme][pygments-tango]
    -   `./css/site.css`: custom definitions.
-   `./etc/`: holding area for files that aren't being used right now but might be (re-)added later.
-   `./favicon.ico`: toolbar icon.
-   `./figures/`: [draw.io][draw-io] source for figures and all exported figures.
    -   `./figures/lesson.xml`: source for all diagrams in that lesson.
    -   `./figures/lesson-something.suffix`: PDF, PNG, or SVG export of a single figure from the XML file.
-   `./img/`: miscellaneous images used in website (e.g., logo for license).
-   `./index.md`: overall home page for site (currently redirects to English-language version).
-   `./js/`: JavaScript files for site.
    -   `./js/all-in-one.js`: create all-in-one HTML version in the browser (uses `concatenate.js`).
    -   `./js/bootstrap.min.js`: [Bootstrap][bootstrap]
    -   `./js/concatenate.js`: utilities used to create all-in-one version of site.
    -   `./js/site.js`: used to clean up bibliographic citations and glossary entries, style tables, etc.
    -   `./js/stitch.js`: command-line utility to combine all Markdown files into one (uses `concatenate.js`).
-   `./project/`: the running example used throughout the lessons.
    -   Put in a sub-directory so that it can be structured the way a real project would be.
-   `./requirements.txt`: Pip installation requirements.
    -   Run with `pip install -r requirements.txt`.
-   `./src/`: source files used in Markdown, broken down by chapter.
-   `./tex/`: LaTeX files used to create PDF.
    -   `./tex/settings.tex`: package inclusions, macro definitions, etc.
    -   `./tex/lang/book.tex`: main file for book.
    -   `./tex/lang/book.bib`: BibTeX bibliography for book.
    -   `./tex/lang/all.tex`: if present, holds the all-in-one LaTeX generated from the Markdown source.

[bootstrap]: https://getbootstrap.com/
[draw-io]: https://www.draw.io/
[jekyll-collections]: https://jekyllrb.com/docs/collections/
[pygments-tango]: https://jwarby.github.io/jekyll-pygments-themes/languages/javascript.html
