---
permalink: "/en/docs/"
title: "Documenting Code"
undone: true
questions:
-   "What kind of documentation should I write and where should I put it?"
objectives:
-   "Explain what docstrings are and add correctly-formatted docstrings to short Python programs."
-   "Extract and format documentation from docstrings using `pydoc`."
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

A more reasonable guideline is therefore,
"If you need to document something in the middle of a function, put it in a separate function."
Once you've done that,
explain the overall purpose of the code in that file,
how each function in the file helps achieve that goal,
and anything else that would puzzle your younger self.

## Where should I put documentation for my code? {#s:docs-docstrings}

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

## Summary {#s:docs-summary}

FIXME: create concept maps for documentation

{% include links.md %}
