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

FIXME: [Dobz1973](#BIB)

## What Are the Standard Rules of Good Style for Python Programs? {#s:style-pep8}

-   Python has a standard style called [PEP 8][pep-8]
-   And a tool called `pep8` that checks code and reports violations
    -   Tools of this kind are called [linters](#g:linter), after an early tool called `[lint][lint]`
    -   FIXME: PyLint
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
    -   Docstring ({% include ref key="s:style" %})
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

[Working memory](#g:working-memory) can only hold a few items at once:
initial estimates in the 1950s put the number at 7 plus or minus 2 [Mill1956](#BIB),
and more recent estimates put it as low as 4 or 5.
If your function requires two dozen parameters,
the odds are very good that users will frequently forget them
or put them in the wrong order.
One solution is to give parameters default values ({% include ref key="s:style" %});
another is to bundle them together so that (for example)
people pass three `point` objects instead of nine separate `x`, `y`, and `z` values.

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

## How and Why Can I Make It Easy to Chain Function Calls Together? {#s:style-chain}

FIXME: method chaining

Functions are easier to understand if they don't have any [side effects](#g:side-effect),
i.e.,
if they don't modify their inputs or any global variables.
But sometimes this is necessary:
a function might set a flag to control the logging level ({% include ref key="s:logging" %}),
update a database record,
or modify an image in place rather than make a copy for performance reasons.
In cases like these,
it's helpful if the function returns the object that was modified...

## Summary {#s:style-summary}

FIXME: create concept map for style.

FIXME: [Orwell's Rules][orwells-rules]

## Exercises {#s:style-exercises}

FIXME: create concept map for style.

{% include links.md %}
