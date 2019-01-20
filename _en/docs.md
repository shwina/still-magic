---
title: "Programming Style"
undone: true
questions:
-   "What kind of documentation should I write and where should I put it?"
objectives:
-   "Explain what docstrings are and add correctly-formatted docstrings to short Python programs."
-   "Extract and format documentation from docstrings using `pydoc`."
-   "Explain why consistent formatting of code is important."
keypoints:
-   "Documentation strings (docstrings) can be placed at the start of a file or at the start of a function."
-   "Docstrings can be formatted using a superset of Markdown."
-   "Tools like `pydoc` and Sphinx can extract and format docstrings to create documentation for software."
---

An old proverb says, "Trust, but verify."
The equivalent in programming is, "Be clear, but document."
No matter how well software is written,
it always embodies decisions that aren't explicit in the final code
or accommodates complications that aren't going to be obvious to the next reader.
Putting it another way,
the best function names in the world aren't going to answer the questions
"Why does the software do this?"
and
"Why doesn't it do this in a simpler way?"
This lesson will explore who we should write documentation for,
what we should write for them,
and where it should go.

## What should I document for whom? {#s:style-what}

There are three kinds of people in any domain:
[novices](#g:novice), [competent practitioners](#g:competent-practitioner), and [experts](#g:expert) [Wils2018](#BIB).
A novice doesn't yet have a [mental model](#g:mental-model) of the domain;
they don't know what the key terms are,
how they relate,
what the causes of their problems are,
or how to tell whether a solution to their problem is appropriate or not.

Competent practitioners know enough to accomplish routine tasks with routine effort:
they may need to check [Stack Overflow(stack-overflow) every few minutes,
but they know what to search for and what "done" looks like.
Finally,
experts have such a deep and broad understanding of the domain
that they can solve routine problems at a glance
and are able to handle the one-in-a-thousand cases
that would baffle the merely competent.

Each of these three groups needs a different kind of documentation.
A novice needs a tutorial that introduces her to key ideas one by one
and shows how they fit together.
A competent practitioner needs reference guides, cookbooks, and Q&A sites;
these give her solutions close enough to what she needs
that she can tweak them the rest of the way.
Experts need this material as well---nobody's memory is perfect---but
they may also paradoxically want tutorials.
The difference between them and novices is that experts want tutorials on how things work
and why they were designed that way.

The first thing to decide when writing documentation
is therefore to decide which of these needs you are trying to meet.
Tutorials like this one should be long-form prose that contain code samples and diagrams.
They should use [authentic tasks](#g:authentic-task) to motivate ideas,
i.e.,
show people things they might actually want to do
rather than printing out prime numbers or having function `foo` call function `bar`.

Guided tours like this will help novices build a mental model,
but competent practitioners and experts will be frustrated by their slow pace and low information density.
They will want single-point solutions to specific problems like
how to find cells in a spreadsheet that contain a certain string
or how to configure the web server to load an access control module.
They can make use of an alphabetical list of the functions in a library,
but are much happier if they can search by keyword to find what they need;
one of the signs that someone is no longer a novice is that
they're able to compose useful queries and tell if the results are on the right track or not.

That observation brings us to the notion of a [false beginner](#g:false-beginner),
which is someone who appears not to know anything,
but who has enough prior experience in other domains
to be able to piece things together much more quickly than a genuine novice.
Someone who is proficient with MATLAB, for example,
will speed through a tutorial on Python's numerical libraries
much more quickly than someone who has never programmed before.

In an ideal world,
we would satisfy these needs with a [chorus of explanations][caulfield-chorus],
some long and detailed,
others short and to the point.
In our world, though,
time and resources are limited.
The rest of this section will therefore concentrate on
how to create a reference guide and an FAQ for a software package.
If you would like to know more about creating tutorials,
please see [Wils2018](#BIB).

## Where should I put documentation for my code? {#s:style-docstrings}

Instead of writing comments to document code,
Python encourages us to write [docstrings](#g:docstring)
(short for "documentation string").
A docstring is a string placed at the start of a file or function
but not assigned to a variable.
If it appears at the start of a file,
and the file is loaded using `import module`,
the string is made available as `module.__doc__` (with two underscores).
If it is placed at the start of a function called `func`,
the string becomes `func.__doc__`.
Python's built-in `help` function looks up this string,
formats it using the rules like [Markdown][markdown]'s,
and displays it,
so `help(module)` or `help(func)` displays something useful.

Docstrings are usually written in triple quotes so that they can span multiple lines,
and to make them stand out from strings that are being used as data.
For example,
here's a file `trim.py` that has a one-sentence docstring for the module as a whole
and a multi-line docstring for the function `trim`:

```python
'''
Tools for trimming values to lie in a specified range.
'''

def trim(values, low, high, in_place=False):
    '''
    Ensure that all values in the result list lie in low...high (inclusive).
    If 'in_place' is 'True', modifies the input instead of creating a new list.

    Args:
        values: List of values to be trimmed.
        low: Lower bound on values (inclusive).
        high: Upper bound on values (inclusive).
        in_place: If true, modify input list (default False).

    Returns:
        List of trimmed values (which may be the input list).

    Raises:
        AssertionError: if 'low' is greater than 'high'.
    '''
    assert low <= high, 'Nonsensical trim range {}..{}'.format(low, high)
    result = values if in_place else values[:]
    for (i, x) in enumerate(result):
        result[i] = min(high, max(low, x))
    return result
```
{: title="docs/trim.py"}

If we run the shell command:

```shell
pydoc bin/trim.py`
```

<!-- == \noindent -->
Python will read the Python file,
extract the docstrings,
and create a nicely-formatted listing:

```text
NAME
    trim - Tools for trimming values to lie in a specified range.

FUNCTIONS
    trim(values, low, high, in_place=False)
        Ensure that all values in the result list lie in low...high (inclusive).
        If 'in_place' is 'True', modifies the input instead of creating a new list.

        Args:
            values: List of values to be trimmed.
            low: Lower bound on values (inclusive).
            high: Upper bound on values (inclusive).
            in_place: If true, modify input list (default False).

        Returns:
            List of trimmed values (which may be the input list).

        Raises:
            AssertionError: if 'low' is greater than 'high'.

FILE
    /Users/standage/magic/bin/trim.py
```
{: title="docs/trim.txt"}

We get the same output from within the Python interpreter with:

```python
import trim
help(trim)
```

<!-- == \noindent -->
or we can run `pydoc -w bin/trim.py` to generate an HTML page
(with some rather garish coloring).

We can go further and use a more sophisticated (i.e., more powerful but also more complicated) tool called [Sphinx][sphinx].
It reads a superset of Markdown called [reStructredText](#g:restructured-text)
and generates. cross-indexed documentation that is more nicely formatted than `pydoc`'s default output.
Sphinx is used by by [ReadTheDocs][readthedocs],
which extracts and formats documentation from GitHub repositories and other places.
One benefit of ReadTheDocs is that it puts documentation in an easily-findable place;
the other is that it automatically regenerates that documentation every time there's a change to the repository
(an example of [continuous integration](#g:continuous-integration)).
It's a great service,
but it's out of the scope of this lesson.

## How Can I Create a Useful FAQ? {#s:docs-faq}

## What can my documentation tell me about the structure of my code? {#s:docs-infer}

FIXME

A more reasonable guideline is therefore,
"If you need to document something in the middle of a function, put it in a separate function."
Once you've done that,
explain the overall purpose of the code in that file,
how each function in the file helps achieve that goal,
and anything else that would puzzle your younger self.

## Summary {#s:docs-summary}

FIXME: create concept map for docs

## Exercises {#s:docs-exercises}

FIXME: create concept map for docs

{% include links.md %}
