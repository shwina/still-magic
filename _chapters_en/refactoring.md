---
permalink: "/en/refactoring/"
title: "Refactoring"
questions:
-   "How can I go about reorganizing code when I'm making changes?"
objectives:
-   "Describe four common refactorings and correctly apply each."
keypoints:
-   "Reorganizing code in consistent ways makes errors less likely."
-   "Common refactorings include replacing a value with a name, replacing a repeated test with a flag, extracting a function, and combining functions."
---

FIXME: introduction

-   [Refactoring](#g:refactor) is changing the structure of code without changing what it does
    -   Like refactoring an equation
-   Most discussions of refactoring focus on [object-oriented programming](#g:oop)
-   But many patterns can and should be used to clean up [procedural](#g:procedural-programming) code
-   An example of [design patterns](#g:design-patterns)

## Replace Value With Name {#s:refactoring-replace-value-with-name}

-   I.e., define a constant

```
# BEFORE
seconds_elapsed = num_days * 24 * 60 * 60
```

```
# AFTER
seconds_elapsed = num_days * SECONDS_PER_DAY
```

-   Easier to understand when read aloud (which is always a good test)
-   Easier to change
    -   You don't think you'll have to, but then people want to use your software on Mars ([Mak2006](#CITE))

### Exercises

FIXME: exercises

## Replace Repeated Test With Flag {#s:refactoring-repeated-test}

-   Similar to the above
-   Remember that Booleans are values and can be assigned

```
# BEFORE
def process_data(data, scaling):
    if len(data) > THRESHOLD:
        scaling = sqrt(scaling)
    ...process data to create score...
    if len(data) > THRESHOLD:
        score = score ** 2
```

```
# AFTER
def process_data(data, scaling):
    is_large_data = len(data) > THRESHOLD
    if is_large_data:
        scaling = sqrt(scaling)
    ...process data to create score...
    if is_large_data:
        score = score ** 2
```

-   Less risk of the tests falling out of sync
-   Clear to reader that the tests are the same
-   Purpose of test is clearer

### Exercises

FIXME: exercises

## Extract Function {#s:refactoring-extract-function}

-   Move common operations into functions to reduce volume of code
-   Move complex operations into functions to reduce cognitive load

```
# BEFORE
def check_neighbors(grid, point):
    if (0 < point.x) and (point.x < grid.width) and \
       (0 < point.y) and (point.y < grid.height):
        ...look at all four neighbors
```

```
# AFTER
def check_neighbors(grid, point):
    if in_interior(grid, point):
        ...look at all four neighbors...

def in_interior(grid, point):
    ...four tests as above...
```

-   Function might be usable in other contexts
-   But even if not, easier to read aloud (which is a good test of comprehensibility)
-   Use original variable names as parameter names during refactoring to reduce typing

### Exercises

FIXME: exercises

## Combine Functions {#s:refactoring-combine-functions}

-   Opposite of Extract Function
-   If operations always done together, more efficient to combine
-   And *possibly* easier to understand

```
# BEFORE
def count_vowels(text):
    num = 0
    for char in text:
        if char in VOWELS:
            num += 1
    return num

def count_consonants(text):
    num = 0
    for char in text:
        if char in CONSONANTS:
            num += 1
    return num
```

```
# AFTER
def count_vowels_and_consonants(text):
    num_vowels = 0
    num_consonants = 0
    for char in text:
        if char in VOWELS:
            num_vowels += 1
        elif char in CONSONANTS:
            num_consonants += 1
    return num_vowels, num_consonants
```

-   Generally done for performance reasons
-   Can make code harder to re-use
    -   For example, assumes that a character is either a vowel or a consonant
    -   Not true of all languages
-   Or people use it and throw some results away

### Exercises

FIXME: exercises

## Create Lookup Table {#s:refactoring-lookup}

```
# BEFORE
def count_vowels_and_consonants(text):
    ...as above...
```

```
# AFTER

IS_VOWEL = {'a' : 1, 'b' : 0, 'c' : 0, ... }
IS_CONSONANT = {'a' : 0, 'b' : 1, 'c' : 1, ... }

def count_vowels_and_consonants(text):
    num_vowels = num_consonants = 0
    for char in text:
        num_vowels += IS_VOWEL[char]
        num_consonants += IS_CONSONANT[char]
    return num_vowels, num_consonants
```

-   Easier to understand and maintain than complicated conditionals
-   [Declarative programming](#g:declarative-programming)

-   Many language features exist to give programmers something to refactor *to*
    -   See a pattern in many contexts
    -   Provide syntactic support for it
    -   Explain in terms of original

### Exercises

FIXME: exercises

## Replace Loop With Comprehension {#s:refactoring-comprehension}

-   This is the purpose of comprehensions

```
# BEFORE
result = []
for num in values:
    result.append(num * num)
```

```
# AFTER
result = [num * num for num in values]
```

-   Easier to read *for simple calculations*
-   Becomes more complicated to understand with conditionals

```
# BEFORE
result = []
for num in values:
    if num > 0:
        result.append(num * num)
    else:
        result.append(0)
```

```
# AFTER
result = [num * num if num > 0 else 0 for num in values]
```

-   The `else` is necessary so that there's a result for each input
-   Cross-product loops are straightforward

```
# BEFORE
result = []
for left in 'ABC':
    for right in 'xyz':
        result.append(left + right)
```

```
# AFTER
result = [left + right for left in 'ABC' for right in 'xyz']
```

-   What's hard to remember is the equivalent of nested loops where the inner loop depends on the outer
    -   Order in expression feels inverted

```
words = ['first', 'second', 'third']
flattened = [c for w in words for c in w]
```

-   Works for sets, dictionaries, and anything else that can be iterated over
-   This is the direction most modern Python is going, so refactor whenever you can
-   And don't be afraid (at least during development) to create temporaries

```
# BEFORE
for record in data:
    result = []
    score = calculate_score(record)
    if score > THRESHOLD:
        score = THRESHOLD
    result.append(record.ID, score)
```

```
# AFTER
raw = [(d.id, calculate_score(d)) for d in data]
trimmed = [(d.id, THRESHOLD) if d.s > THRESHOLD else (d.id, d.s) for d in raw]
```

### Exercises

FIXME: exercises

## Summary {#s:refactoring-summary}

-   Provide Default and Encapsulate Control Flow: forward reference to [s:reuse](#CHAPTER)

FIXME: create concept map

{% include links.md %}
