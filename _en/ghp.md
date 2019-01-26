---
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

All options for publishing technical work in the early 21st Century are clumsy and contradictory.
[WYSIWYG](#g:wysiwyg) tools like [Microsoft Word][ms-word],
[LibreOffice][libreoffice],
and [Google Docs][google-docs] lower [cognitive load](#g:cognitive-load)
because you can see what your readers will see as you're writing.
They *can* allow restyling if authors are careful to apply named styles
instead of just changing the font and making something bold,
but most people don't to this
because it's extra work up front for an uncertain downstream payoff.
It's had to automatically regenerate reports as data changes
(although again it's possible, just not taken advantage of),
and most importantly,
it's hard to coordinate the work of multiple contributors
because version control systems don't support these formats.
There's no reason they couldn't,
but programmers are pretty heavily invested in plain text,
and unfortunately tend to consider everything else beneath them.

[Typesetting languages](#g:typesetting-language) like [Markdown][markdown],
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

A [static website](#g:static-website) is one that consists solely of pages:
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
and on and on until eventually Markdown became just as complex as HTML
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

It's generally considered better style to use a memorable name for the link
in square brackets in the text
and then define that link at the bottom of the file:

```
Create links [like this][website] to ensure consistency.

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

## How can I give my pages a consistent appearance? {#s:ghp-metadata}

When Jekyll processes source files,
it copies text files (including Markdown and HTML) as-is,
unless they start with two triple-dash lines:

```
---
---

The manifold perplexities of my chosen research topic...
```

Any file with this header is processed:
in particular, Markdown is turned into HTML,
which is what browsers know how to render.

The triple-dash header can contain [metadata](#g:metadata)
telling Jekyll how to format the document.
Here's a simple example:

```text
---
layout: simple
title: "Adagu's Home Page"
author: "Adagu Okereke"
---

The manifold perplexities of my chosen research topic...
```
{: title="ghp/adagu.md"}

First line specifies the [page template](#g:page-template) that Jekyll is to use.
This tells it what common HTML elements should be put in each page.
To create a template,
make a sub-directory called `_layouts`
and create an HTML file called `simple.html` with everything common to all pages.
`{% raw %}{{content}}{% endraw %}` to show where the content of the page is to go,
and Jekyll will fill it in:

```html
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
{: title="ghp/simple_01.html"}

As it processes the page,
Jekyll copies values from the header into the expanded text wherever `{% raw %}{{page.key}}{% endraw %}` appears,
where `key` is the name of one of the keys from the header.
For example,
suppose we add an `h1` element to our HTML template like this:

```html
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
{: title="ghp/simple_02.html"}

After Jekyll does its filling in,
the generated page will be:

```html
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
{: title="ghp/simple_02_generated.html"}

We can (and should) put data that's common to all pages
in a file called `_config.yml` in the top leve of the `docs` directory.
This is a YAML-formatted configuration file that controls how Jekyll operates;
values from this file are used in pages as `{% raw %}{{site.key}}{% endraw %}`.
For example,
if `_config.yml` contains this line:

```text
author: "Adagu Okereke"
```
{: title="ghp/config.yml"}

<!-- == \noindent -->
then every occurrence of `{% raw %}{{site.author}}{% endraw %}`
will be replaced with "Adagu Okereke" (without the quotation marks).

Other values in `_config.yml` control how Jekyll works.
One of the most common is the key `exclude`,
that introduces a list of things Jekyll is to ignore
and *not* copy into the site it builds:

```text
exclude:
- *.bak
- status.xlsx
```
{: title="ghp/config.yml"}

<!-- == \noindent -->
The `exclude` list is completely independent of what's listed in the repository's `.gitignore`
because there are things we probably *do* want saved (like the spreadsheet with the status of our experiments)
but *don't* want shared with the world.

There are *lots* of [themes](#g:theme) for Jekyll
that will set background colors, fonts, and page layouts:
use one of GitHub's defaults unless you know a lot about graphic design
and want to spend hours fiddling with [CSS](#g:css).

## How can I preview pages locally? {#s:ghp-preview}

Pushing half-finished work to the web for everyone to see is a bit unprofessional.
To preview your work locally,
you will have to:

1.  Install [Jekyll][jekyll].
2.  Go into the `docs` directory of your project.
3.  Run `jekyll serve` to build the site and run a little web server.
4.  Open `https://localhost:4000` in your browser.
    (`localhost` means "this machine",
    and `4000` means "port 4000".)

As you move around the preview of your site in the browser,
keep an eye on the shell window where you ran `jekyll serve`.
If you try to open a file that doesn't exist,
you'll see an error message.

## How can I publish pages myself instead of relying on GitHub? {#s:ghp-self-pub}

Jekyll is very limited for research publishing:
it doesn't number sections,
do cross-referencing,
or handle bibliographic citations.
If you need any of these,
the best approach is to use something other than Jekyll to build the site yourself
and then commit the generated files to version control.
A typical workflow is:

1.  Store source in a directory other than `docs` in the `master` branch of your repository.
2.  Generate the HTML pages you want using whatever tool you want and put them in the `docs` directory.
    (Make sure the generated files *don't* have triple-dash YAML headers
    so that Jekyll doesn't try to translate them a second time.)
3.  Commit the generated files to Git and push to your GitHub site.

<!-- == \noindent -->
This means you're storing generated files in your repository,
which is generally considered bad practice,
but we should always break rules rather than doing something awkward ([CHAPTER](../rules/)).

There are a *lot* of tools for generating static websites,
[Sphinx][sphinx] and [Hugo][hugo] being only two of the most popular.
[Pandoc][pandoc] is a widely-used general-purpose format-to-format conversion tool
that can turn HTML into Word into Markdown into LaTeX into many other things.
It uses its own superset of Markdown,
but can be told to conform to GitHub Flavored Markdown.
It also handles bibliographic citations and other things that GFM doesn't.
For research and data analysis,
though,
the best choices these days are [R Markdown][r-markdown] and [Jupyter][jupyter],
both of which can generate static websites that you can commit to `docs`.
It's very common to use a Makefile to automate this ([CHAPTER](../automate/)),
and have `make site` run `ipython nbconvert` or `knit` on any files that need to be updated.

## How can I include math in web pages? {#s:ghp-math}

Ironically,
while HTML was created by a scientist,
it has never been very good at displaying equations.
The best solution today is a tool called [MathJax][mathjax],
which is a JavaScript library that transforms expressions written in [LaTeX][latex]'s mathematical notation
into whatever the browser will support.
To use it,
we have to:

1.  Tell the browser to load the JavaScript library when it loads our page.
2.  Mark the sections of our page that MathJax is to translate.

To load the library,
we include a `script` tag in the `head` of our page.
The `src` attribute of the `script` tag tells the browser what to load;
everything after the `?` in the URL is configuration for MathJax.
(In this case, we're telling it exactly which style of notation we want to use.)
Finally,
the word `async` means "don't hold up loading, but run the script as soon as it's available";
see [this tutorial][js-vs-ds] if you really want to learn more.

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

<!-- == \noindent -->
One thing to note is that the sample HTML above is loading MathJax from a [content delivery network](#g:cdn),
which means that the math won't render if we are offline.
We can install MathJax locally,
but that's out of the scope of this lesson.

Our other task is to tell MathJax which parts of our page to translate.
To do this,
we mark the inline LaTeX in the body of our page with `$$...$$` markers
(i.e., with a double dollar sign at the start and end).
This works in both Markdown and HTML,
so that:

```
The circle is defined by $$x^2 + y^2 = \mu$$.
```

<div markdown="1" replacement="ghp/mathjax-1.tex">

<!-- == \noindent -->
produces "The circle is defined by $$x^2 + y^2 = \mu$$."
We can also use double dollar signs on lines of their own to generate block equations:

</div>

```
$$ r = \sqrt{\frac {N} {N+1}} \sqrt{\frac {N+1} {2N}} = \sqrt{\frac{1}{2}} $$
```

<!-- == \noindent -->
produces:

<div markdown="1" replacement="ghp/mathjax-2.tex">

$$
r = \sqrt{\frac {N} {N+1}} \sqrt{\frac {N+1} {2N}} = \sqrt{\frac{1}{2}}
$$

</div>

Here are just a few of the things MathJax can do:

<div markdown="1" replacement="ghp/mathjax-3.tex">

| Item        | Source                      | Rendered                  |
| ----------- | --------------------------- | ------------------------- |
| Symbol      | `$$\alpha$$`                | $$\alpha$$                |
| Superscript | `$$a^2$$`                   | $$a^2$$                   |
| Subscript   | `$$x_i$$`                   | $$x_i$$                   |
| Vector      | `$$\hat{x} < \vec{x}$$`     | $$\hat{x} < \vec{x}$$     |
| Fractions   | `$$\frac{x - y}{x + y}$$`   | $$\frac{x - y}{x + y}$$   |
| Roots       | `$$\sqrt[3]{x / y}$$`       | $$\sqrt[3]{x / y}$$       |
| Sums        | `$$\sum_{i=0}^\infty i^2$$` | $$\sum_{i=0}^\infty i^2$$ |
| Integrals   | `$$\int_{i=0}^\infty i^2$$` | $$\int_{i=0}^\infty i^2$$ |

</div>

## How can I avoid duplication in my pages? {#s:ghp-inclusions}

In order to enable MathJax in a page,
we need to include this line in the page's `head` element:

```
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML" async></script>
```

If all our pages use the same template,
it's easy enough to put this line in that template.
If we have several templates,
though---one for pages, one for blog posts, and one for papers---we
would have to duplicate the line in each.
Duplication always makes maintenance more difficult,
so Jekyll allows us to put commonly-used bits of text in separate files.
Even if a snippet of text is only used one place,
putting it in its own file can make the site's design easier to understand,
just as putting code in a function can make a program easier to read
even if that function is only called once.

To do this,
we create a directory called `_includes` (with a leading underscore)
and put the text we want to include in a file in that directory.
We then use {% raw %}{% include filename %}{% endraw %} to include it.
For example,
we can create a file called `_includes/footer.html` that contains this:

```html
<footer>
  <p>Copyright 2019 {{site.author}} | Made available under the Creative Commons - Attribution 4.0 License</p>
</footer>
```

<!-- == \noindent -->
and then include that in our template with:

```html
<html>
  {% raw %}{% include header.html %}{% endraw %}
  <body>
  {% raw %}{{content}}{% endraw %}
  {% raw %}{% include footer.html %}{% endraw %}
</html>
```

## How can I make paths to images and other files work everywhere? {#s:ghp-paths}

One thing you have to be careful about when building sites this way is the paths to files.
The home page of your project is `/index.html` when you're running locally,
but `https://USER.github.io/PROJECT/index.html` when you're running on GitHub,
i.e., the path below the domain is `/PROJECT/index.html`.
This means that you cannot use something like `/images/profile.png` as an image URL in a page,
because when you're running on GitHub Pages,
the actual path will be `/PROJECT/images/profile.png`.

The solution is to use [relative URLs](#g:relative-url)
instead of [absolute URLs](#g:absolute-url) where you can,
i.e., use `../images/profile.png`.
This is fine until you URLs in your templates and want to put pages at different levels of your directory hierarchy.
For example,
you may want to include the Creative Commons logo in the footer of every page,
one of which might be `index.html` and another `reports/quarterly.html`.
If you use `../images/creative-commons.png` in the template,
that will work in `reports/quarterly.html` but not in `index.html`;
if you use `./images/creative-commons.png` (with `.` instead of `..`),
it will work in `index.html` but not in pages that are one level down.

The solution is to use a Jekyll [filter](#g:jekyll-filter),
which is simply a small function that transforms the value you give it into some other value.
The syntax is shown below:

-   Double curly brackets to trigger evaluation by Jekyll.
-   The absolute path for the link (in quotes).
-   A pipe symbol (just as you would use in the shell).
-   The name of the filter function (in this case, `relative_url`).

```
<img src="{% raw %}{{'/images/profile.png' | relative_url}}{% endraw %}" />
```

<!-- == \noindent -->
As its name suggests,
`relative_url` takes an absolute path from the root of the project
and transforms it into a relative path from the page that's being generated.
There are lots of other filters:
`absolute_url` to create an absolute path to a file,
`date` to format dates in various ways,
and so on.

## Summary {#s:ghp-summary}

FIXME: create concept map for GitHub Pages

## Exercises {#s:ghp-exercises}

FIXME: exercises for GitHub Pages.

{% include links.md %}
