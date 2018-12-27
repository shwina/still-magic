---
permalink: "/en/unit/"
title: "Unit Testing"
questions:
-   "How should I write tests for my software?"
-   "How can I tell how much testing I've actually done?"
objectives:
-   "Explain what realistic technical and social goals for software testing are."
-   "Explain what a test runner is."
-   "Explain what a text fixture is."
-   "Write and run unit tests using Python's `pytest` test runner."
-   "Check test coverage using Python's `coverage` module."
keypoints:
-   "Testing can only ever show that software has flaws, not that it is correct."
-   "Its real purpose is to convince people (including yourself) that software is correct enough, and to make tolerances on 'enough' explicit."
-   "A test runner finds and runs tests written in a prescribed fashion and reports their results."
-   "A unit test can pass (work as expected), fail (meaning the software under test is flawed), or produce an error (meaning the test itself is flawed)."
-   "A fixture is the data or other input that a test is run on."
-   "Every unit test should be independent of every other to keep results comprehensible and reliable."
-   "Programmers should check that their software fails when and as it is supposed to in order to avoid silent errors."
-   "Write test doubles to replace unpredictable inputs such as random numbers or the current date or time with a predictable value."
-   "Use string I/O doubles when testing file input and output."
-   "Use a coverage tool to check how well tests have exercised code."
---

-   [Term frequency-inverse document frequency][tf-idf] (TF-IDF) is a way to determine how relevant a document is in a search
    -   Term frequency: (# occurrences of word) / (# words in document)
    -   Inverse document frequency: (# documents) / (# documents in which word occurs)
    -   If a word is very common in one document, but absent in others, TF-IDF is high for that (word, document) pair
    -   If a word is common in all documents, or if a word is rare in a document, TF-IDF is lower
-   Depends on counting words in a document
    -   While ignoring leading/trailing punctuation
    -   Except for words like "Ph.D."
    -   And what to do about hyphenation?
-   Goals for testing:
    -   Make it easy for people to write tests (because otherwise they won't do it)
    -   Run a set of tests
    -   Report which ones have failed
    -   Give some idea of where or why they failed (to help debugging)
    -   Give some idea of whether any results have changed since the last run
    -   Give people a clear idea of what our definition of correct and our [tolerances](../gloss/#g:tolerance) are
-   This introduction is based in part on [Testing and Continuous Integration with Python][huff-testing] by [Katy Huff][huff-katy]

## What Does a Systematic Software Testing Framework Look Like? {#s:unit-own}

-   A test that checks one thing is called a [unit test](../gloss/#g:unit-test)
-   A tool that finds and runs unit tests and reports their results is called a [test runner](../gloss/#g:test-runner)
-   A single test can have one of three outcomes:
    -   Pass: everything worked as expected
    -   Fail: something went wrong in the software being tested
    -   Error: something went wrong in the test itself (so we don't know anything about the software being tested)
-   A [fixture](../gloss/#g:fixture) is what the test is run on, e.g., the input data
-   Good tests are independent
    -   Should produce the same results no matter what order they are run in
    -   Which means that each test starts from a freshly-generated fixture rather than using the output of previous tests
    -   Otherwise a failure in one test can cause false positives or false negatives in subsequent tests
-   Roll our own

```python
TESTS = [
   ['word', {'word' : 1}],
   ['word word', {'word' : 2}],
   ['another word', {'another' : 1, 'word' : 1}],
   ["anothers' word", {'anothers' : 1, 'word' : 1}]
]

pass = fail = error = 0
for (fixture, expected) in TESTS:
    try:
        actual = count_words(fixture)
        if actual == expected:
            pass += 1
        else:
            fail += 1
    except:
        error += 1
print('pass {} fail {} error {}'.format(pass, fail, error))
```

-   This works
-   But what if test fixtures take several lines to construct?
-   Or checking result is complex?
-   Or we have tests split across multiple files?
-   Or...

## How Can I Use a Standard Software Testing Framework? {#s:unit-pytest}

-   Instead, put each input-output pair in a function in `test_count.py`
-   Use `assert` to check that the output is correct

```python
from tf_idf import count_word

def test_single_word():
    assert count_words('word') == {'word' : 1}

def test_single_repeated_word():
   assert count_words('word word') == {'word' : 2}

def test_two_words():
   assert count_words('another word') == {'another' : 1, 'word' : 1}

def test_trailing_punctuation():
   assert count_words("anothers' word") == {'anothers' : 1, 'word' : 1}
```

-   Note the absence of an error message in the `assert`
    -   Name of test function is included in the output if the test fails
    -   That name should be all the documentation we need
    -   If the test is so complicated that more is needed, write a simpler test
-   Run from the command line

```
$ pytest
```
```
============================= test session starts ==============================
platform darwin -- Python 3.6.5, pytest-3.5.1, py-1.5.3, pluggy-0.6.0
rootdir: /Users/standage/still-magic/src/unit, inifile:
plugins: remotedata-0.2.1, openfiles-0.3.0, doctestplus-0.1.3, arraydiff-0.2
collected 4 items

test_count.py ...F                                                       [100%]

=================================== FAILURES ===================================
__________________________ test_trailing_punctuation ___________________________

    def test_trailing_punctuation():
>      assert count_words("anothers' word") == {'anothers' : 1, 'word' : 1}
E      assert {"anothers'": 1, 'word': 1} == {'anothers': 1, 'word': 1}
E        Omitting 1 identical items, use -vv to show
E        Left contains more items:
E        {"anothers'": 1}
E        Right contains more items:
E        {'anothers': 1}
E        Use -v to get the full diff

test_count.py:13: AssertionError
====================== 1 failed, 3 passed in 0.05 seconds ======================
```

-   Searches for all files named `test_*.py` or `*_test.py` in the current directory and its sub-directories
    -   Can use command-line options to narrow the search, e.g., `pytest test_count.py`
-   Runs all functions in those files whose names start with `test_`
-   Records pass/fail/error counts
-   Gives us a nicely-formatted report
-   Works the same way for everyone, so we can test without having think about *how* (only about *what*)
    -   Although fitting tests into this framework sometimes requires some tricks

## How Can I Tell If My Software Failed As It Was Supposed To? {#s:unit-exception}

-   Did the call fail as it was supposed to, i.e., raise the right kind of exception?
    -   If not, system could produce a [silent error](../gloss/#g:silent-error)
-   Many errors in production systems happen because people don't test their error handling code [Yuan2014](#BIB)
    -   Almost all (92%) of the catastrophic system failures are the result of
        incorrect handling of non-fatal errors explicitly signaled in software.
    -   In 58% of the catastrophic failures, the underlying faults could easily have
        been detected through simple testing of error handling code.
    -   A majority (77%) of the failures require more than one input event to manifest, but
        most of the failures (90%) require no more than 3.
-   Can check manually:

```python
# Expect count_words to raise ValueError for empty input.
def test_text_not_empty():
    try:
        count_words('')
        assert False, 'Should not get this far'
    except ValueError:
        pass
```

-   Better: `pytest` provides a [context manager](../gloss/#g:context-manager) to handle tests for exceptions
    -   Uses Python's `with` keyword to create something for a particular scope

```python
import pytest

def test_text_not_empty():
    with pytest.raises(ValueError):
        count_words('')
```
```
============================= test session starts ==============================
platform darwin -- Python 3.6.5, pytest-3.5.1, py-1.5.3, pluggy-0.6.0
rootdir: /Users/gvwilson/merely-useful/still-magic/src/unit, inifile:
plugins: remotedata-0.2.1, openfiles-0.3.0, doctestplus-0.1.3, arraydiff-0.2
collected 1 item

test_exception.py F                                                      [100%]

=================================== FAILURES ===================================
_____________________________ test_text_not_empty ______________________________

    def test_text_not_empty():
        with pytest.raises(ValueError):
>           count_words('')
E           Failed: DID NOT RAISE <class 'ValueError'>

test_exception.py:6: Failed
=========================== 1 failed in 0.04 seconds ===========================
```

-   Clearly, we have some work to do...

## How Can I Test Software That is Random or Unpredictable? {#s:unit-random}

-   Testing random numbers
    -   Rely on the fact that they aren't actually random
    -   *Always* specify the RNG seed
    -   And *always* record it
-   Current dates and time count as randomness
    -   Write your own function
    -   Replace it with another for testing purposes
    -   The replacement is called a [test double](../gloss/#g:test-double)
        -   Or a mock, or a stub, or... terminology is very inconsistent
    -   Or provide a way to change one function's behavior
-   First version using the latter strategy

```python
# tf_idf.py
import datetime

DAYS_PER_WEEK = 7

TESTING_DATE = None
def weeks_since_01(start):
    current = TESTING_DATE
    if current is None:
        current = datetime.date.today()
    return round((current - start).days / DAYS_PER_WEEK)
```

-   Test it

```python
# demo_test_weeks.py
import datetime
import tf_idf

print('first', tf_idf.weeks_since_01(datetime.date(2018, 8, 1)))
tf_idf.TESTING_DATE = datetime.date(2018, 8, 30)
print('second', tf_idf.weeks_since_01(datetime.date(2018, 8, 1)))
```
```
$ date
Wed 15 Aug 2018 15:14:52 EDT
$ python demo_test_weeks.py
first 2
second 4
```

-   Cleaner approach: make the test control an [attribute](../gloss/#g:function-attribute) of the function
    -   Works because body of function isn't executed as the function is defined
    -   So it's OK to refer to values that are added afterward
-   Advantage: can import the function alone, since the extra value is attached to it

```python
# demo_test_weeks.py
import datetime
from tf_idf import weeks_since_02

print('first', weeks_since_02(datetime.date(2018, 8, 1)))
weeks_since_02.testing_date = datetime.date(2018, 8, 30)
print('second', weeks_since_02(datetime.date(2018, 8, 1)))
```
```
$ python demo_test_weeks.py
first 2
second 4
```

## How Can I Test Software That Does File I/O? {#s:unit-io}

-   Reading from external files isn't so bad, but writing to temporary files is awkward
    -   Scraps need to be re-read for testing and then cleaned up
-   Use `StringIO`

```python
from io import StringIO

writer = StringIO()
for word in 'first second third'.split():
    writer.write('{}\n'.format(word))
print(writer.getvalue())
```
```
first
second
third
```

-   And for input
    -   Note: line includes trailing newline

```python
DATA = '''first
second
third'''

for line in StringIO(DATA):
    print(len(line))
```
```
6
7
5
```

-   It's common to have a function open a file, read its contents, and return the result
-   But this is hard to test, since there's no easy way to substitute a `StringIO`
-   Reorganize software so that file opening is done separately from reading/writing
    -   Good practice anyway for handling `stdin` and `stdout` in command-line tools, which don't need to be opened

```python
# BEFORE
def main(infile, outfile):
    with open(infile, 'r') as reader:
        with open(outfile, 'w') as writer:
            process(infile, outfile)
```
```python
# AFTER
def main(infile, outfile):
    reader = stdin if infile == '-' else open(infile, 'r')
    writer = stdout if outfile == '-' else open(outfile, 'w')
    process(reader, writer)
    if infile == '-': reader.close()
    if outfile == '-': writer.close()
```

## How Can I Tell Which Parts of My Software Have and Have Not Been Tested? {#s:unit-coverage}

-   Which lines are and aren't being executed?

```python
def first(left, right):
    if left < right:
        left, right = right, left
    while left > right:
        value = second(left, right)
        left, right = right, int(right/2)
    return value

def second(check, balance):
    if check > 0:
        return balance
    else:
        return 0

def main():
    final = first(3, 5)
    print(3, 5, final)

if __name__ == '__main__':
    main()
```

-   [Coverage](../gloss/#g:coverage) measures which parts of program are(n't) executed
    -   In principle, keep a list of Booleans, one per line
    -   Each time the line is executed, set the flag to `True`
    -   At the end, report `True` and `False` per line, percentages, etc.
-   Easy (and wrong) to obsess about meeting specific targets for [test coverage](../gloss/#g:test-coverage)
    -   But anything that *isn't* tested should be assumed to be wrong
    -   And drops in coverage often indicate new [technical debt](../gloss/#g:technical-debt)
-   Use `pip install coverage` to install coverage tool
-   Instead of `python filename.py` use `coverage run filename.py`
    -   Creates a file called `.coverage`
-   Run `coverage report` to get a summary of the most recent report

```
Name               Stmts   Miss  Cover
--------------------------------------
demo_coverage.py      16      1    94%
```

-   Use `coverage html` to generate an HTML listing

<table>
  <tr>
    <td>
      1<br/>
      2<br/>
      3<br/>
      4<br/>
      5<br/>
      6<br/>
      7<br/>
      8<br/>
      9<br/>
      10<br/>
      11<br/>
      12<br/>
      <span class="coverage">13</span><br/>
      14<br/>
      15<br/>
      16<br/>
      17<br/>
      18<br/>
      19<br/>
      20
    </td>
    <td>
      def first(left, right):<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;if left &lt; right:<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;left, right = right, left<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;while left > right:<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;value = second(left, right)<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;left, right = right, int(right/2)<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;return value<br/>
      <br/>
      def second(check, balance):<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;if check > 0:<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return balance<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;else:<br/>
      <span class="coverage">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return 0&nbsp;&nbsp;&nbsp;&nbsp;</span><br/>
      <br/>
      def main():<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;final = first(3, 5)<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;print(3, 5, final)<br/>
      <br/>
      if _name__ == '__main__':<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;main()
    </td>
  </tr>
</table>

## Summary {#s:unit-summary}

-   [Test-driven development](../gloss/#g:tdd) (TDD)
    -   Write a handful of tests that don't even run because the code they
        are supposed to test doesn't exist yet.
    -   Write just enough code to make those tests pass.
    -   Clean up what's just been written.
    -   Commit it to version control.
-   Advocates claim that writing tests first:
    -   Focuses people's minds on what code is supposed to
        so that they're not subject to confirmation bias when viewing test results
    -   Ensures that code actually *is* testable
    -   Ensures tests are actually written
-   Evidence backing these claims is contradictory
    -   Empirical studies have not found a strong effect [Fucc2016](#BIB)
    -   But many productive programmers believe in it, so maybe we're measuring the wrong things...

FIXME: create concept map for unit testing

{% include links.md %}
