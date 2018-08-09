---
permalink: "/en/style/"
title: "Programming Style"
questions:
-   "How should I name my variables and functions?"
-   "How should I organize my code so that other people can understand it?"
-   "What kind of documentation should I write and where should I put it?"
-   "What kinds of variables should I create so that my code is easier to understand?"
-   "How can I go about reorganizing code when I'm making changes?"
objectives:
-   "Explain why consistent formatting of code is important."
-   "Describe standard Python formatting rules and identify cases where code does or doesn't conform to them."
-   "Explain what docstrings are and add correctly-formatted docstrings to short Python programs."
-   "Extract and format documentation from docstrings using `pydoc`."
-   "Describe four common roles for variables and correctly identify instances of each."
-   "Explain why using variables in stereotyped ways aids comprehension."
-   "Describe four common refactorings and correctly apply each."
keypoints:
-   "The brain thinks every difference is significant, so removing unnecessary differences in formatting reduces cognitive load."
-   "Python software should always conform to the formatting the rules in PEP 8."
-   "Documentation strings (docstrings) can be placed at the start of a file or at the start of a function."
-   "Docstrings can be formatted using a superset of Markdown."
-   "Tools like `pydoc` and Sphinx can extract and format docstrings to create documentation for software."
-   "Using variables in consistent ways reduces cognitive load."
-   "Common roles for variables include constant, stepper, most-recent holder, most-wanted holder, gatherer, and flag."
-   "Reorganizing code in consistent ways makes errors less likely."
-   "Common refactorings include replacing a value with a name, replacing a repeated test with a flag, extracting a function, and combining functions."
---

> Nothing in software engineering makes sense except in the light of human psychology.
>
> --- Greg Wilson (after [[Dobz1973](#CITE)])

-   Text with *meaningless* **differences** takes longer to read than text without
    because our brains think every difference might be significant
-   Being consistent therefore reduces [cognitive load](#g:cognitive-load),
    which in turn helps us work faster and make fewer errors
-   This lesson explores four kinds of consistency:
    -   How to format program text
    -   What documentation to create and where to put it
    -   How to create and use variables in predictable ways
    -   How to reorganize code systematically when the time comes to make changes
-   Always remember [Orwell's Sixth Rule][orwells-rules]:
    "Break any of these rules sooner than saying anything outright barbarous."

## Standard Python Style {#s:style-pep8}

-   Python has a standard style called [PEP 8][pep-8]
-   And a tool called `pep8` that checks code and reports violations
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
-   However, short variable names for temporaries and loop variables are OK [[Beni2017](#CITE)]
-   Order within file should be:
    -   Docstring
    -   Imports
    -   Constants
    -   Functions (highest level first)
    -   `if __name__ == '__main__'`
-   A few other rules (some borrowed from [Jenny Bryan][bryan-jenny]'s "[Code Smells and Feels][code-smells-and-feels]")
    -   Do not comment and uncomment sections of code to change behavior
    -   Keep functions short (no more than a page or three levels of control flow)
    -   Put early exits or decisions at the top of the function ([guard clause](#g:guard-clause))
    -   Prefer `if` to `else`

## Embedded Documentation {#s:style-docstrings}

-   Some people argue that if you need to add comments to your software, you should have written clearer software
-   But software is only "self-explanatory" if you understand intention and design constraints,
    neither of which usually show up in the software itself
    -   "Why does the software do this?"
    -   "Why doesn't it do this in a simpler way?"
-   A more reasonable guideline is therefore "if you need to document something in the middle of a function, put it in a separate function"
-   And then document:
    -   The overall purpose of the code in that file
    -   The purpose of each function in the file
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

{% include style/trim.html %}

-   Can use a more sophisticated tool (i.e., more powerful but also more complicated) called [Sphinx][sphinx]
    -   Reads a superset of Markdown called [reStructredText](#g:restructured-text)
    -   Generates cross-indexed documentation that is more nicely formatted
-   Used by [ReadTheDocs][readthedocs]
    -   Extracts and formats documentation from GitHub repositories (and other places)
    -   Automatically regenerates documentation every time there's a change
    -   An example of [continuous integration](#g:continuous-integration)
    -   And it's free
    -   But out of the scope of this lesson

## Roles of Variables {#s:style-roles}

-   [Chunking](#g:chunking) refers to our brain's innate tendency to group things together and remember them as a unit
    -   Chord progressions in music
    -   The murder/background investigation/false suspect/revelation/capture/confession pattern in British murder mysteries
-   Using variables in consistent ways allows us to create and use chunks when reading programs
-   [Design patterns](#g:design-patterns) serve this purpose for larger object-oriented programs
-   The [Roles of Variables][roles-variables] is intended for smaller, non-object programs [[Saja2006](#CITE)]
    -   Names for things you're probably already doing
    -   Makes it easier to communicate
    -   And if you consciously stick to these patterns, others will find your code easier to read as well
-   fixed value: not changed after it is first defined
    -   Some languages allow explicit definition of constants
    -   But sometimes a fixed value's actual value isn't known until the program runs (e.g., output directory)
-   stepper: goes through a succession of values in a predictable way
    -   E.g., the loop variable in a `for` loop or the current time in a simulation that advances hour by hour
-   most-recent holder: the value most recently seen
    -   A stepper is a common special case of this
    -   Most-recent holder's value isn't predictable, e.g., the last URL visited
-   most-wanted holder: the "best" value seen so far
    -   E.g., the largest value seen so far in a list, or the record with the highest score
-   gatherer: often called an accumulator or aggregator, it collects values seen so far in some way
    -   Sum of all values seen to date
    -   List of all positive scores seen to date
-   follower: the value before the current one
    -   E.g., the last-but-one value when calculating the Fibonacci sequence
-   one-way flag: changes value once and only once if a condition is seen
    -   E.g., have any negative values been included in this sum?
-   temporary: holds a value long enough to be used in some calculation and is then discarded
    -   E.g., temporary value for three-way swap
    -   Or intermediate values in large numerical expression
-   organizer: a temporary used to organize some set of values
    -   E.g., a list that exists just long enough to sort values
-   container: used to hold values so that they can be processed together
    -   An organizer is a temporary container

FIXME: include examples of these

## Refactoring {#s:style-refactor}

-   [Refactoring](#g:refactor) is changing the structure of code without changing what it does
    -   Like refactoring an equation
-   Most discussions of refactoring focus on [object-oriented programming](#g:oop)
-   But many patterns can and should be used to clean up [procedural](#g:procedural-programming) code
-   Replace Value With Name
    -   FIXME: example
-   Replace Repeated Test With Flag
    -   FIXME: example
-   Extract Function
    -   FIXME: example
-   Combine Functions
    -   FIXME: example
-   Create Lookup Table
    -   FIXME: example
-   Provide Default
    -   FIXME: forward reference to [s:reuse](#CHAPTER)
-   Encapsulate Control Flow
    -   FIXME: forward reference to [s:reuse](#CHAPTER)

{% include links.md %}
