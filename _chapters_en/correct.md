---
permalink: "/en/correct/"
title: "Making Sure It's Right"
questions:
-   "How can I tell if my software is working correctly?"
-   "How can other people tell if it is?"
-   "What does 'correctly' even mean?"
-   "How can I tell that I've done enough testing (or at least adequate testing)?"
objectives:
-   "Explain what realistic technical and social goals for software testing are."
-   "Explain what a test runner is."
-   "Explain what a text fixture is."
-   "Write and run unit tests using Python's `pytest` test runner."
-   "Write tests that take floating-point roundoff into account."
-   "Write tests that check whether software fails when and as it is supposed to."
-   "Write tests for functions that use random numbers, dates and times, and other sources of unpredictability."
-   "Write tests for functions that do file I/O."
-   "Explain why it is hard to test code that produces plots or other graphical output."
-   "Describe and implement heuristics for testing data analysis."
-   "Describe the role of inference in data analysis testing and use the `tdda` library to find and check constraints on tabular data."
keypoints:
-   "Testing can only ever show that software has flaws, not that it is correct."
-   "Its real purpose is to convince people (including yourself) that software is correct enough, and to make tolerances on 'enough' explicit."
-   "A test runner finds and runs tests written in a prescribed fashion and reports their results."
-   "A unit test can pass (work as expected), fail (meaning the software under test is flawed), or produce an error (meaning the test itself is flawed)."
-   "A fixture is the data or other input that a test is run on."
-   "Every unit test should be independent of every other to keep results comprehensible and reliable."
-   "Programmers should use tolerances when comparing floating-point numbers (not just in tests)."
-   "Programmers should check that their software fails when and as it is supposed to in order to avoid silent errors."
-   "Write test doubles to replace unpredictable inputs such as random numbers or the current date or time with a predictable value."
-   "Use string I/O doubles when testing file input and output."
-   "Test the data structures used in plotting rather than the plots themselves."
-   "Check that parametric or non-parametric statistics of data do not differ from saved values by more than a specified tolerance."
-   "Infer constraints on data and then check that subsequent data sets obey these constraints."
---

-   [Term frequency-inverse document frequency][tf-idf] (TF-IDF) is a way to determine how relevant a document is in a search
    -   Term frequency: (# occurrences of word) / (# words in document)
    -   Inverse document frequency: (# documents) / (# documents in which word occurs)
    -   If a word is very common in one document, but absent in others, TF-IDF is high for that (word, document) pair
    -   If a word is common in all documents, or if a word is rare in a document, TF-IDF is lower
-   Input: one CSV file for each document containing (word, count) pairs
-   Output: a CSV file containing (word, document, TF-IDF score) for each word and each document
-   Our goal: test the program that produces this table
-   More specifically:
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

## Some Simple Test Cases {#s:correct-simple}

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

## Is It Close Enough? {#s:correct-float}

-   Recap of floating point roundoff
-   Use `pytest.approx` with a [relative error](#g:relative-error) rather than an [absolute error](#g:absolute-error)
    -   It works on lists, sets, arrays, and other collections

### Exercises

FIXME: exercises

## Did It Fail As It Was Supposed To? {#s:correct-exception}

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

## Testing Randomness {#s:correct-random}

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

## Testing File I/O {#s:correct-io}

-   Reading from external files isn't so bad, but writing to temporary files is awkward
    -   Scraps need to be re-read for testing and then cleaned up
-   Introduction to `StringIO`
-   Reorganize software so that file opening is done separately from reading/writing
    -   Good practice anyway for handling `stdin` and `stdout` in command-line tools

### Exercises

FIXME: exercises

## Testing Plots {#s:correct-plots}

-   This is hard, so try not to do it
    -   Test the data and data structures going into your plots instead, and trust the plotting library
    -   Testing user interfaces is similarly hard, for similar reasons

```
FIXME: example
```

-   If you really need to test the image, there are [tools][pytest-mpl] that compare images
    -   Root mean square (RMS) difference between images must be below a threshold for the comparison to pass
    -   Enables you to turn off comparison of text (because font differences can throw up spurious failures)
    -   If images are close enough that a human being would make the same decision about meaning, the test should pass

### Exercises

FIXME: exercises

## Testing Data Analysis {#s:correct-analysis}

-   Sanity tests
    -   Same number of output records as input records
    -   Or fewer output records than input records if you're aggregating
    -   Or a product if you're joining
    -   Standard deviation has to be smaller than the range of the data
    -   NaNs and NULLs only where you're expecting them (check between each stage of the pipeline)
-   Verify that distribution isn't changing
    -   Non-parametric: create histogram of results for test data, verify that subsequent data fits histogram
    -   Although you still have to decide what "fits" means
-   Verify data against a distribution
    -   Test that data fits a distribution (if you know what distribution to expect)
    -   E.g., [Shapiro-Wilk test][shapiro-wilk] that data is normal
    -   Still requires a tolerance, but at least you're now making your tolerances specific
-   Subsampling
    -   Choose random subsets of input data, do analysis, see how close output is to output with full data set
    -   If output doesn't converge as sample size grows, something is probably unstable
    -   Which is not the same as wrong: it's a problem with the algorithm, rather than with the implementation
-   Test with edge cases
    -   Uniform data, i.e., same values for all observations
    -   Strictly bimodal data
    -   Data generated from known distribution
-   Example: generate text that exactly conforms to Zipf's Law and test analysis

### Exercises

FIXME: exercises

## Inferring Constraints {#s:correct-infer}

-   The [TDDA library][tdda-site] can infer test rules from data
-   `age <= 100`, `Date` should be sorted ascending, `StartDate <= EndDate`, etc.
-   Comes with a command-line tool `tdda`
    -   `tdda discover elements92.csv elements.tdda` infers rules from data
    -   `tdda verify elements92.csv elements.tdda` verifies data against those rules (should pass)
-   Inferred rules are stored as JSON, and are (sort of) readable
    -   Reading and modifying the rules is a good way to get to know your data

```
"fields": {
    "Name": {
        "type": "string",
        "min_length": 3,
        "max_length": 12,
        "max_nulls": 0,
        "no_duplicates": true
    },
    "Symbol": {
        "type": "string",
        "min_length": 1,
        "max_length": 2,
        "max_nulls": 0,
        "no_duplicates": true
    },
    "ChemicalSeries": {
        "type": "string",
        "min_length": 7,
        "max_length": 20,
        "max_nulls": 0,
        "allowed_values": [
            "Actinoid",
            "Alkali metal",
            "Alkaline earth metal",
            "Halogen",
            "Lanthanoid",
            "Metalloid",
            "Noble gas",
            "Nonmetal",
            "Poor metal",
            "Transition metal"
        ]
    },
    "AtomicWeight": {
        "type": "real",
        "min": 1.007947,
        "max": 238.028913,
        "sign": "positive",
        "max_nulls": 0
    },
    ...
}
```

-   Apply these inferred rules to all elements
    -   `-7` to get pure ASCII output
    -   `-f` to show only fields with failures

```
$ tdda verify -7 -f elements118.csv elements92.tdda 
FIELDS:

Name: 1 failure  4 passes  type OK  min_length OK  max_length X  max_nulls OK  no_duplicates OK

Symbol: 1 failure  4 passes  type OK  min_length OK  max_length X  max_nulls OK  no_duplicates OK

AtomicWeight: 2 failures  3 passes  type OK  min OK  max X  sign OK  max_nulls X

...others...

SUMMARY:

Constraints passing: 57
Constraints failing: 15
```

-   Additional use: generate constraints for two datasets and then look at differences in constraint files
-   Especially useful if the constraint file is put under version control

## Coverage {#s:correct-coverage}

-   [Test coverage](#g:test-coverage) measures which parts of program are(n't) exercised by tests
-   Easy (and wrong) to obsess about meeting specific targets
-   But:
    -   Anything that *isn't* tested should be assumed to be wrong
    -   Drops in coverage often indicate new [technical debt](#g:technical-debt)
-   Run `coverage` with tests
-   Look at summary report
-   Drill down into line-by-line HTML listing

## Test-Driven Development {#s:correct-tdd}

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

{% include links.md %}
