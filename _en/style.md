---
title: "Programming Style"
questions:
-   "How should I name my variables and functions?"
-   "How should I organize my code so that other people can understand it?"
-   "How can I make functions more reusable?"
-   "What should my code do when an error occurs?"
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
-   "Use destructuring to unpack data structures as needed."
---

To paraphrase [Dobz1973](#BIB),
nothing in software development makes sense except in light of human psychology.
This is particularly true when we look at programming style.
Computers don't need to understand programs in order to execute them,
but people do in order to create them, maintain them, and fix them.
The more clearly those programs are laid out,
the easier it is to find things and make sense of them.
This lesson therefore describes some widely-used rules of Python programming style,
and some features of the language that you can use to make your programs more flexible and more readable.

## What are the standard rules of good style for Python programs? {#s:style-pep8}

The single most important rule of style is to be consistent,
both internally and with other programs.
Python's standard style is called [PEP 8][pep-8];
the term "PEP" is short for "Python Enhancement Proposal".
It also has a tool that used to be called `pep8`
and is now called `pycodestyle`
that checks source files against this style guide and reports violations.
Tools of this kind are called [linters](#g:linter),
after an early tool called `[lint][lint]` that found lint (or fluff) in C code.
Some of `pycodestyle`'s rules are listed below,
along with others borrowed from "[Code Smells and Feels][code-smells-and-feels]":

FIXME: add before-and-after examples for each of these.

### Always indent code blocks using 4 spaces, and use spaces instead of tabs.

### Do not put spaces inside parentheses

I.e., don't write <code>(&nbsp;1+2&nbsp;)</code>.
This applies to function calls as well:
do not write <code>max(&nbsp;a,&nbsp;b&nbsp;)</code>.

### Always use spaces around comparisons like `>` and `<=`.

Use your own judgment for spacing around common arithmetic operators like `+` and `/`.

### Use `ALL_CAPS_WITH_UNDERSCORES` for constants.

### Use `lower_case_with_underscores` for the names of functions and variables.

This naming convention is sometimes called [pothole case](#g:pothole-case).
You should only use [`CamelCase`](#g:camel-case) for classes,
which are outside the scope of this lesson.

### Put two blank links between each function definition.

This helps them stand out.

### Avoid abbreviations in function and variable names.

They can be ambiguous,
and can be be hard for non-native speakers to understand.
This rule doesn't necessarily you will have to do more typing:
a good programming editor will [auto-complete](#g:auto-completion) names for you.

### Use short names for short-lived local variables but longer names for things with wider scope.

Loop indices [Beni2017](#BIB) can be `i` and `j` (provided the loop is only a few lines long).
Anything that is used at a greater distance
or whose purpose isn't immediately clear
(such as a function) should have a longer name.

### Put everything in a file in order.

The order of items in each file should be:

-   The [shebang](#g:shebang) line (because it has to come first to work).
-   The file's documentation string ([s:style](#REF)).
-   All of the `import` statements, one per line.
-   Constant definitions.
-   Function definitions.
-   If the file can be run as a program,
    the `if __name__ == '__main__'` statement discussed in
    [s:package-import](#REF).

### Do not comment and uncomment sections of code to change behavior.

If you need to do something in some runs of the program and not do it in others,
use an `if` statement to enable or disable that block of code.
It's much more reliable---you're far less likely to accidentally comment out one too many lines---and
you may find that you want to leave those conditional sections in the finished program
for logging purposes ([s:logging](#REF)).

### Keep functions short.

Nothing should be more than a page long
or have more than three levels of indentation because of nested loops and conditionals.
Anything longer or more deeply nested will be hard for readers to fit into [working memory](#g:working-memory);
when you find yourself needing to break these limits,
extract a function ([s:refactor-extract-function](#REF)).

### Handle special cases at the start of the function.

This helps readers mentally get them out of the way
and focus on the "normal" case.
[s:refactor-short-circuits](#REF)
discusses this in more detail.

## In what order should functions be defined? {#s:style-order}

When encountering code for the first time,
most people scan it from top to bottom.
If that code is a program or script,
rather than a library,
its main function should be put first,
and should probably be called `main`.

After reading that function,
someone should have a good idea of what the program does in what order.
Three common patterns that people might match against are:

1.  Figure out what the user has asked it to do ([s:configure](#REF)).
2.  Read all input data.
3.  Process it.
4.  Write output.

<!-- == noindent -->
or:

1.  Figure out what the user has asked for.
2.  For each input file:
    1.  Read.
    2.  Process.
    3.  Write file-specific output (if any).
3.  Write summary output (if any).

<!-- == noindent -->
or:

1.  Figure out what the user has asked for.
2.  Repeatedly:
    1.  Wait for user input.
    2.  Do what the user has asked.
3.  Exit when a "stop" command of some sort is received.

Each step in each of the outlines above usually becomes a function.
Those functions depend on others,
some of which are written to break code into comprehensible chunks and are then called just once,
others of which are utilities that may be called many times from many different places.

FIXME: figure

Different people order these differently;
our preferred order is:

1.  Put all of the single-use functions in the first half of the file
    in the order in which they are likely to be called.
2.  Put all of the multi-use utility functions in the bottom of the file in alphabetical order.

If any of those utility functions are used by other scripts or programs,
they should go in a file of their own.
In fact,
this is a good practice even if they're only used by one program,
since it signals even more clearly which functions are in the "structural" layer
and which are in the "utility" layer.

## How can I specify default values for functions' parameters? {#s:style-defaults}

[Working memory](#g:working-memory) can only hold a few items at once:
initial estimates in the 1950s put the number at 7 plus or minus 2 [Mill1956](#BIB),
and more recent estimates put it as low as 4 or 5.
If your function requires two dozen parameters,
the odds are very good that users will frequently forget them
or put them in the wrong order.
One solution is to give parameters default values ([s:style](#REF));
another is to bundle them together so that (for example)
people pass three `point` objects instead of nine separate `x`, `y`, and `z` values.

A third approach (which can be combined with the preceding two)
is to specify default values for some of the parameters.
Doing this gives users control over everything
while also allowing them to ignore details;
it also codifies what you consider "normal" for the function.

For example,
suppose we are comparing images to see if they are the same or different.
We can specify two kinds of tolerance:
how large a difference in color value to notice,
and how many differences above that threshold to tolerate
(as a percentage of the total number of pixels).
By default,
any color difference is considered significant,
and only 1% of pixels are allowed to differ:

```python
def image_diff(left, right, per_pixel=0, fraction=0.01):
    # ...implementation...
```

<!-- == noindent -->
When this function is called using `image_diff(old, new)`,
those default values apply.
However,
it can also be called like this:

-   `image_diff(old, new, per_pixel=2)`
    allows pixels to differ slightly without those differences being significant.
-   `image_diff(old, new, fraction=0.05)` allows more pixels to differ.
-   `image_diff(old, new, per_pixel=1, fraction=0.005)`
    raises the per-pixel threshold but decrease number of allowed differences.

Default parameter values make code easier to understand and use,
but there is a subtle trap.
When Python executes a function definition like this:

```python
def collect(new_value, accumulator=set()):
    accumulator.add(new_value)
    return accumulator
```

<!-- == noindent -->
it calls `set()` to create a new empty set,
and then uses that set as the default value for `accumulator` every time the function is called.
It does *not* call `set()` anew for each call,
so all calls using the default will share the same set:

```python
>>> collect('first')
{'first'}
>>> collect('second')
{'first', 'second'}
```

A common way to avoid this is to pass `None` to the function
to signal that the user didn't provide a value:

```python
def collect(new_value, accumulator=None):
    if accumulator is None:
        accumulator = set()
    accumulator.add(new_value)
    return accumulator
```

## How can I write functions to handle a variable number of arguments? {#s:style-varargs}

We can often make programs simpler by writing functions that take a variable number of arguments,
just like `print` and `max`.
One way to to require user to stuff those arguments into a list,
e.g.,
to write `find_limits([a, b, c, d])`.
However,
Python can do this for us.
If we declare a single argument whose name starts with a single `*`,
Python will put all "extra" arguments into a [tuple](#g:tuple)
and pass that as the argument.
By convention,
this argument is called `args`:

```python
def find_limits(*args):
    print(args)

find_limits(1, 3, 5, 2, 4)
```
{: title="style/find_limits.py"}
```text
(1, 3, 5, 2, 4)
```

This catch-all parameter can be used with regular parameters,
but must come last in the parameter list to avoid ambiguity:

```python
def select_outside(low, high, *values):
    result = []
    for v in values:
        if (v < low) or (v > high):
            result.add(v)
    return result

print(select_outside(0, 1.0, 0.3, -0.2, -0.5, 0.4, 1.7))
```
{: title="style/select_outside.py"}
```text
[-0.2, -0.5, 1.7]
```

An equivalent special form exists for named arguments:
the catch-all variable is conventionally called `kwargs`
(for "keyword arguments")
and its name is prefixed with `**` (i.e., two asterisks instead of one).
When this is used,
the function is given a [dictionary](#g:dictionary) of names and values
rather than a list:

```python
def set_options(tag, **kwargs):
    result = '<{}'.format(tag)
    for key in kwargs:
        result += ' {}="{}"'.format(key, kwargs[key])
    result += '/>'
    return result

print(set_options('h1', color='blue'))
print(set_options('p', align='center', size='150%'))
```
```text
<h1 color="blue"/>
<p align="center" size="150%"/>
```
{: title="style/set_options.py"}

<!-- == noindent -->
Notice that the names of parameters are not quoted:
the call is `color='blue'` and not `'color'='blue'`.

## How can I pass an unknown number of parameters? {#s:style-starargs}

We can use the inverse of `*args` and `*kwargs` to match a list of values to arguments.
In this case,
we put the single `*` in front of the list when *calling* the function
rather than in front of the parameter when *defining* it:

```python
def trim_value(data, low, high):
    print(data, "with", low, "and", high)

parameters = ['some matrix', 'lower bound', 'upper bound']
trim_value(*parameters)
```
{: title="style/trim_value.py"}
```text
some matrix with lower bound and upper bound
```

## How can I get values out of structured data more easily? {#s:style-destructure}

Modern programming languages have lots of other tools to make life more convenient for programmers.
One that's particularly useful is [destructuring](#g:destructuring):

```python
[first, [second, third]] = [1, [2, 3]]
print(first)
print(second)
print(third)
```
{: title="style/destructuring.py"}
```text
1
2
3
```

As this example shows,
if the variables on the left are arranged in the same way as the values on the right,
Python will automatically unpack the values and assign them correctly.
This is particularly useful when looping over lists of structured values:

```python
people = [
    [['Kay', 'McNulty'], 'mcnulty@eniac.org'],
    [['Betty', 'Jennings'], 'jennings@eniac.org'],
    [['Marlyn', 'Wescoff'], 'mwescoff@eniac.org']
]
for [[first, last], email] in people:
    print('{} {} <{}>'.format(first, last, email))
```
{: title="style/looping.py"}
```text
Kay McNulty <mcnulty@eniac.org>
Betty Jennings <jennings@eniac.org>
Marlyn Wescoff <mwescoff@eniac.org>
```

## Summary {#s:style-summary}

George Orwell laid out [six rules for good writing][orwells-rules],
the last and most important of which is,
"Break any of these rules sooner than say anything outright barbarous."
There will always be cases where your code will be easier to understand
if you *don't* do the things described in this lesson,
but there are probably fewer of them than you think.

FIXME: create concept map for style.

## Exercises {#s:style-exercises}

FIXME: create exercises for style.

{% include links.md %}
