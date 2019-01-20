---
title: "Refactoring"
undone: true
questions:
-   "How can I go about reorganizing code when I'm making changes?"
objectives:
-   "Describe at least four common refactorings and correctly apply each."
keypoints:
-   "Reorganizing code in consistent ways makes errors less likely."
-   "Replace a value with a name to make code more readable and to forestall typing errors."
-   "Replace a repeated test with a flag to ensure consistency."
-   "Turn small pieces of large functions into functions in their own right, even if they are only used once."
-   "Combine functions if they are always used together on the same inputs."
-   "Use lookup tables to make decision rules easier to follow."
-   "Use comprehensions instead of loops."
---

-   [Refactoring](#g:refactor) is changing the structure of code without changing what it does
    -   Like refactoring an equation
    -   Because nobody gets it right the first time [Bran1995](#BIB)
-   Most discussions of refactoring focus on [object-oriented programming](#g:oop)
-   But many patterns can and should be used to clean up [procedural](#g:procedural-programming) code
    -   An example of [design patterns](#g:design-patterns)

## Replace Value With Name {#s:refactoring-replace-value-with-name}

-   I.e., define a constant
-   Easier to understand when read aloud (which is always a good test)
-   Easier to change
    -   You don't think you'll have to, but then people want to use your software on Mars [Mak2006](#BIB)

```python
# BEFORE
seconds_elapsed = num_days * 24 * 60 * 60
```
```python
# AFTER
SECONDS_PER_DAY = 24 * 60 * 60
...
seconds_elapsed = num_days * SECONDS_PER_DAY
```

## Hoist Repeated Calculation Out of Loop {#s:refactoring-hoist-repeated}

-   Move something that is being re-calculated inside a loop out of the loop
-   More efficient
-   More readable: makes it clear that the value actually *is* the same
    -   And by naming the common value, you're signalling its meaning

```python
# BEFORE
for sample in all_signals:
    transform.append(2 * pi * sample / normalize)
```
```python
# AFTER
scaling = 2 * pi / normalize
for sample in all_signals:
    transform.append(sample * scaling)
```

## Replace Repeated Test With Flag {#s:refactoring-repeated-test}

-   Booleans are values and can be assigned
-   Note: do *not* need to compare to `True` or `False`
    -   `if greater == True` is the same as `if greater`
    -   `if greater == False` is the same as `if not greater`

```python
greater = estimate > 0.0
...other code that possibly changes estimate...
if greater:
    ...do something...
```

-   Using a flag instead of repeating the test is therefore like assigning a calculation to a "constant" and using it later
-   Like using a constant, doing this makes intention clearer (these really are the same test) and future changes easier

```python
# BEFORE
def process_data(data, scaling):
    if len(data) > THRESHOLD:
        scaling = sqrt(scaling)
    ...process data to create score...
    if len(data) > THRESHOLD:
        score = score ** 2
```
```python
# AFTER
def process_data(data, scaling):
    is_large_data = len(data) > THRESHOLD
    if is_large_data:
        scaling = sqrt(scaling)
    ...process data to create score...
    if is_large_data:
        score = score ** 2
```

-   If the test needs to change to `>=`, the `AFTER` version is more likely to be right the first time

## Use In-Place Operator {#s:refactoring-in-place}

-   An [in-place operator](#g:in-place-operator) does a calculation with two values and overwrites one of those values
-   Instead of `x = x + 1`, write `x += 1`
-   `samples[least_factor_index, max(current_offset, offset_limit)] *= scaling_factor` is much easier to read if the array indexing *isn't* repeated
-   Using in-place operators also makes it clear that a value is being overwritten
    -    `samples[day-1, hour, minute-1] = samples[day-1, hour, minute+1] + latest_reading` is really, really hard to spot

```python
# BEFORE
for least_factor_index in all_factor_indexes:
    samples[least_factor_index, max(current_offset, offset_limit)] = \
        samples[least_factor_index, max(current_offset, offset_limit)] * scaling_factor
```
```python
# AFTER
for least_factor_index in all_factor_indexes:
    samples[least_factor_index, max(current_offset, offset_limit)] *= scaling_factor
```

## Place Short Circuits Early {#s:refactoring-short-circuits}

-   A [short circuit](#g:short-circuit) test is a quick check to handle a special case
-   Place these near the start of functions to give readers a sense of what the remaining code is there to handle

```python
# BEFORE
def rescale_by_average(values, factors, weights):
    a = 0.0
    for (f, w) in zip(factors, weights):
        a += f * w
    if a == 0.0:
        return
    a /= len(f)
    if not values:
        return
    else:
        for (i, v) in enumerate(values):
            values[i] = v / a
```
```python
# AFTER
def rescale_by_average(values, factors, weights):
    if (not values) or (not factors) or (not weights):
        return
    a = 0.0
    for (f, w) in zip(factors, weights):
        a += f * w
    a /= len(f)
    for (i, v) in enumerate(values):
        values[i] = v / a
```

## Default and Override {#s:refactoring-default-override}

-   Make default clear by putting it first, unconditionally
-   Then override in special case
-   Means executing two assignments instead of one, but fewer lines of code

```python
# BEFORE
if configuration['threshold'] > UPPER_BOUND:
    scale = 0.8
else:
    scale = 1.0
```
```python
# AFTER
scale = 1.0
if configuration['threshold'] > UPPER_BOUND:
    scale = 0.8
```

-   For simple cases, can put onto one line

```python
# SOMETIMES
scale = 1.0
if configuration['threshold'] > UPPER_BOUND: scale = 0.8
```

-   Some programmers prefer to use [conditional expression](#g:conditional-expression)

```python
# BETTER
scale = 0.8 if configuration['threshold'] > UPPER_BOUND else 1.0
```

-   However, this puts the default last instead of first, which is unclear
    -   Can invert the sense of the test, but that's also confusing

## Extract Function {#s:refactoring-extract-function}

-   Move common operations into functions to reduce amount of code that needs to be read
-   Move complex operations into functions to reduce cognitive load
    -   Signals that something can be understood separately
-   If you can't think of a plausible name, or if a lot of data has to come *out* of the function,
    it probably shouldn't be extracted

```python
# BEFORE
def check_neighbors(grid, point):
    if (0 < point.x) and (point.x < grid.width) and \
       (0 < point.y) and (point.y < grid.height):
        ...look at all four neighbors
```
```python
# AFTER
def check_neighbors(grid, point):
    if in_interior(grid, point):
        ...look at all four neighbors...

def in_interior(grid, point):
    ...four tests as above...
```

-   Function might be usable in other contexts
    -   But even if not, it is (again) easier to read aloud
-   Use original variable names as parameter names during refactoring to reduce typing
-   Multi-part conditionals, parts of long equations, and bodies of loops are good candidates for extraction

## Combine Functions {#s:refactoring-combine-functions}

-   Opposite of Extract Function
-   If operations always done together, might be more efficient to combine
-   And *might* be easier to understand
-   But probably decreases reusability
-   And usually makes code harder to maintain

```python
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
```python
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

-   Note that this assumes characters are either vowels or consonants, where the split implementation didn't
    -   This implementation *could* use two independent tests instead of `elif`
    -   But you probably didn't notice the change in semantics
-   One sign that functions shouldn't have been combined is how often people use the combination and throw some results away

## Create Lookup Table {#s:refactoring-lookup}

-   Easier to understand (and therefore maintain) lookup tables than complicated conditionals
    -   An example of [declarative programming](#g:declarative-programming) (see [CHAPTER](../automate/))

```python
# BEFORE
def count_vowels_and_consonants(text):
    ...as above...
```
```python
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

-   Note that this fails for spaces, punctuation, etc.
-   Every lookup table should either:
    -   Have a value for "none of the above"
    -   Or raise an error

```python
# BETTER

IS_VOWEL = {'a' : 1, 'b' : 0, 'c' : 0, ... }
IS_CONSONANT = {'a' : 0, 'b' : 1, 'c' : 1, ... }

def count_vowels_and_consonants(text):
    num_vowels = num_consonants = 0
    for char in text:
        num_vowels += IS_VOWEL.get(char, 0)
        num_consonants += IS_CONSONANT.get(char, 0)
    return num_vowels, num_consonants
```

-   Note: in this case, could use a set, check for membership, and increment
-   So we should only use lookup tables when weights differ among elements

## Replace Loop With Comprehension {#s:refactoring-comprehension}

-   Many language features exist to give programmers something to refactor *to*
    -   See a pattern in many contexts
    -   Provide syntactic support for it
    -   Explain in terms of original
-   Comprehensions exist to replace simple loops

```python
# BEFORE
result = []
for num in values:
    result.append(num * num)
```
```python
# AFTER
result = [num * num for num in values]
```

-   Easier to read *for simple calculations*
-   Becomes more complicated to understand with conditionals

```python
# BEFORE
result = []
for num in values:
    if num > 0:
        result.append(num * num)
```
```python
# AFTER
result = [num * num for num in values if num > 0]
```

-   But `if`-`else` is structured differently

```python
# BEFORE
result = []
for num in values:
    if num > 0:
        result.append(num * num)
    else:
        result.append(0)
```
```python
# AFTER
result = [num * num if num > 0 else 0 for num in values]
```

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

-   What's hardest to remember is the equivalent of nested loops where the inner loop depends on the outer
    -   Order in expression feels inverted

```
words = ['first', 'second', 'third']
flattened = [c for w in words for c in w]
```

-   Works for sets, dictionaries, and anything else that can be iterated over
-   This is the direction most modern Python is going, so write comprehensions for new code and refactor wherever you can
-   And don't be afraid (at least during development) to create temporaries

## Summary {#s:refactoring-summary}

-   A good test of code quality: each plausible small change to functionality requires one change in one place

FIXME: create concept map for refactoring

{% include links.md %}
