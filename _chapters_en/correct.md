---
permalink: "/en/correct/"
title: "Making Sure It's Right"
questions:
-   FIXME
objectives:
-   FIXME
keypoints:
-   FIXME
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
    -   Input: list of (filename, stats) pairs, where stats is a set of words occuring in that filename
    -   Output: list of (word, filename, IDF) triples
    -   We're not allowed to change the input or output formats (for now)
-   Put each input-output pair in a function in `test_idf.py`
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

## Is It Close Enough? (#s:correct-float)

-   Recap of floating point roundoff
-   Use `pytest.approx` with a [relative error](#g:relative-error) rather than an [absolute error](#g:absolute-error)
    -   It works on lists, sets, arrays, and other collections

## Did It Fail As It Was Supposed To? {#s:correct-exception}

-   Did the call fail as it was supposed to, i.e., raise the right kind of exception?
    -   Many errors in production systems happen because people don't test their error handling code [[Yuan2014](#CITE)]

```
FIXME: example
```

## Testing File I/O {#s:correct-io}

-   Reading from external files isn't so bad, but writing to temporary files is awkward
    -   Scraps need to be re-read for testing and then cleaned up
-   Introduction to `StringIO`
-   Reorganize software so that file opening is done separately from reading/writing
    -   Good practice anyway for handling `stdin` and `stdout` in command-line tools

## Testing Plots {#s:correct-plots}

-   [Testing plots and other images](https://github.com/matplotlib/pytest-mpl)
    -   Simpler to test the data structures and trust the plotting library

## Testing Randomness {#s:correct-random}

-   Testing random numbers: always allow specification of the seed

## Testing Data Analysis {#s:correct-analysis}

-   Sanity tests
    -   Same number of output records as input records
    -   *Or* fewer output records than input records
    -   Standard deviation has to be smaller than the range of the data
    -   NaNs and NULLs only where you're expecting them (check between each stage of the pipeline)
-   Subsampling
    -   Choose random subsets of input data, do analysis, see how close output is to output with full data set
    -   If output doesn't converge as sample size grows, something is probably unstable
    -   (Which is not the same as wrong)
-   Edge cases
    -   Uniform data, i.e., same values for all observations
    -   Strictly bimodal data
    -   Data generated from known distribution
-   Example: generate text that exactly conforms to Zipf's Law and test analysis

## Coverage {#s:correct-coverage}

-   [Test coverage](#g:test-coverage) measures which parts of program are(n't) exercised by tests
-   Easy (and wrong) to obsess about meeting specific targets
-   But:
    -   Anything that *isn't* tested should be assumed to be wrong
    -   Drops in coverage often indicate new [technical debt](#g:technical-debt)
-   Run `coverage` with tests
-   Look at summary report
-   Drill down into line-by-line HTML listing

{% include links.md %}
