---
permalink: "/en/intro/"
title: "Introduction"
questions:
-   "What is computational competence?"
-   "What is the scope of this training?"
objectives:
-   "Explain the difference between open science, reproducible research, and computational competence."
-   "Determine readiness for using this material."
keypoints:
-   FIXME
---

-   Distinguish between:
    -   Open science: everyone can read it
    -   Reproducible research: people can re-do the analysis
    -   Computational competence: get reliable results without late nights and heartbreak
-   Computational competence requires the programming equivalent of good laboratory skills
    -   Because software is just another kind of lab equipment
-   Goals of this training:
    -   Other people (including our future selves) can re-do analyses
    -   All stakeholders can be confident in the results
    -   Re-using software is cheaper than rewriting it
    -   In short, the coding equivalent of [tidy data](#g:tidy-data) [[Wick2014](#CITE)]
-   We will cover:
    -   Writing code that is readable, testable, and maintainable ([s:style](#CHAPTER))
    -   Building software tools that play nicely with others ([s:tools](#CHAPTER))
    -   Managing libraries in a reproducible way ([s:libs](#CHAPTER))
    -   Organizing the code, data, results, and reports in a small or medium-sized project ([s:project](#CHAPTER))
    -   Automating analyses with build tools ([s:automate](#CHAPTER))
    -   Building reusable software with classes and higher-order functions ([s:reuse](#CHAPTER))
    -   Checking and demonstrating correctness via automated tests ([s:correct](#CHAPTER))
    -   Using a branch-per-feature workflow, rebasing, and tags to manage work ([s:workflow](#CHAPTER))
-   Prerequisites
    -   Python: lists, loops, conditionals, functions, importing and using libraries
    -   Unix shell: paths, editing/renaming/deleting files, wildcards, redirection, pipes and filters, shell scripts
    -   Git: add/commit, log, merge, resolving conflicts, push, pull
    -   The [Software Carpentry][swc] lessons cover these topics

These lessons can be used for self-study by people who plan to enroll in
something like the [Insight Data Science][insight] Fellows Program,
or as part of a one-semester course for graduate students or senior undergraduates
who are already comfortable writing two-page programs in Python using lists, functions, and libraries.

## What Does 'Done' Look Like?

1.  Analysts are reasonably confident that results are correct.
    -   Not the same as "absolutely sure".
    -   As trustworthy as lab experiments or careful manual analysis.
2.  Software can be used by people other than original authors without heroic effort.
    -   I.e., people other than the authors can figure it out and use it in less time than it would take to write their own.
3.  Small changes and extensions are easy.
    -   So that the software can be re-used as problems and questions evolve.

## Sources

-   "A Quick Guide to Organizing Computational Biology Projects" [[Nobl2009](#CITE)]
-   "Ten Simple Rules for Making Research Software More Robust" [[Tasc2017](#CITE)]
-   "Best Practices for Scientific Computing" [[Wils2014](#CITE)]
-   "Good Enough Practices in Scientific Computing" [[Wils2017](#CITE)]
-   *Teaching Tech Together* [[Wils2018](#CITE)]

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
