---
permalink: "/en/continuous/"
title: "Continuous Integration"
questions:
-   "How can I tell what state my project is actually in?"
objectives:
-   "Explain how continuous integration works."
-   "Configure continuous integration for a small software project."
keypoints:
-   "Continuous integration rebuilds and/or re-tests software every time something changes."
-   "Use continuous integration to check changes before they are inspected."
-   "Check style as well as correctness."
---

-   [Continuous integration](#g:continuous-integration)
    -   Build and test code and documentation every time someone commits code
    -   Post results somewhere the team can see them
    -   If build or tests fail, send out notifications
-   Even better: build and test changes *before* they're merged
    -   Only do code review on changes that have passed mechanical checks
-   Most widely used system is [Travis CI][travis-ci]
    -   Easy integration with [Github][github]
    -   Will run tests on multiple platforms and with multiple versions of tools
-   Developers still have to build the tests
    -   CI only as good as the tests it runs
-   Check style as well as correctness by running [pep8][pep-8] or [formatR][format-r] as part of the build

### Exercises

#### Setting Up Continuous Integration

Follow the steps in [this tutorial][python-travis-tutorial] to set up Travis-CI testing for the example repository.

1.  How long did it take you to get it working?
2.  What could have been added to the documentation to make your life easier?

## Summary {#s:continuous-summary}

FIXME: create concept map

{% include links.md %}
