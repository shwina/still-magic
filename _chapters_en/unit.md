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
-   Input: one CSV file for each document containing (word, count) pairs
-   Output: a CSV file containing (word, document, TF-IDF score) for each word and each document
-   Goals for testing:
    -   Make it easy for people to write tests (because otherwise they won't do it)
    -   Run a set of tests
    -   Report which ones have failed
    -   Give some idea of where or why they failed (to help debugging)
    -   Give some idea of whether any results have changed since the last run
    -   Give people a clear idea of what our [tolerances](#g:tolerance) are
-   A test that checks one thing is called a [unit test](#g:unit-test)
-   A tool that finds and runs unit tests and reports their results is called a [test runner](#g:test-runner)
-   A single test can have one of three outcomes:
    -   Pass: everything worked as expected
    -   Fail: something went wrong in the software being tested
    -   Error: something went wrong in the test itself (so we don't know anything about the software being tested)
-   A [fixture](#g:fixture) is what the test is run on, e.g., the input data
-   Good tests are independent
    -   Should produce the same results no matter what order they are run in
    -   Which means that each test starts from a freshly-generated fixture rather than using the output of previous tests
    -   Otherwise a failure in one test can cause false positives or false negatives in subsequent tests
-   This introduction is based in part on [Testing and Continuous Integration with Python][huff-testing] by [Katy Huff][huff-katy]

## Some Simple Test Cases {#s:unit-simple}

-   Start with a simpler problem: test the calculation of IDF
    -   Input: list of (filename, word, count) triples
    -   Output: list of (word, filename, IDF) triples
    -   We're not allowed to change the input or output formats (for now)
-   Roll our own
    -   `assert` that inputs produce outputs (example)
    -   But our test script halts at the first failure
    -   And we may want to split tests across files (e.g., to test different parts of the analysis)
-   Instead, put each input-output pair in a function in `test_idf.py`
    -   Use `assert` to check that the output is correct
    -   Calculate "correct" by hand for simple cases
    -   If they don't work, nothing else is likely to...
-   Note the absence of an error message in the `assert`
    -   Name of test function is included in the output if the test fails
    -   That name should be all the documentation we need
    -   If the test is so complicated that more is needed, write a simpler test

```
FIXME: examples
```

-   Run from the command line

```
$ pytest
```
```
FIXME: output
```

-   Searches for all files named `test_*.py` or `*_test.py` in the current directory and its sub-directories
-   Runs all functions in those files whose names start with `test_`
-   Records pass/fail/error counts
-   Gives us a nicely-formatted report
-   Works the same way for everyone, so we can test without having think about *how* (only about *what*)
    -   Although fitting tests into this framework sometimes requires some tricks

### Exercises

FIXME: exercises

## Did It Fail As It Was Supposed To? {#s:unit-exception}

-   Did the call fail as it was supposed to, i.e., raise the right kind of exception?
    -   If not, system could produce a [silent error](#g:silent-error)
-   Many errors in production systems happen because people don't test their error handling code [[Yuan2014](#CITE)]
    -   Almost all (92%) of the catastrophic system failures are the result of
        incorrect handling of non-fatal errors explicitly signaled in software.
    -   In 58% of the catastrophic failures, the underlying faults could easily have
        been detected through simple testing of error handling code.
    -   A majority (77%) of the failures require more than one input event to manifest, but
        most of the failures (90%) require no more than 3.

```
FIXME: example
```

### Exercises

FIXME: exercises

## Testing Randomness {#s:unit-random}

-   Testing random numbers: always allow specification of the seed
-   Dates and times count as randomness
    -   Write your own function
    -   Replace it with another for testing purposes
-   The replacement is called a [test double](#g:test-double)
    -   Or a mock, or a stub, or... terminology is very inconsistent

```
FIXME: example
```

### Exercises

FIXME: exercises

## Testing File I/O {#s:unit-io}

-   Reading from external files isn't so bad, but writing to temporary files is awkward
    -   Scraps need to be re-read for testing and then cleaned up
-   Introduction to `StringIO`
-   Reorganize software so that file opening is done separately from reading/writing
    -   Good practice anyway for handling `stdin` and `stdout` in command-line tools

### Exercises

FIXME: exercises

## Coverage {#s:unit-coverage}

-   [Test coverage](#g:test-coverage) measures which parts of program are(n't) exercised by tests
-   Easy (and wrong) to obsess about meeting specific targets
-   But:
    -   Anything that *isn't* tested should be assumed to be wrong
    -   Drops in coverage often indicate new [technical debt](#g:technical-debt)
-   Run `coverage` with tests
-   Look at summary report
-   Drill down into line-by-line HTML listing

### Exercises

FIXME: exercises

## Summary {#s:unit-summary}

-   [Test-driven development](#g:tdd) (TDD)
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
    -   Empirical studies have not found a strong effect [[Fucc2016](#CITE)]
    -   But many productive programmers believe in it, so maybe we're measuring the wrong things...

FIXME: create concept map

{% include links.md %}
