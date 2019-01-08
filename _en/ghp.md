---
permalink: "/en/ghp/"
title: "Using GitHub Pages"
undone: true
questions:
-   "How can I create a static website for my work?"
objectives:
-   "Explain the strengths and shortcomings of today's publishing options for research reports."
-   "Format pages using Markdown."
-   "Publish pages online using GitHub Pages."
-   "Use metadata headers, templates, and configuration files to eliminate redundancy in GitHub Pages."
-   "Preview GitHub Pages sites locally."
-   "Publish sites on GitHub Pages by generating documentation locally and committing it to the repository."
-   "Configure and use MathJax to add mathematics to web pages."
keypoints:
-   "WYSIWYG editors make simple things simple, but complex things hard, and are not well suited to large-scale collaboration."
-   "Typesetting pipelines are more complex to use, but scale well and are easier to integrate into reproducible research pipelines."
-   "Markdown is a family of throwback text formats that provides a subset of the formatting available in HTML."
-   "GitHub can be configured to use Jekyll to publish files located in the `docs` directory of a repository's `master` branch as a website."
-   "Jekyll can be controlled using YAML metadata in page headers, configuration data in `_config.yml`, and page templates in `_layouts`."
-   "Instead of using Jekyll, pages can be generated locally and committed to the repository's `docs` directory."
-   "Math can be added to pages using MathJax and LaTeX equation syntax."
---

All options for publishing technical work in the early 21st Century are clumsy and contradictory.
[WYSIWYG](../gloss/#g:wysiwyg) tools like [Microsoft Word][ms-word],
[LibreOffice][libreoffice],
and [Google Docs][google-docs] lower [cognitive load](../gloss/#g:cognitive-load)
because you can see what your readers will see as you're writing.
They *can* allow restyling if authors are careful to apply named styles
instead of just changing the font and making something bold,
but most people don't to this
because it's extra work up front for an uncertain downstream payoff.
It's had to automatically regenerate reports as data chages
(although again it's possible, just not taken advantage of),
and most importantly,
it's hard to coordinate the work of multiple contributors
because version control systems don't support these formats.
There's no reason they couldn't,
but programmers are pretty heavily invested in plain text,
and unfortunately tend to consider everything else beneath them.

[Typesetting languages](../gloss/#g:typesetting-language) like [Markdown][markdown],
HTML,
and [LaTeX][latex] require authors to type in the text they want
plus instructions on how to format it.
The compilation from source to rendered view has a cognitive cost,
but typesetting languages are better suited to large-scale collaboration
because the source for every document is plain text
and can therefore be managed by today's version control systems.
Compilation also makes documents easier to restyle:
simply change the definition of what a level-2 heading is supposed to look like,
push the button,
and bingo---there's your document.
Of course,
the last sentence of section 3 is now sitting on a page of its own,
and the tables have all moved around,
and...

Some modern systems attempt to compromise
by offering WYSIWYG view of typesetting language:
[Overleaf][overleaf] uses LaTeX as its storage format,
and many different in-browser editors
(including those built into the [Jupyter Notebook][jupyter])
will render Markdown in real time.
These work until authors try to use any features of the underlying layer
that aren't supported by the WYSIWYG view.

In this section we will explore one of the simplest widely-used typesetting-style systems:
Markdown and GitHub Pages.
The combination illustrates the key ideas of a compilation-based workflow,
and while its simplicity means that there are things it can't do (or can't do easily),
it also means that less can go wrong.

## How can I write HTML without writing HTML? {#s:ghp-markdown}

A [static website](../gloss/#g:static-website) is one that consists solely of pages:
no forms, no interactivity, just information to read.
To create such a site,
we ust write HTML,
but some people find that typing `<p>` to start a paragraph
and `</p>` to end one is too much work.

[Markdown][markdown] was created as a simpler way to write the equivalent of HTML.
It supports many of the same kinds of formatting,
such as bold, italics, headings, and links,
but doesn't require tags in angle brackets.
It also allows authors to write HTML for things the "standard" doesn't support.

The word "standard" is in quotes because it turned out that
everyone wanted a little bit more than what was originally included in Markdown.
Tables, for example:
lots of people wanted tables.
And footnotes,
and images,
and on and on until eventually Markdwon became just as complex as HTML
but much less regular,
once again proving that using an arbitrary collection of syntax rules for simple things
makes complicated things harder to do.

We will focus on [GitHub Flavored Markdown][gfm],
which is the variation of Markdown used to create websites on GitHub.
Paragraphs are separated by blank lines,
and it uses asterisks or underscores for `*italics*` and `**bold**`,
which render as *italics* and **bold**.
(I prefer to mix them to do `*__bold italics__*` because I can't tell three marks from two.)

We can use one to six `#` signs at the start of a line to create headings of various levels:

```
# Level-1
## Level-2
### Level-3
```

Unnumbered lists are written using dashes or asterisks as markers;
it's conventional to indent points and nested lists by four columns for readability,
but not strictly required.

```
-   First top item
    -   First nested item
    -   Second nested
        item with text
        spanning multiple lines
-   Second top item
    *   Use asterisks instead of dashes
```

Numbered lists are written `1.`, `2.`, and so on instead of dashes or asterisks.
We usually number everything with `1.`
and let the Markdown processor figure out what the actual numbers should be.

```
1.  First top item
1.  Second top item
    1.  You can use
    2.  the actual numbers
    3.  if you want
1.  Third top item
```

Code can be written inline using back quotes:

```
Compile `rnadiff` using `Make`.
```

<!-- == \noindent -->
or we can use three back quotes or tildes at the start and end of a code block:

    ```
    this is
    a
    code block
    ```

Alternatively,
we can indent code blocks by four spaces,
which is helpful when we're trying to show how back quotes work
(as we just did).

There are three ways to write links.
The first puts the displayed text in square brackets and the URL in parentheses:

```
Please see [our website](http://example.com) for more information.
```

It's generally considered better style to use a symbolic name for the link in the text
in square brackets, `[like this][website]`,
and then put a definition for the link name at the bottom of the file:

```
[website]: http://example.com
```

This ensures that all uses are consistent.
Finally, we can display the link itself by putting it in angle brackets like:
`<http://example.org>`.

Images are where things start to get squirrelly.
There is no obvious syntax,
so Markdown uses link syntax with an exclamation mark at the start:

```
![image title](URL)
```

And then there are tables.
In a throwback to the 1970s,
Markdown requires us to draw them using horizontal and vertical bars:

```
| Common Name | Scientific Name       |
|-------------|-----------------------|
| groath      | Hebecephalus montanus |
| grobbit     | Ungulamys cerviforme  |
| gurrath     | Oncherpestes fodrhami |
```

The columns don't have to line up,
but the table source easier to read if we do,
which means we'll spend far more time than we should using a supercomputer to indent with spaces.
Alternatively,
we can use something like the [Tables Generator][tables-generator]
to create the layout we need.
And if you want to merge rows or columns,
it's much simpler simply to write HTML.

## How can I publish web pages using GitHub? {#s:ghp-ghp}

Most people don't want to read Markdown as-is,
so we need some way to translate and publish it.
GitHub provides a mechanism called [GitHub Pages][github-pages].
There are several ways to use it,
the simplest of which is:

1.  Go to the `master` branch of your repository.
1.  Create a top-level subdirectory in your project called `docs`.
1.  Go to the settings for your project on GitHub and turn on publishing for that directory.

GitHub Pages uses a tool called [Jekyll][jekyll] to translate Markdown and other files for publication.
Simple things are simple to do in Jekyll;
complex things are complex,
and should be avoided in favor of self-publishing (discussed [below](#s:ghp-self-pub)).

By default,
Jekyll copies all of the files in the `docs` directory to create the website for the project.
If the project is hosted at <code>https://github.com/<em>user</em>/<em>project</em></code>,
its website is <code>https://<em>user</em>.github.io/<em>project</em></code>.
(Note that the domain is `github.io`, not `github.com`.)

Files and directories whose names begin with a single underscore `_` aren't copied,
but are instead used for configuration and customization,
which are described below.

## How Can I Give My Pages a Consistent Look and Feel? {#s:ghp-metadata}

Text files (including Markdown and HTML) are copied as-is,
unless they start with two triple-dash lines:

```
---
---

The manifold perplexities of my chosen research topic...
```

-   Any file with this header is processed - in particular, Markdown is turned into HTML

-   The triple-dash header can contain metadata telling Jekyll how to format the document
-   Work through this example

```
---
layout: simple
title: "Adagu's Home Page"
author: "Adagu Okereke"
---

The manifold perplexities of my chosen research topic...
```

-   First line specifies the [page template](../gloss/#g:page-template) to use
-   Create a sub-directory called `_layouts`
-   Create an HTML file with everything common to all pages
-   Use `{% raw %}{{content}}{% endraw %}` to show where the content of the page is to go
-   Jekyll will fill it in

```
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta charset="utf-8" />
  </head>
  <body bgcolor="LightYellow">
{% raw %}{{content}}{% endraw %}
  </body>
</html>
```

-   Jekyll will copy values from the header into the page where `{% raw %}{{page.key}}{% endraw %}` appears

```
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta charset="utf-8" />
    <meta name="author" content="{% raw %}{{page.author}}{% endraw %}" />
  </head>
  <body bgcolor="LightYellow">
  <h1>{% raw %}{{page.title}}{% endraw %}</h1>
{% raw %}{{content}}{% endraw %}
  </body>
</html>
```

```
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta charset="utf-8" />
    <meta name="author" content="Adagu Okereke" />
  </head>
  <body bgcolor="LightYellow">
  <h1>Adagu's Home Page</h1>
<p>The manifold perplexities of my chosen research topic...</p>
  </body>
</html>
```

-   Can (should) also put data in `_config.yml` in the `docs` directory
    -   Uses a format called [YAML][yaml] for names with values and lists
-   Values from the configuration file are used in pages as `{% raw %}{{site.key}}{% endraw %}`
    -   E.g., replace `{% raw %}{{page.author}}{% endraw %}` with `{% raw %}{{site.author}}{% endraw %}`
-   Other values control how Jekyll works
    -   E.g., list of names under the `exclude` key tells Jekyll to ignore files and directories
    -   This is completely independent from what's listed in `.gitignore`

```
author: "Adagu Okereke"
exclude:
- bin
- status.xlsx
- raw
- results
```

-   There are *lots* of [themes](../gloss/#g:theme) for Jekyll
    -   Use one of GitHub's defaults unless you know a lot about graphic design and want to spend hours fiddling with CSS

## How Can I Preview Pages Locally? {#s:ghp-preview}

-   Pushing half-finished work to the web for everyone to see is a bit unprofessional
-   To preview work locally:
    -   Install Jekyll
    -   Go into the `docs` directory
    -   Run `jekyll serve` (can't do it from the root because that's a GitHub thing)
-   Point your browser at <https://localhost:4000>
    -   `localhost` means "this machine"
    -   `:4000` means port 4000 (instead of the usual ports used by web servers)
-   If there are missing files, you'll see an error message in the terminal window when you try to access them
-   Have to be careful about paths to files
    -   The home page of your project is `/index.html` when you're running locally
    -   But `https://USER.github.io/PROJECT/index.html` when you're running on GitHub
    -   Which means the path below the domain is `/PROJECT/index.html`
    -   So you cannot use something like `/images/profile.png` as an image URL,
        because that won't resolve
-   Use relative URLs wherever you can
    -   E.g., `../images/profile.png`
-   But what about your templates?
    -   Want to use the same template for pages at all levels
-   Use a Jekyll [filter](../gloss/#g:jekyll-filter)
    -   Double curly brackets to trigger evalution by Jekyll
    -   The absolute path for the link
    -   A pipe symbol
    -   The `relative_url` function name

```
<img src="{% raw %}{{'/images/profile.png' | relative_url}}{% endraw %}" />
```

-   or:

```
![My Profile Picture]({% raw %}{{'/images/profile.png' | relative_url}}{% endraw %})
```

-   There are lots of other filters, like `absolute_url`

## How Can I Publish Pages Myself Instead of Relying on GitHub? {#s:ghp-self-pub}

-   Jekyll is very limited for research publishing
    -   Doesn't number sections or translate section cross-references
    -   Doesn't handle bibliographic citations
-   The solution is to use something else
    -   Store source in a directory other than `docs` in your `master` branch
    -   Generate the files you want using whatever tool you want and put them in `docs`
    -   Make sure they *don't* have triple-dash YAML headers so that Jekyll doesn't try to translate them a second time
    -   Commit and push
    -   This means you're storing generated files in your repository, which is generally bad practice
    -   But you do what you have to do...
-   [Pandoc][pandoc] is a widely-used format-to-format conversion tool
    -   Turn HTML into Word into Markdown into LaTeX into...
    -   Uses its own superset of Markdown, but can be told to conform to GFM
    -   Handles bibliographic citations and other things that GFM doesn't
-   [R Markdown][r-markdown] and [Jupyter][jupyter] can both generate static websites that you can commit to `docs`
-   Run `jekyll serve` in the `docs` folder to preview

## How Can I Include Math in Web Pages? {#s:ghp-math}

-   LaTeX is widely used for typesetting math
-   [MathJax][mathjax] is a JavaScript library that parses LaTeX and renders it in the browser
-   Steps are:
    1.  Tell the browser to load the JavaScript library when it loads your page
    2.  Mark the sections of your page that MathJax is to translate
-   Loading the library:

```
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML" async></script>
  </head>
  <body>
  ...the body of your page...
  </body>
</html>
```

-   Break it down
    -   Use the `script` tag inside the `head` of a page to tell the browser to load JavaScript
    -   The `src` attribute tells the browser what to load
    -   Everything after the `?` is configuration for MathJax
    -   The word `async` means "don't hold up loading, but run the script as soon as it's available"
    -   Things like this are why we use page templates...
-   Note: this is loading MathJax from a [content delivery network](../gloss/#g:cdn)
    -   Means the math won't render if you are offline
    -   You can install MathJax locally, but that's out of the scope of this lesson
-   Now mark the inline LaTeX in the body of your page with `$$...$$` markers
    -   Works in both Markdown and HTML

```
The circle is defined by $$x^2 + y^2 = \mu$$.
```

-   Produces "The circle is defined by $$x^2 + y^2 = \mu$$."
-   Use double dollar signs on lines of their own to generate block equations

```
$$ r = \sqrt{\frac {N} {N+1}} \sqrt{\frac {N+1} {2N}} = \sqrt{\frac{1}{2}} $$
```

-   Output is:

$$ r = \sqrt{\frac {N} {N+1}} \sqrt{\frac {N+1} {2N}} = \sqrt{\frac{1}{2}} $$

## Summary {#s:ghp-summary}

FIXME: create concept map for GitHub Pages

{% include links.md %}
