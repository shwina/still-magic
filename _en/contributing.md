---
permalink: "/en/contributing/"
title: "Contributing"
---

{% include contributing.md %}

-   We use the term "slug" to refer to the short name of a chapter,
    e.g., `publish` for "Publishing".

-   The [Jekyll][jekyll] template used in this tutorial can support multiple languages.
    All English content should go in the `_en` directory.
    (Please note that we use Simplified English
    rather than Traditional English,
    i.e., American rather than British spelling and grammar.)
    We encourage translations;
    if you would like to take this on,
    please [email us][config-email].

-   If you wish to report errata or suggest improvements to wording,
    please include the chapter name in the first line of the body of your report
    (e.g., `Testing Data Analysis`).

-   If you would like to add code fragments,
    please put the source in `src/chapter/long-name.ext`.
    Include it in a triple-backquoted code block;
    use `py` for Python, `r` for R, `shell` for shell commands,
    and `text` for output (including error output).

-   If you want to leave out sections of code,
    use `# ...explanation...` (i.e., a comment with triple dots enclosing the text).

-   If you would like to add or fix a diagram, please:
    1.  Edit the XML file in `./files/` corresponding to the chapter using [draw.io][draw-io].
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

-   The naming conventions for labels are:
    -   `s:chapter-section` for section labels.
    -   `f:chapter-slug` for figure labels.
    -   `g:slug` for glossary references.
    -   `b:item` for bibliography references.

-   Use `[Name1900](#BIB)` to cite a bibliography entry,
    i.e., the key without the leading `b:` as the text of the link
    and `#BIB` as the link;
    the JavaScript in `js/site.js` will do the rest.
    If you want to cite multiple items at once,
    put them together like `[Name1900,Enam2000](#BIB)`.

-   Use `#g:key` as a URL when referring to a glossary item by key,
    and JavaScript will patch this up too.

-   If you need to embed a one-line LaTeX command in a Markdown file and have it passed through,
    format it as an HTML comment with a double equals sign and then the command.
    (We do not include one here because it will be interpreted literally,
    this mechanism being rather crude...)

{% include links.md %}
