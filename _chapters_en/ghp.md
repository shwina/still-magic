---
permalink: "/en/ghp/"
title: "Using GitHub Pages"
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

-   All options for publishing data science in the early 21st Century are clumsy and contradictory
    -   Just as all classroom instruction compromises the efficacy of individual tutoring in the name of economics,
        all publishing options compromise the flexibility of pen on paper in the name of readability and efficiency
-   [WYSIWYG](#g:wysiwyg) tools like [Microsoft Word][ms-word], [LibreOffice][libreoffice], and [Google Docs][google-docs]
    -   Lower cognitive load because you can see what your readers will see
    -   *Can* allow restyling, but most people don't take advantage of those features (extra work up front for downstream payoff)
    -   Hard to automatically regenerate (although again it's possible, just not taken advantage of)
    -   Hard to coordinate the work of multiple contributors because version control systems don't support their formats
-   [Typesetting languages](#g:typesetting-language) like [Markdown][markdown], HTML, and [LaTeX][latex] use plain text plus instructions
    -   Much higher cognitive load because of the compilation step
    -   Much easier to restyle because of the compilation step
    -   Much easier to automatically regenerate (provided the thing you want to regenerate fits the format)
    -   Better suited to large-scale collaboration because plain text is the one format that programmers respect
-   Many attempts to compromise by offering WYSIWYG view of typesetting language, e.g., [Authorea][authorea], [Overleaf][overleaf], and a gazillion different in-browser Markdown editors, including those built into the [Jupyter Notebook][jupyter]
    -   These work until authors try to use any features of the substrate that aren't supported by the WYSIWYG view
    -   Or author things in the substrate in ways that the overlay doesn't recognize
-   We will explore Markdown and GitHub Pages
    -   Illustrates the key ideas of a compilation-based workflow
    -   Probably the least painful to set up

## Exercises

FIXME

## Markdown {#s:ghp-markdown}

-   Created as a simple way to write simple HTML
    -   Support the same kinds of formatting (bold, italics, headings, etc.)
    -   But save people from all the angle brackets
    -   And allow embedded HTML for things the "standard" doesn't support
-   Turns out that:
    -   Everybody wants something more (tables! citations!)
    -   Using an arbitrary collection of syntax rules for simple things makes more complicated things hard to do
-   We will focus on [GitHub Flavored Markdown][gfm] (GFM)
-   Use asterisks (or underscores) for `*italics*` and `**bold**` (which render as *italics* and **bold**)
    -   I prefer to mix them to do `*__bold italics__*` because I can't tell three marks from two
-   Use one to six `#` signs at the start of a line to create a heading

```
# Level-1
## Level-2
### Level-3
```

-   Unnumbered lists are written using dashes or asterisks as markers
    -   Conventional to indent text and nested lists by four columns for readability

```
-   First top item
    -   First nested item
    -   Second nested
        item with text
        spanning multiple lines
-   Second top item
    *   Use asterisks instead of dashes
```

-   Numbered lists are written with numbers
    -   Usually number everything with `1.` and let the processor figure it out

```
1.  First top item
1.  Second top item
    1.  You can use
    2.  the actual numbers
    3.  if you want
1.  Third top item
```

-   Code can be written inline using back quotes:

```
Compile `rnadiff` using `Make`.
```

-   Use three back quotes or tildes at the start and end of a code block:

    ```
    this is
    a
    code block
    ```

-   Can also indent code blocks by four spaces
    -   Which is helpful when you're trying to show how back quotes work
-   Write links as `[text](URL)`

```
Please see [our website](http://example.com) for more information.
```

-   Better style to use a symbolic name in the text `[like this][website]`
-   Then put a definition for the link name at the bottom of the file

```
[website]: http://example.com
```

-   This ensures that all uses are consistent
-   Images are where things start to get squirrelly
    -   No obvious syntax, so use link syntax with an exclamation mark at the start

```
![image title](URL)
```

-   And then there are tables
    -   Draw them in ASCII

```
| Common Name | Scientific Name       |
|-------------|-----------------------|
| groath      | Hebecephalus montanus |
| grobbit     | Ungulamys cerviforme  |
| gurrath     | Oncherpestes fodrhami |
```

-   Columns don't have to line up, but it's easier to read if you do
    -   So you'll spend far more time than you should using a supercomputer to indent with spaces
-   Or use something like the [Tables Generator][tables-generator]
    -   Yes, you are using a WYSIWYG program to create 1970s-era text to be translated back into what you drew
-   This is the point where it's often simpler to just write HTML

## Exercises

FIXME

## GitHub Pages {#s:ghp-ghp}

-   Most people don't want to read Markdown as-is, so need some way to translate and publish it
-   GitHub provides a mechanism called [GitHub Pages][github-pages]
-   Several ways to use it, the simplest of which is:
    1.  Go to the `master` branch of your repository
    1.  Create a top-level subdirectory in your project called `docs`
    1.  Go to the settings for your project on GitHub and turn on publishing
-   GitHub Pages uses a tool called [Jekyll][jekyll] to translate Markdown and other files for publication
    -   Simple things are simple
    -   Complex things are complex, and should be avoided in favor of self-publishing (discussed below)
-   By default, Jekyll copies all of the files in `docs` to create the website for the project
    -   If the project is hosted at `https://github.com/USER/PROJECT`, the website is `https://USER.github.io/PROJECT`
    -   Note: `github.io`, not `github.com`
-   Files and directories whose names begin with `_` aren't copied
    -   Jekyll will generate the site into a directory called `_site`
    -   So add that to your `.gitignore`
-   Text files (including Markdown and HTML) are copied as-is...
-   ...unless they start with two triple-dash lines:

```
---
---

The manifold perplexities of my chosen research topic...
```

-   Any file with this header is processed - in particular, Markdown is turned into HTML

## Exercises

FIXME

## Metadata and Templating {#s:ghp-metadata}

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

-   First line specifies the [page template](#g:page-template) to use
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

-   There are *lots* of [themes](#g:theme) for Jekyll
    -   Use one of GitHub's defaults unless you know a lot about graphic design and want to spend hours fiddling with CSS

## Exercises

FIXME

## Previewing Locally {#s:ghp-preview}

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
-   Use a Jekyll [filter](#g:jekyll-filter)
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

## Exercises

FIXME

## Self-Publishing {#s:ghp-self-pub}

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

## Exercises

FIXME

## Math {#s:ghp-math}

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
-   Note: this is loading MathJax from a [content delivery network]{#g:cdn}
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

## Exercises

FIXME

## Summary {#s:ghp-summary}

FIXME: create concept map

{% include links.md %}
