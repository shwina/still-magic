---
permalink: "/en/publish/"
title: "Publishing"
questions:
-   FIXME
objectives:
-   FIXME
keypoints:
-   FIXME
---

-   It is not enough to be right: you must be heard

## Editing {#s:publish-editing}

-   Options in the early 21st Century are clumsy and contradictory
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
-   Many attempts to compromise by offering WYSIWYG view of typesetting language, e.g., [Authorea][authorea], [Overleaf][overleaf], and a gazillion different in-browser Markdown editors
    -   These work until authors try to use any features of the substrate that aren't supported by the WYSIWYG view
    -   Or author things in the substrate in ways that the overlay doesn't recognize
-   We will explore Markdown and GitHub Pages
    -   Illustrates the key ideas of a compilation-based workflow
    -   Probably the least painful to set up

## Markdown {#s:publish-markdown}

This part of the lesson will give an overview of the core Markdown syntax.
Before we begin, it is worth keeping in mind that there are a few different
markdowns around. [CommonMark][cm] is built to be a standard, and [GitHub
Flavored Markdown][gfm] (GFM) is so widely used that it could well be a standard
already. This lesson will present the syntax that is *common* to both (a very
large part of it is).

## Basic Syntax

Markdown easily allows to specify *italics*, **bold**, and ***bold italics***
(although not all "flavors" of Markdown agree on the last point). These styles
can be applied using either `*` or `_`, so that the following commands are all
equivalent:

```
*italics* and _italics_
**bold** and __bold__
***bold italics*** and ___bold italics___
```

Levels of sub-division in your text can be indicated by writing a single line
with between one and six hash marks. For example, the following document will
have two first-level headers (`Introduction` and `Methods`), and a second-level
header nested under `Methods`:

```
# Introduction
# Methods
## Model of population dynamics
```

Code can be written either inline by wrapping the text in backticks:

```
The program can be compiled using `Make`.
```

or with blocks by using a line with three backticks or three tildes (`~`)
to delimitate the code block:

~~~
```
this is
a
code block
```
~~~

On the first line of the block, it is common to specify the language.
Many tools that translate Markdown into HTML and other formats use this
to determine what rules to apply for syntax highlighting.

~~~
We write loops in `Python`:

``` python
for value in data:
    print(value)
```

to print these values.
```

Code can also be written by indenting four spaces, which is useful when you are
trying to show the use of triple back quotes or triple tildes.

There are two ways to write hyperlinks. The first is to write them inline
with the text in square brackets and the URL in parentheses:

```
Please see [our website](http://example.com) for more information.
```

The second is to use symbolic names for links by putting the second part
in square brackets:

```
Please see [our website][website] for more information.
```

and then putting a table of name-to-link translations at the bottom of the document:

```
[website]: http://example.com
```

FIXME: images

## Pandoc {#s:publish-pandoc}

Standard Markdown doesn't support equations, automatic section numbering, or
bibliographic citations.  Most dialects support tables, but in different ways
(and most of those are confusing to write and read for anything except very
simple two- or three-column tables).

[Pandoc][pandoc] does support all of these, but... FIXME

## GitHub Pages {#s:publish-github-pages}

FIXME: basic structure of GitHub Pages.

## Metadata and Templating {#s:publish-templating}

Markdown allows authors to indicate metadata in the document, in the form a
`YAML` header. `YAML` stands from Yet Another Markup Language, but this is
hardly important. A `YAML` header could look like:

```
---
title: "Modern Scientific Authoring Using Markdown"
author: "Meredith Slalom"
date: "2018-05-09"
---
...body of page...
```

These elements do not appear when the document is displayed, but are often
processed by publication tools.

FIXME: more on GitHub Pages and templates.

## What to Publish and Where {#s:publish-what-where}

-   What to publish
    -   Raw data
    -   Intermediate files that take a long time to generate
    -   Software versions
    -   Software command line flags
    -   Workflows and/or shell scripts
    -   R, Python, etc. scripts and notebooks for analysis and figures
-   Where to publish (same source)
    -   Big raw data - may not be yours in the first place, but needs professional archiving.
    -   Medium-size raw data (between 500 MB and 5 GB): Open Science Framework <osf.io>
    -   Small raw data (under 500 MB): GitHub and [Zenodo][zenodo]

## FAIR {#s:publish-fair}

FIXME
-   explain what FAIR is
-   [GO FAIR][go-fair]

### Findable

The first step in (re)using data is to find them.

-   (Meta)data are assigned a globally unique and persistent identifier
-   Data are described with rich metadata
-   Metadata clearly and explicitly include the identifier of the data they describe
-   (Meta)data are registered or indexed in a searchable resource

### Accessible

Once the user finds the required data, they need to know how can they be accessed, possibly including authentication and authorisation.

-   (Meta)data are retrievable by their identifier using a standardised communications protocol
    -   The protocol is open, free, and universally implementable
    -   The protocol allows for an authentication and authorisation procedure, where necessary
-   Metadata are accessible, even when the data are no longer available

### Interoperable

Data usually needs to be integrated with other data, which means that tools need to be able to process it.

-   (Meta)data use a formal, accessible, shared, and broadly applicable language for knowledge representation.
-   (Meta)data use vocabularies that follow FAIR principles
-   (Meta)data include qualified references to other (meta)data

### Reusable

The ultimate goal of FAIR is re-use.

-   Meta(data) are richly described with a plurality of accurate and relevant attributes
    -   (Meta)data are released with a clear and accessible data usage license
    -   (Meta)data are associated with detailed provenance
    -   (Meta)data meet domain-relevant community standards

{% include links.md %}
