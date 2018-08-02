---
permalink: "/en/intro/"
title: "Introduction"
questions:
-   "What is tidy code?"
-   "What is the scope of this training?"
objectives:
-   "Explain the difference between open science, reproducible research, and computational competence."
-   "Determine readiness for using this material."
keypoints:
-   FIXME
---

-   Research doesn't necessarily mean "academic"
    -   Most data scientists are doing research
    -   Act on findings instead of publishing them
-   Researchers of all kinds need the equivalent of good laboratory skills for computing
    -   Because software is just another kind of lab equipment
-   Goals of this training:
    -   Other people (including our future selves) can re-do analyses
    -   All stakeholders can be confident in the results
    -   Re-using software is cheaper than rewriting it
-   We will cover:
    -   Writing code that is readable, testable, and maintainable (and why those are all actually the same thing)
    -   Building software tools that play nicely with others
    -   Managing libraries in a reproducible way
    -   Organizing the code, data, results, and reports in a small or medium-sized project
    -   Automating analyses with build tools
    -   Using classes and/or higher-order functions to create reusable software
    -   Checking and demonstrating correctness via automated tests
    -   Maintaining code quality using checking tools
    -   Using a branch-per-feature workflow, rebasing, and tags to manage work
-   Prerequisites
    -   Python: lists, loops, conditionals, functions, importing and using libraries
    -   Unix shell: paths, editing/renaming/deleting files, wildcards, redirection, pipes and filters, shell scripts
    -   Git: add/commit, log, merge, resolving conflicts, push, pull
    -   The [Software Carpentry][swc] lessons cover these topics

These lessons can be used for self-study by people who plan to enroll in
something like the [Insight Data Science][insight] Fellows Program,
or as part of a one-semester course for graduate students or senior undergraduates
who are already comfortable writing two-page programs in Python using lists, functions, and libraries.

## Sources

-   "Best Practices for Scientific Computing" [[Wils2014](#CITE)]
-   "Good Enough Practices in Scientific Computing" [[Wils2017](#CITE)]
-   "Ten Simple Rules for Making Research Software More Robust" [[Tasc2017](#CITE)]

## Contributing

Contributions of all kinds are welcome, from errata and minor
improvements to entirely new sections and chapters. All proposed
contributions will be managed in the same way as edits to Wikipedia or
patches to open source software, and all contributors will be credited
for their work each time a new version is released.  please file an
issue in our [GitHub repository]({{site.repo}}) or [email the author
directly](mailto:{{site.email}}).  Please note that all contributors
are required to abide by our code of conduct ((s:joining)[#APPENDIX]).

{% include links.md %}
