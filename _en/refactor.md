---
title: "Refactoring"
undone: true
questions:
-   "How can I improve code that already works?"
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

[Refactoring](#g:refactor) means changing the structure of code without changing what it does,
like refactoring an equation to simplify it.
It is just as much a part of programming as writing code in the first place:
nobody gets things right the first time [Bran1995](#BIB),
and needs or insights can change over time.

Most discussions of refactoring focus on [object-oriented programming](#g:oop),
but many patterns can and should be used to clean up [procedural](#g:procedural-programming) code.
This lesson describes and motivates some of the most useful patterns;
These rules are examples of [design patterns](#g:design-patterns):
general solutions to commonly occurring problems in software design.
Knowing them and their names will help you create better software,
and also make it easier for you to communicate with your peers.

## How can I avoid repeating values in code? {#s:refactoring-replace-value-with-name}

Our first and simplest refactoring is called "replace value with name".
It tells us to replace magic numbers with names,
i.e., to define constants.
This can seem ridiculous in simple cases
(why define and use `inches_per_foot` instead of just writing 12?).
However,
what may be obvious to you when you're writing code won't be obvious to the next person,
particularly if they're working in a different context
(most of the world uses the metric system and doesn't know how many inches are in a foot).
It's also a matter of habit:
if you write numbers without explanation in your code for simple cases,
you're more likely to do so for complex cases,
and more likely to regret it afterward.

Using names instead of raw values also makes it easier to understand code when you read it aloud,
which is always a good test of its style.
Finally,
a single value defined in one place is much easier to change
than a bunch of numbers scattered throughout your program.
You may not think you will have to change it,
but then people want to use your software on Mars and you discover that constants aren't [Mak2006](#BIB).

{% include refactor/replace_value_with_name.html %}

## How can I avoid repeating calculations in code? {#s:refactoring-hoist-repeated}

It's inefficient to calculate the same value over and over again.
It also makes code less readable:
if a calculation is inside a loop or a function,
readers will assume that it might change each time the code is executed.

Our second refactoring,
"hoist repeated calculation out of loop",
tells us to move the repeated calculation out of the loop or function.
Doing this signals that its value is always the same.
And by naming that common value,
you help readers understand what its purpose is.

{% include refactor/hoist_repeated_calculation.html %}

## How can I make repeated conditional tests clearer? {#s:refactoring-repeated-test}

Novice programmers frequently write conditional tests like this:

```python
if (a > b) == True:
    # ...do something...
```

<!-- == \noindent -->
The comparison to `True` is unnecessary because `a > b` is a Boolean value
that is itself either `True` or `False`.
Like any other value,
Booleans can be assigned to variables,
and those variables can then be used directly in tests:

```python
was_greater = estimate > 0.0
# ...other code that might change estimate...
if was_greater:
    # ...do something...
```

<!-- == \noindent -->
This refactoring is called "replace repeated test with flag".
When it is used,
there is no need to write `if was_greater == True`:
that always produces the same result as `if was_greater`.
Similarly, the equality tests in `if was_greater == False` is redundant:
the expression can simply be written `if not was_greater`.
Creating and using a [flag](#g:flag) instead of repeating the test
is therefore like moving a calculation out of a loop:
even if that value is only used once,
it makes our intention clearer---these really are the same test.

{% include refactor/replace_repeated_test_with_flag.html %}

<!-- == \noindent -->
If it takes many lines of code to process data and create a score,
and the test then needs to change from `>` to `>=`,
we're more likely to get the refactored version right the first time,
since the test only appears in one place and its result is given a name.

## How can I avoid duplicating expressions in assignment statements? {#s:refactoring-in-place}

An [in-place operator](#g:in-place-operator),
sometimes called an [update operator](#g:update-operator),
does a calculation with two values
and overwrites one of the values.
For example,
instead of writing:

```python
step = step + 1
```

<!-- == \noindent -->
we can write:

```python
step += 1
```

In-place operators save us some typing.
They also make the intention clearer,
and most importantly,
they make it harder to get complex assignments wrong.
For example:

```python
samples[least_factor_index, max(current_offset, offset_limit)] *= scaling_factor
```

<!-- == \noindent -->
is much easier to read than the equivalent expression:

```python
samples[least_factor_index, max(current_offset, offset_limit)] = \
    scaling_factor * samples[least_factor_index, max(current_limit, offset_limit)]
```

<!-- == \noindent -->
(The proof of this claim is that you probably didn't notice on first reading
that the long form uses different expressions to index `samples`
on the left and right of the assignment.)
The refactoring "use in-place operator" does what its name suggests:
converts normal assignments into their briefer equivalents.

{% include refactor/use-in-place-operator.html %}

## How can I make special cases easier to spot? {#s:refactoring-short-circuits}

A [short circuit test](#g:short-circuit-test) is a quick check to handle a special case,
such as checking the length of a list of values
and returning `math.nan` for the average if the list is empty.
"Place short circuits early" tells us to put short-circuit tests near the start of functions
so that readers can mentally remove special cases from their thinking
while reading the code that handles the usual case.

{% include refactor/place-short-circuits-early.html %}

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
