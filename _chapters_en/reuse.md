---
permalink: "/en/reuse/"
title: "Creating Reusable Code"
questions:
-   FIXME
objectives:
-   FIXME
keypoints:
-   FIXME
---

-   The more code you re-use, the less code you have to write
-   Design code to be re-usable
-   [Refactor](#g:refactor) code as you use it based on what you learn as you go along
    -   Nobody gets it right the first time
    -   *How Buildings Learn* [[Bran1995](#CITE)]
-   Goal is to allow old code to use new code

## Default Parameter Values {#s:reuse-defaults}

FIXME
-   Give users control over everything *and* the ability to ignore details
-   Example: testing tolerance for image comparison
    -   How large a difference in color value to notice?
    -   How many differences above that threshold to tolerate (as percentage)?

```
def image_diff(left, right, per_pixel=0, fraction=0.01):
    ...implementation...
```

-   Default: "any difference counts" and "more than 1% of pixels differ"
    -   But can also be called as `image_diff(old, new, per_pixel=2)` to raise threshold per pixel
    -   Or `image_diff(old, new, fraction=0.05)` to allow more pixels to differ
    -   Or `image_diff(old, new, per_pixel=1, fraction=0.005)` to raise per-pixel threshold but decrease number of allowed differences
-   A subtle trap:

```
def collect(new_value, accumulator=set()):
    accumulator.add(new_value)
    return accumulator
```

-   All calls to `collect` will share the same `accumulator`
    -   Python executes code to define a function
    -   So `set()` is called once as the function is being defined
    -   And `accumulator` refers to *that* set

```
>>> collect('first')
{'first'}
>>> collect('second')
{'first', 'second'}
```

## Variable Numbers of Arguments {#s:reuse-varargs}

-   Often want functions to be able to accept variable number of arguments (like `print` and `max` do)
-   Can require user to stuff those arguments into a list, e.g., `find_limits([a, b, c, d])`
-   But Python can do this for us
-   Declare a single argument whose name starts with `*`, and Python will put all "extra" arguments into that tuple
    -   By convention, this argument is called `args`

```
def find_limits(*args):
    print(args)
```
```
>>> find_limits(1, 3, 5, 2, 4)
(1, 3, 5, 2, 4)
```

-   This comes after all explicit parameters to avoid ambiguity

```
def select_outside(low, high, *values):
    result = []
    for v in values:
        if (v < low) or (v > high):
            result.add(v)
    return result
```
```
>>> select_outside(0, 1.0, 0.3, -0.2, -0.5, 0.4, 1.7)
[-0.2, -0.5, 1.7]
```

-   Can use the reverse form

```
def trim_value(m, lower, upper):
    print(m, lower, upper)
```
```
>>> saved = ['matrix', 'low', 'high']
>>> trim_value(*saved)
matrix low high
```

-   Parallel forms exist for keyword arguments
    -   Prefix catch-all variable's name with `**`
    -   By convention, variable is called `kwargs`
    -   Catch-all is a dictionary instead of a tuple

```
def settings(user_id, **settings):
    print(user_id, settings)
```
```
>>> settings('jenny', country='CA', lang='R')
jenny {'lang': 'R', 'country': 'CA'}
```

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

{% include links.md %}
