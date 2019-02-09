-   Create histogram of results for test data
    -   Verify that subsequent data fits histogram
    -   Although you still have to decide what "fits" means
    -   And you have to 
-   Verify data against a distribution
    -   E.g., [Shapiro-Wilk test][shapiro-wilk] that data is normal
    -   Requires a tolerance, but again, that's good because it forces you to make your tolerances explicit
-   Alternative: use a non-parametric test
    -   Kolmogorov Smirnov test checks that an empirical distribution fits a ideal distribution
    -   Chi-square test check whether the two distributions are the same or different
    -   t-stat test is good for testing how far out of the mean something is

```python
TEST_BINS = 100
TEST_TOLERANCE = 1.0e-3

reference = pandas.read_csv('test_reference.csv').iloc[,0]
actual = ...some complex calculation...
check = actual.hist(column=3, bins=TEST_BINS)
assert actual == pytest.approx(reference, rel=TEST_TOLERANCE)
```

[shapiro-wilk]: https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test
