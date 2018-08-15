---
permalink: "/en/correct/"
title: "Testing Data Analysis"
questions:
-   "How should I test data analysis pipelines?"
objectives:
-   "Explain why it is hard to test code that produces plots or other graphical output."
-   "Describe and implement heuristics for testing data analysis."
-   "Describe the role of inference in data analysis testing and use the `tdda` library to find and check constraints on tabular data."
keypoints:
-   "Programmers should use tolerances when comparing floating-point numbers (not just in tests)."
-   "Test the data structures used in plotting rather than the plots themselves."
-   "Check that parametric or non-parametric statistics of data do not differ from saved values by more than a specified tolerance."
-   "Infer constraints on data and then check that subsequent data sets obey these constraints."
---

-   FIXME: introduction

## Is It Close Enough? {#s:correct-float}

-   Recap of floating point roundoff
-   Use `pytest.approx` with a [relative error](#g:relative-error) rather than an [absolute error](#g:absolute-error)
    -   It works on lists, sets, arrays, and other collections

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

### Exercises

FIXME: exercises

## Summary {#s:correct-summary}

FIXME: create concept map

{% include links.md %}
