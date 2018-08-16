---
permalink: "/en/correct/"
title: "Testing Data Analysis"
questions:
-   "How should I test a data analysis pipeline?"
objectives:
-   "Explain why floating point results aren't random but can still be unpredictable."
-   "Explain why it is hard to test code that produces plots or other graphical output."
-   "Describe and implement heuristics for testing data analysis."
-   "Describe the role of inference in data analysis testing and use the `tdda` library to find and check constraints on tabular data."
keypoints:
-   "Programmers should use tolerances when comparing floating-point numbers (not just in tests)."
-   "Test the data structures used in plotting rather than the plots themselves."
-   "Check that parametric or non-parametric statistics of data do not differ from saved values by more than a specified tolerance."
-   "Infer constraints on data and then check that subsequent data sets obey these constraints."
---

-   Previous lesson explained how to test in general
-   This lesson focuses on tests specific to data analysis pipelines
    -   Run them when building the pipeline to convince ourselves the code is correct
    -   Run them in production to make sure assumptions still hold and environment hasn't changed
-   Different from the test most software engineers write because you don't always know what the right answer is
    -   If you did, you would have submitted your report and moved on to the next problem
-   But there's a close analogy with physical experiments
    -   High school students should get $$10 m/sec^2$$
    -   Undergraduates might get $$9.8 m/sec^2$$ depending on the equipment used
    -   If any of them get $$9.806 m/sec^2$$ with a stopwatch, they're either incredibly lucky or rather foolish
-   Similarly, when testing data analysis, we specify tolerances
    -   How close is good enough?
-   Particularly important when doing repeated analyses
    -   Don't necessarily expect exactly the same result from the second data set
    -   Making tolerances explicit in tests in production tells us when something needs attention
-   Most of the time we calibrate estimates by checking real data, convincing ourselves it's OK, then re-checking whenever an alarm rings
    -   If you change things substantially the mean absolute error (which is in units of your original problem) will move noticeably
-   There are also method-specific checks
    -   A good metric for k-means clustering is homogeneity score
    -   0 = every datapoint is a different class
    -   1 = there is only one class in the cluster
    -   If the score for a production run differs from the score for an earlier run, human attention is required

## Is It Close Enough? {#s:correct-float}

-   Finding a good representation for floating point numbers is hard.
    -   We cannot represent an infinite number of real values with a finite set of bit patterns
    -   And unlike integers, no matter what values we *do* represent, there will be an infinite number of values between each of them that we can't
-   The explanation that follows is simplified---possibly over-simplified---to keep it manageable.
    -   If you want to know more, take half an hour to read [[Gold1991](#CITE)]
-   Floating point numbers are usually represented using [sign](#g:sign), [magnitude](#g:magnitude), and an [exponent](#g:exponent).
-   In a 32-bit word, the IEEE 754 standard calls for 1 bit of sign,
    23 bits for the magnitude (or [mantissa](#g:mantissa)),
    and 8 bits for the exponent
-   To illustrate the problems with floating point, we'll use a much dumber representation.
    -   Only use 5 bits: 3 for the magnitude and 2 for the exponent
    -   Don't worry about fractions or signs
-   Here are the possible values (in decimal) that we can represent this way
    -   For example, the decimal values 48 is binary 110 times 2 to the binary 11 power.
    -   Which is 6 times 2 to the third...
    -   ...or 6 times 8.
    -   Real floating point representations don't have all the redundancy that you see in this table, but it illustrates the point

<table class="table table-striped">
  <tr>
    <th></th>
    <th colspan="4">Exponent</th>
  </tr>
  <tr>
    <th>Mantissa</th> <th>00</th> <th>01</th> <th>10</th> <th>11</th>
  </tr>
  <tr>
    <th>000</th> <td>0</td> <td>0</td> <td>0</td> <td>0</td>
  </tr>
  <tr>
    <th>001</th> <td>1</td> <td>2</td> <td>4</td> <td>8</td>
  </tr>
  <tr>
    <th>010</th> <td>2</td> <td>4</td> <td>8</td> <td>16</td>
  </tr>
  <tr>
    <th>011</th> <td>3</td> <td>6</td> <td>12</td> <td>24</td>
  </tr>
  <tr>
    <th>100</th> <td>4</td> <td>8</td> <td>16</td> <td>32</td>
  </tr>
  <tr>
    <th>101</th> <td>5</td> <td>10</td> <td>20</td> <td>40</td>
  </tr>
  <tr>
    <th>110</th> <td>6</td> <td>12</td> <td>24</td> <td>48</td>
  </tr>
  <tr>
    <th>111</th> <td>7</td> <td>14</td> <td>28</td> <td>56</td>
  </tr>
</table>


-   Here's a clearer view of some of the values our scheme can represent:

<figure>
  <figcaption>Number Spacing</figcaption>
  <img id="f:correct-spacing" src="../../files/number-spacing.png" alt="Number Spacing" />
</figure>

-   There are a lot of values we *can't* store
    -   Can do 8 and 10 but not 9
    -   Exactly like the problem writing out 1/3 in decimal: have to round that to 0.3333 or 0.3334
-   But if this scheme has no representation for 9, then 8+1 must be stored as either 8 or 10
-   Which raises an interesting question: if 8+1 is 8, what is 8+1+1?
    -   If we add from the left, 8+1 is 8, plus another 1 is 8 again
    -   If we add from the right, 1+1 is 2, and 2+8 is 10
    -   Changing the order of operations can make the difference between right and wrong
-   This is the sort of thing that numerical analysts spend their time on
    -   In this case, if we sort the values and then add from smallest to largest, it gives us the best chance of getting the best answer
    -   In other situations, like inverting a matrix, the rules are more complicated
    -   Trust the authors of core libraries to get this right (just like electrical engineers trust oscilloscope makers)
-   The absolute spacing between the values we can represent is uneven
    -   But the relative spacing between each set of values stays the same
    -   The first group is separated by 1, then the separation becomes 2, then 4, then 8
    -   This happens because we're multiplying the same fixed set of mantissas by ever-larger exponents
    -   Leads to some useful definitions
-   The [absolute error](#g:absolute-error) in some approximation to a value is the absolute value of the difference between the two
-   The [relative error](#g:relative-error) is the ratio of the absolute error to the value we're approximating
    -   If we are off by 1 in approximating 8+1 and 56+1, that's the same absolute error
    -   But the relative error is larger in the first case than in the second
-   Relative error is almost always more useful than absolute
    -   It makes little sense to say that we're off by a hundredth when the value in question is a billionth
-   What does this have to do with testing?

```python
vals = []
for i in range(1, 10):
    number = 9.0 * 10.0 ** -i
    vals.append(number)
    total = sum(vals)
    expected = 1.0 - (10.0 ** -i)
    diff = total - expected
    print('{:2d} {:22.21f} {:22.21f}'.format(i, total, total-expected))
```

-   Loop runs over the integers from 1 to 9 inclusive
    -   Put the numbers 0.9, 0.09, 0.009, and so on in `vals`
    -   Sum should be 0.9, 0.99, 0.999, and so on, but is it?
-   Calculate the same value a different way, by subtracting .1 from 1, then subtracting .01 from 1, and so on
    -   This should create exactly the same sequence of numbers

<table class="table table-striped">
  <tr> <th>index</th> <th>total</th> <th>difference</th> </tr>
  <tr> <th>1</th> <td>0.900000000000000022204</td> <td>0.000000000000000000000</td> </tr>
  <tr> <th>2</th> <td>0.989999999999999991118</td> <td>0.000000000000000000000</td> </tr>
  <tr> <th>3</th> <td>0.998999999999999999112</td> <td>0.000000000000000000000</td> </tr>
  <tr> <th>4</th> <td>0.999900000000000011013</td> <td>0.000000000000000000000</td> </tr>
  <tr> <th>5</th> <td>0.999990000000000045510</td> <td>0.000000000000000000000</td> </tr>
  <tr> <th>6</th> <td>0.999999000000000082267</td> <td>0.000000000000000111022</td> </tr>
  <tr> <th>7</th> <td>0.999999900000000052636</td> <td>0.000000000000000000000</td> </tr>
  <tr> <th>8</th> <td>0.999999990000000060775</td> <td>0.000000000000000111022</td> </tr>
  <tr> <th>9</th> <td>0.999999999000000028282</td> <td>0.000000000000000000000</td> </tr>
</table>

-   The very first value contributing to our sum is already slightly off
    -   Even with 23 bits for a mantissa, we cannot exactly represent 0.9 in base 2,
        any more than we can exactly represent 1/3 in base 10
    -   Doubling the size of the mantissa would reduce the error, but we can't ever eliminate it
-   The good news is, $$9 {\times} 10^{-1}$$ and $$1 - 0.1$$ are exactly the same
    -   Might not be precisely right, but at least it's consistent
-   But some later values differ
    -   And sometimes accumulated error makes the result *more* accurate
-   Very important to note that *this has nothing to do with randomness*
    -   The same calculation will produce exactly the same results no matter how many times it is run
    -   Process is completely deterministic, just hard to predict
    -   If you see someone run the same code on the same data with the same parameters many times and average the results,
        you should ask if they know what they're doing
    -   It *can* be defensible if there is parallelism (which can change evaluation order),
        but in every other case, it's usually a sign that they don't understand
-   So what does this have to do with testing?
    -   If the function you're testing uses floating point numbers, what do you compare its result to?
    -   If we compared the sum of the first few numbers in `vals` to what it's supposed to be, the answer could be `False`
-   No one has a good generic answer,
    because the root of our problem is that we're using approximations,
    and each approximation has to be judged on its own merits
-   So what can you do to test your programs?
-   Use `pytest.approx` with a relative error rather than an absolute error
    -   It works on lists, sets, arrays, and other collections
-   `approx` can be given either relative or absolute error bounds
    -   To show how it works, set an unrealistically tight absolute bound

```python
from pytest import approx

for bound in (1e-15, 1e-16):
    vals = []
    for i in range(1, 10):
        number = 9.0 * 10.0 ** -i
        vals.append(number)
        total = sum(vals)
        expected = 1.0 - (10.0 ** -i)
        if total != approx(expected, abs=bound):
            print('{:22.21f} {:2d} {:22.21f} {:22.21f}'.format(bound, i, total, expected))
```
```
9.999999999999999790978e-17  6 0.999999000000000082267 0.999998999999999971244
9.999999999999999790978e-17  8 0.999999990000000060775 0.999999989999999949752
```

-   So two tests pass at an absolute error of $$10^{-15}$$ but fail at $$10^{-16}$$
-   Both of these bounds are unreasonably tight
    -   A relative error of $$10^{-3}$$ (three decimal places) is more than good enough for most data science
-   [Accuracy](#g:accuracy) is how close your answer is to right
-   [Precision](#g:precision) is how close repeated measurements are to each other
-   You can be precise without being accurate (systematic bias), or accurate without being precise (near the right answer, but without many significant digits)
-   Accuracy is usually more important than precision
-   Putting explicit bounds in your tests tells people what you have focused on

### Exercises

FIXME: exercises

## Testing Plots {#s:correct-plots}

-   Testing visualizations is hard
    -   Any change to the dimension of the plot, however small, can change many pixels
    -   Trivial changes (such as moving the legend up a couple of pixels) will generate false positives
-   Test the data and data structures going into your plots instead, and trust the plotting library
-   If you really need to test the generated image, there are tools that do this
-   [pytest-mpl][pytest-mpl] compares the latest image against a saved reference verseion
    -   Root mean square (RMS) difference between images must be below a threshold for the comparison to pass
-   It also allows you to turn off comparison of text, because font differences can throw up spurious failures
    -   If images are close enough that a human being would make the same decision about meaning, the test should pass

```
FIXME: example
```
-   The right answer is to test the data structures used to generate the plot and then trust the plotting library
    -   If the right data and parameters are going in, the rest is outside your control anyway

### Exercises

FIXME: exercises

## Testing Simple Inputs {#s:correct-simple}

-   Subsampling
    -   Choose random subsets of input data, do analysis, see how close output is to output with full data set
    -   If output doesn't converge as sample size grows, something is probably unstable
    -   Which is not the same as wrong: it's a problem with the algorithm, rather than with the implementation
-   Test with synthesized data
    -   Uniform data, i.e., same values for all observations
    -   Strictly bimodal data
    -   Data generated from known distribution
-   Example: generate distribution that conforms to Zipf's Law and test analysis
    -   Real data will be integers (since words only occur or not), and distribution is fractional
    -   Use 5% relative error (by experimentation, 1% excludes a valid correct value)

```
import sys
from pytest import approx


RELATIVE_ERROR = 0.05

    
def is_zipf(hist):
    scaled = [h/hist[0] for h in hist]
    print('scaled', scaled)
    perfect = [1/(1 + i) for i in range(len(hist))]
    print('perfect', perfect)
    return scaled == approx(perfect, rel=RELATIVE_ERROR)


def test_fit_correct():
    actual = [round(100 / (1 + i)) for i in range(10)]
    print('actual', actual)
    assert is_zipf(actual)


def test_fit_first_too_small():
    actual = [round(100 / (1 + i)) for i in range(10)]
    actual[0] /= 2
    assert not is_zipf(actual)


def test_fit_last_too_large():
    actual = [round(100 / (1 + i)) for i in range(10)]
    actual[-1] = actual[1]
    assert not is_zipf(actual)
```

## Operational Tests {#s:correct-operational}

-   [Operational tests](#g:operational-test) are ones that are kept in place during production
    -   Is everything working as it should?
-   Common pattern:
    -   Have every tool append information to a log
    -   Have another tool check that log file after the run is over
    -   Simpler to do comparisons between different stages of the pipeline than inserting checks between stages
-   Common tests
    -   Same number of output records as input records
    -   Or fewer output records than input records if you're aggregating
    -   Or the product of the sizes of two tables if you're joining records
    -   Standard deviation has to be smaller than the range of the data
    -   NaNs and NULLs only where you're expecting them and handling them

```python
# text_to_words.py
import sys

num_lines = num_words = 0
for line in sys.stdin:
    num_lines += 1
    words = [strip_punctuation(w) for w in line.strip().split()]
    num_words += len(words)
    for w in words:
        print(w)
with open('logfile.txt', 'a') as logger:
    logger.write('text_to_words.py,num_lines,{}\n'.format(num_lines))
    logger.write('text_to_words.py,num_words,{}\n'.format(num_words))
```

```python
# word_count.py
import sys

num_words = 0
count = {}
for word in sys.stdin:
    num_words += 1
    count[word] = count.get(word, 0) + 1
for word in count:
    print('{} {}', word, count[word])
with open('logfile.txt', 'a') as logger:
    logger.write('word_count.py,num_words,{}\n'.format(num_words))
    logger.write('word_count.py,num_distinct,{}\n'.format(len(count)))
```

```
text_to_words.py,num_lines,431
text_to_words.py,num_words,2554
word_count.py,num_words,2554
word_count.py,num_distinct,1167
```

```python
# check_log.py
data = ...read CSV file...
check(data['text_to_words.py']['num_lines'] <= data['word_count.py']['num_words'])
check(data['text_to_words.py']['num_words'] == data['word_count.py']['num_words'])
check(data['word_count.py']['num_words'] >= data['word_count.py']['num_distinct'])
```

-   Verify data against a distribution
    -   E.g., [Shapiro-Wilk test][shapiro-wilk] that data is normal
    -   Requires a tolerance, but at least you're now making your tolerances specific
-   Alternative: use a non-parametric test
    -   Kolmogorov Smirnov test checks that an empirical distribution fits a ideal distribution
    -   Chi-square test check whether the two distributions are the same or different
    -   t-stat test is good for testing how far out of the mean something is
-   Create histogram of results for test data
    -   Verify that subsequent data fits histogram
    -   Although you still have to decide what "fits" means
    -   And you have to 

```python
TEST_BINS = 100
TEST_TOLERANCE = 1.0e-3

reference = pandas.read_csv('test_reference.csv').iloc[,0]
actual = ...some complex calculation...
check = actual.hist(column=3, bins=TEST_BINS)
assert actual == pytest.approx(reference, rel=TEST_TOLERANCE)
```

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
    -   "Is this dataset similar to the one I tested on?"
-   Especially useful if the constraint file is put under version control

### Exercises

FIXME: exercises

## Summary {#s:correct-summary}

FIXME: create concept map

{% include links.md %}
