---
title: "Programming Style"
undone: true
questions:
-   "How should I name my variables and functions?"
-   "How should I organize my code so that other people can understand it?"
objectives:
-   "Explain why consistent formatting of code is important."
-   "Describe standard Python formatting rules and identify cases where code does or doesn't conform to them."
-   "Write functions whose parameters have default values."
-   "Explain which parameters should have default values and how to select good ones."
-   "Write functions that can handle variable numbers of arguments."
-   "Explain what problems can most easily be solved by creating functions with variable numbers of arguments."
keypoints:
-   "The brain thinks every difference is significant, so removing unnecessary differences in formatting reduces cognitive load."
-   "Python software should always conform to the formatting the rules in PEP 8."
-   "Use `name=value` to define a default value for a function parameter."
-   "Use `*args` to define a catch-all parameter for functions taking a variable number of unnamed arguments."
-   "Use `**kwargs` to define a catch-all parameter for functions taking a variable number of named arguments."
---

-   Text with *meaningless* **differences** takes longer to read than text without
    because our brains think every difference might be significant
-   Being consistent therefore reduces [cognitive load](#g:cognitive-load),
    which in turn helps us work faster and make fewer errors

> Nothing in programming makes sense except in the light of human psychology.
>
> --- Greg Wilson (after [Dobz1973](#BIB))

-   This lesson explores two kinds of consistency:
    -   How to format program text
    -   How to reorganize code systematically when the time comes to make changes
-   Consistency helps with [chunking](#g:chunking)
-   Always remember [Orwell's Sixth Rule][orwells-rules]:
    "Break any of these rules sooner than saying anything outright barbarous."

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
    -   Docstring ([s:docs](#CHAPTER))
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
