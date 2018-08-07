---
permalink: "/en/style/"
title: "Programming Style"
questions:
-   FIXME
objectives:
-   FIXME
keypoints:
-   FIXME
---

FIXME

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

FIXME
-   explain what docstrings are and how to write them
-   explain how to extract and format documentation

## Roles of Variables {#s:style-roles}

-   <http://www.cs.joensuu.fi/~saja/var_roles/role_intro.html>

## Refactoring {#s:style-refactor}

-   [Refactoring](#g:refactor) is changing the structure of code without changing what it does
    -   Like refactoring an equation
-   Most discussions of refactoring focus on [object-oriented programming](#g:oop)
-   But many patterns can and should be used to clean up [procedural](#g:procedural-programming) code
-   Replace Value With Name

FIXME: example

-   Replace Repeated Test With Flag

FIXME: example

-   Extract Function

FIXME: example

-   Combine Functions

FIXME: example

-   Encapsulate Control Flow

FIXME: example (shown above)

-   Combine Values

FIXME (depends on dictionaries)

{% include links.md %}
