---
permalink: "/en/reuse/"
title: "Creating Re-usable Code"
questions:
-   "How can I write software that I'll be able to re-use in the future?"
-   "What kind of documentation should I write and where should I put it?"
objectives:
-   "Explain what docstrings are and add correctly-formatted docstrings to short Python programs."
-   "Extract and format documentation from docstrings using `pydoc`."
-   "Explain what happens when a new function is defined."
-   "Create an alias for a function and explain what this does."
-   "Write programs that pass functions as arguments to other functions."
-   "Use higher-order functions to separate control flow from specific operations."
-   "Write programs that store functions in lists."
-   "Use generators and generator expressions to make complex operations appear simpler."
-   "Explain why too little or too much abstraction increases cognitive load, and why 'too little' and 'too much' are relative terms."
keypoints:
-   "Documentation strings (docstrings) can be placed at the start of a file or at the start of a function."
-   "Docstrings can be formatted using a superset of Markdown."
-   "Tools like `pydoc` and Sphinx can extract and format docstrings to create documentation for software."
-   "When a function is defined, Python translates the instructions into data and stores that data in memory."
-   "Variables can refer to functions just as they refer to lists, strings, and other values."
-   "References to functions can be stored in lists and other data structures."
-   "Functions can be passed as arguments to other functions just like other values."
-   "Higher-order functions are a way to abstract and re-use control flow."
-   "Every higher-order function implicitly defines a contract that must be respected by the functions passed to it."
-   "Define generators using the `yield` keyword to make complex calculations loopable."
-   "Use generator expressions instead of creating lists in order to make code more efficient."
-   "Too little abstraction increases cognitive load by requiring the reader to assemble meaning as they read."
-   "Too much abstraction increases cognitive load by requiring the reader to translate generalities into specifics as they read."
-   "'Too little' and 'too much' depend on the reader's level of expertise, which varies over time."
---

-   The more code you re-use, the less code you have to write
-   Design code to be re-usable
-   [Refactor](#g:refactor) code as you use it based on what you learn as you go along
    -   Nobody gets it right the first time
    -   *How Buildings Learn* [[Bran1995](#CITE)]
-   Goal is to allow old code to use new code

## Embedded Documentation {#s:reuse-docstrings}

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

{% include reuse/trim.html %}

-   Can use a more sophisticated tool (i.e., more powerful but also more complicated) called [Sphinx][sphinx]
    -   Reads a superset of Markdown called [reStructredText](#g:restructured-text)
    -   Generates cross-indexed documentation that is more nicely formatted
-   Used by [ReadTheDocs][readthedocs]
    -   Extracts and formats documentation from GitHub repositories (and other places)
    -   Automatically regenerates documentation every time there's a change
    -   An example of [continuous integration](#g:continuous-integration)
    -   And it's free
    -   But out of the scope of this lesson

### Exercises

FIXME: exercises

## Functions as Variables {#s:reuse-funcvar}

-   When you define a function, Python:
    -   Reads the text
    -   Translates it into instructions
    -   Stores those in a blob in memory
    -   Points a variable at that blob

```
def add_one(x):
    return x + 1
```

FIXME: image

-   Can assign that value (the instructions) to another variable just as you would a list

```
a1 = add_one
```
```
>>> a1(3)
4
```

FIXME: image

-   Use this to choose or replace functions dynamically

```
def normalize_huff(matrix):
    ...implementation...

def normalize_turk(matrix):
    ...implementation...

normalize = normalize_huff
if rescaling:
    normalize = normalize_turk

for m in matrices:
    resample(m)
    normalize(m)
    add_boundary_conditions(m)
```

-   In this case, it might make sense to put the conditional inside the loop
-   But:
    -   Easier to read and understand loop without the extra conditional
    -   If there are several loops or other uses, ensures the same normalizer being used everywhere

### Exercises

FIXME

## Creating Pipelines {#s:reuse-pipeline}

-   We can also put functions into lists
    -   More precisely, put references to functions into lists

```
def double(x):
    return x * 2

def add_one(x):
    return x + 1

def window(x):
    if x < 0: return 0
    if x > 100: return 100
    return x

operations = [double, add_one, window]
for original in [11, 90, 37]:
    current = original
    for op in operations:
        current = op(current)
    print('{} => {}'.format(original, current))
```
```
11 => 23
90 => 100
37 => 75
```

-   The first step toward building a configurable data analysis pipeline
-   Put the pipeline in a function of its own

```
def pipeline(operations, values):
    result = []
    for v in values:
        for op in operations:
            v = op(v)
        result.append(v)
    return result
```
```
>>> pipeline([window, add_one, double], [200, 100, 0])
[202, 202, 2]
>>> pipeline([add_one, double, window], [200, 100, 0])
[100, 100, 2]
```

-   Depends on all functions being called the same way
-   A [protocol](#g:protocol)
    -   One of the things [object-oriented programming](#g:oop) does is make protocols explicit

### Exercises

FIXME

## Functions as Arguments {#s:reuse-funcarg}

-   If we can pass functions to other functions in lists, surely we can pass them on their own

```
def do_twice(function, value):
    return function(function(value))
```
```
>>> do_twice(add_one, 1)
3
```

-   Separates [control flow](#g:control-flow) (e.g., the loop) from specific operations
-   A very common pattern in numerical computing, and one that you should use
-   Makes the control flow re-usable

### Exercises

FIXME

## Generators {#s:reuse-generator}

-   Using `yield` instead of `return` creates a [generator](#g:generator)
    -   Looks like a function
    -   But resumes execution from where it left off

```
def count_down(value):
    while value > 0:
        yield value
        value -= 1

c = count_down(3)
print(next(c))
print(next(c))
print(next(c))
print(next(c))
```
```
3
2
1
Traceback (most recent call last):
  File "foo.py", line 10, in <module>
    print(next(c))
StopIteration
```

-   Meant to be used in loops
    -   Don't require lots of memory
-   The basis of [generator expressions](#g:generator-expression)
    -   Use `(...)` instead of `[...]` (the latter actually creates the list in memory)
    -   Equivalent to defining an unnamed generator and then using it

```
g = (c.upper() for c in 'abc')
print(next(g))
print(next(g))
print(next(g))
print(next(g))
```
```
A
B
C
Traceback (most recent call last):
  File "foo.py", line 5, in <module>
    print(next(g))
StopIteration
```

-   Why would we do this?

```
def odd(values):
    for v in values:
        if (v % 2) == 1:
            yield v

def double(values):
    for v in values:
        yield v + v

def pair(values):
    previous = None
    for v in values:
        if previous is None:
            previous = v
        else:
            yield previous + v
            previous = None

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
for n in pair(double(odd(numbers))):
    print(n)

8
24
```

-   `pair` asks `double` for a value, then for another one
-   Each time, `double` asks `odd` for a value
-   `odd` produces the next odd value from the input list
-   No intermediate lists are created: the only memory cost is the call stack
-   And these are easy to re-use
    -   Though you have to be a bit careful about semantics

```
results = list(odd(pair(numbers)))
print(results)
[3, 7, 11, 15]

results = [odd(pair(numbers))]
print(results)
[<generator object odd at 0x10f3ab5c8>]
```

## Summary {#s:reuse-summary}

<figure>
  <figcaption>Reuse Concept Map</figcaption>
  <img id="f:reuse-concept" src="../../files/reuse.svg" alt="Reuse Concept Map" />
</figure>

### Exercises

FIXME

{% include links.md %}
