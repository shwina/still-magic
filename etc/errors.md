---
title: "Handling Errors"
undone: true
questions:
-   "How should I handle errors in my code?"
objectives:
-   "FIXME"
keypoints:
-   "FIXME"
---

Things go wrong.
We can test our software to try to prevent problems ([s:unit](#REF) and [s:verify](#REF))
and report the ones that occur despite our best efforts ([s:logging](#REF)),
but in between those two steps we need to detect and handle errors.
This lesson will look at what it's practical to do.

----------------------------------------

-   Handle the most specific exception you can
-   Either log it or catch and re-throw, but don't do both (avoid cluttering the log)
-   Log enough data to track down the problem: there's no point telling me "File Not Found" if you don't tell me *which* file.
-   If you return a default (e.g., couldn't find configuration file, using default settings) tell users, and confirm before proceeding.
-   For things like null pointers, assume that state is too corrupt to be recoverable: log and fail.

-   Example from Nick Radcliffe: the message below isn't helpful because it doesn't tell us which of the four tests failed:

```python
if (val is not None and minVal < val < maxVal and val % 2 = 0 and val >= prevVal):
    # OK branch
else:
    raise Exception('Bad value: {}'.format(val))
```

-   Use `finally`.
-   Sometimes worth retrying (e.g., web pages) but this quickly gets into the weeds.

-   Example: expect 2D filter, given 1D, can spread, but have to choose how: use an exception or test beforehand?

-   LBYL vs EAFP: <https://blogs.msdn.microsoft.com/pythonengineering/2016/06/29/idiomatic-python-eafp-versus-lbyl/>

-   Cleanup is the hard part, so tutorial should provide examples of how to structure code so that cleanup is straightforward.

## Summary {#s:errors-summary}

FIXME: create concept map for error handling

## Exercises {#s:errors-exercises}

FIXME: create exercises for error handling

{% include links.md %}
