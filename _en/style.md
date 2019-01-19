---
permalink: "/en/style/"
title: "Programming Style"
undone: true
questions:
-   "What kind of documentation should I write and where should I put it?"
-   "How should I name my variables and functions?"
-   "How should I organize my code so that other people can understand it?"
objectives:
-   "Explain what docstrings are and add correctly-formatted docstrings to short Python programs."
-   "Extract and format documentation from docstrings using `pydoc`."
-   "Explain why consistent formatting of code is important."
-   "Describe standard Python formatting rules and identify cases where code does or doesn't conform to them."
-   "Write functions whose parameters have default values."
-   "Explain which parameters should have default values and how to select good ones."
-   "Write functions that can handle variable numbers of arguments."
-   "Explain what problems can most easily be solved by creating functions with variable numbers of arguments."
keypoints:
-   "Documentation strings (docstrings) can be placed at the start of a file or at the start of a function."
-   "Docstrings can be formatted using a superset of Markdown."
-   "Tools like `pydoc` and Sphinx can extract and format docstrings to create documentation for software."
-   "The brain thinks every difference is significant, so removing unnecessary differences in formatting reduces cognitive load."
-   "Python software should always conform to the formatting the rules in PEP 8."
-   "Use `name=value` to define a default value for a function parameter."
-   "Use `*args` to define a catch-all parameter for functions taking a variable number of unnamed arguments."
-   "Use `**kwargs` to define a catch-all parameter for functions taking a variable number of named arguments."
---

> Nothing in software development makes sense except in light of human psychology.
>
> -- Greg Wilson (with apologies to [Dobz1973](#BIB))

-   Text with *meaningless* **differences** takes longer to read than text without
    because our brains think every difference might be significant
-   Being consistent therefore reduces [cognitive load](#g:cognitive-load),
    which in turn helps us work faster and make fewer errors

-   Consistency helps with [chunking](#g:chunking)
-   Always remember [Orwell's Sixth Rule][orwells-rules]:
    "Break any of these rules sooner than saying anything outright barbarous."

## What Should I Document? {#s:style-what}

FIXME

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

## What Are the Standard Rules of Good Style for Python Programs? {#s:style-pep8}

-   Python has a standard style called [PEP 8][pep-8]
-   And a tool called `pep8` that checks code and reports violations
    -   Tools of this kind are called [linters](#g:linter), after an early tool called `[lint][lint]`
-   Indent 4 spaces, and always use spaces instead of tabs
-   Do *not* put spaces inside parentheses, i.e., don't use `( 1+2 )`
    -   This applies to function calls as well
-   Always use spaces around comparisons, but use your own judgment for common arithmetic operators
-   Use `ALL_CAPS_WITH_UNDERSCORES` for constants (which should be placed at the top of the file)
-   Use `lower_case_with_underscores` for function and variable names
    -   Only use `CamelCase` for types and classes, which are outside the scope of this lesson
-   Use two blank links between each function
-   Avoid abbreviations (which can be hard for non-native speakers to understand)
    -   A good programming editor will auto-complete names, so you don't have to do much typing
-   However, short variable names for temporaries and loop variables are OK [Beni2017](#BIB)
-   Order within file should be:
    -   Docstring ([s:style](#CHAPTER))
    -   Imports
    -   Constants
    -   Functions (highest level first)
    -   `if __name__ == '__main__'`
-   A few other rules (some borrowed from [Jenny Bryan][bryan-jenny]'s "[Code Smells and Feels][code-smells-and-feels]")
    -   Do not comment and uncomment sections of code to change behavior
    -   Keep functions short (no more than a page or three levels of control flow)
    -   Put early exits or decisions at the top of the function ([guard clause](#g:guard-clause))
    -   Prefer `if` to `else`

## How Can I Specify Default Values for My Functions' Parameters? {#s:style-defaults}

-   Give users control over everything *and* the ability to ignore details
-   Example: testing tolerance for image comparison
    -   How large a difference in color value to notice?
    -   How many differences above that threshold to tolerate (as percentage)?

```python
def image_diff(left, right, per_pixel=0, fraction=0.01):
    ...implementation...
```

-   Default: "any difference counts" and "more than 1% of pixels differ"
    -   But can also be called as `image_diff(old, new, per_pixel=2)` to raise threshold per pixel
    -   Or `image_diff(old, new, fraction=0.05)` to allow more pixels to differ
    -   Or `image_diff(old, new, per_pixel=1, fraction=0.005)` to raise per-pixel threshold but decrease number of allowed differences
-   A subtle trap:

```python
def collect(new_value, accumulator=set()):
    accumulator.add(new_value)
    return accumulator
```

-   All calls to `collect` will share the same `accumulator`
    -   Python executes code to define a function
    -   So `set()` is called once as the function is being defined
    -   And `accumulator` refers to *that* set

```python
>>> collect('first')
{'first'}
>>> collect('second')
{'first', 'second'}
```

## How Can I Write Functions to Handle a Variable Number of Arguments? {#s:style-varargs}

-   Often want functions to be able to accept variable number of arguments (like `print` and `max` do)
-   Can require user to stuff those arguments into a list, e.g., `find_limits([a, b, c, d])`
-   But Python can do this for us
-   Declare a single argument whose name starts with `*`, and Python will put all "extra" arguments into that tuple
    -   By convention, this argument is called `args`

```python
def find_limits(*args):
    print(args)
```
```python
>>> find_limits(1, 3, 5, 2, 4)
(1, 3, 5, 2, 4)
```

-   This comes after all explicit parameters to avoid ambiguity

```python
def select_outside(low, high, *values):
    result = []
    for v in values:
        if (v < low) or (v > high):
            result.add(v)
    return result
```
```python
>>> select_outside(0, 1.0, 0.3, -0.2, -0.5, 0.4, 1.7)
[-0.2, -0.5, 1.7]
```

-   Can use the reverse form

```python
def trim_value(m, lower, upper):
    print(m, lower, upper)
```
```python
>>> saved = ['matrix', 'low', 'high']
>>> trim_value(*saved)
matrix low high
```

-   Parallel forms exist for keyword arguments
    -   Prefix catch-all variable's name with `**`
    -   By convention, variable is called `kwargs`
    -   Catch-all is a dictionary instead of a tuple

```python
def settings(user_id, **settings):
    print(user_id, settings)
```
```python
>>> settings('jenny', country='CA', lang='R')
jenny {'lang': 'R', 'country': 'CA'}
```

## Summary {#s:style-summary}

FIXME: create concept map for style

{% include links.md %}
