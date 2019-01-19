---
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

-   Design code to be comprehensible, but document
-   Some people argue that if you need to add comments to your software, you should have written clearer software
-   But software is only "self-explanatory" if you understand intention and design constraints,
    neither of which usually show up in the software itself
    -   "Why does the software do this?"
    -   "Why doesn't it do this in a simpler way?"
-   A more reasonable guideline is therefore "if you need to document something in the middle of a function, put it in a separate function"
-   And then document:
    -   The overall purpose of the code in that file
    -   The purpose of each function in the file

## How Can I Embed Documentation for My Code in the Code Itself? {#s:docs-docstrings}

-   Instead of using comments for this, use [docstrings](#g:docstring) (short for "documentation string")
    -   A string that is created at the start of a file or function, but not assigned to a variable
    -   Python automatically attaches this to the file (when it is loaded as a library) or to the function
    -   Available as `module.__doc__` or `function.__doc__`
-   The `help` function takes this string, formats it nicely using [Markdown][markdown] rules, and displays it
-   Typically format docstrings using triple quotes (so that they can span multiple lines)
-   Example: `trim.py`

```
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

-   Run `pydoc bin/trim.py` on the command line

```
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

-   Get the same output from within the Python interpreter:

```
import trim
help(trim)
```

-   Or run `pydoc -w bin/trim.py` to generate an HTML page `trim.html`
    -   Formatting is a bit garish

-   Can use a more sophisticated tool (i.e., more powerful but also more complicated) called [Sphinx][sphinx]
    -   Reads a superset of Markdown called [reStructredText](#g:restructured-text)
    -   Generates cross-indexed documentation that is more nicely formatted
-   Used by [ReadTheDocs][readthedocs]
    -   Extracts and formats documentation from GitHub repositories (and other places)
    -   Automatically regenerates documentation every time there's a change
    -   An example of [continuous integration](#g:continuous-integration)
    -   And it's free
    -   But out of the scope of this lesson

## Summary {#s:docs-summary}

FIXME: create concept maps for documentation

{% include links.md %}
