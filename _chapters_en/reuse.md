---
permalink: "/en/reuse/"
title: "Creating Re-usable Code"
questions:
-   "How can I write software that I'll be able to re-use in the future?"
objectives:
-   "Explain what happens when a new function is defined."
-   "Create an alias for a function and explain what this does."
-   "Write programs that pass functions as arguments to other functions."
-   "Use higher-order functions to separate control flow from specific operations."
-   "Write programs that store functions in lists."
-   "Use generators and generator expressions to make complex operations appear simpler."
keypoints:
-   "When a function is defined, Python translates the instructions into data and stores that data in memory."
-   "Variables can refer to functions just as they refer to lists, strings, and other values."
-   "References to functions can be stored in lists and other data structures."
-   "Functions can be passed as arguments to other functions just like other values."
-   "Higher-order functions are a way to abstract and re-use control flow."
-   "Every higher-order function implicitly defines a contract that must be respected by the functions passed to it."
-   "Define generators using the `yield` keyword to make complex calculations loopable."
-   "Use generator expressions instead of creating lists in order to make code more efficient."
---

-   The more code you re-use, the less code you have to write
-   Design code to be re-usable
-   Goal is to allow old code to use new code

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

{% include links.md %}
