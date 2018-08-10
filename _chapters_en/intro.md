---
permalink: "/en/intro/"
title: "Introduction"
questions:
-   "What is the difference between open, reproducible, and competent?"
-   "What is the scope of this training?"
-   "What are the prerequisites for this training?"
objectives:
-   "Explain the difference between open science, reproducible research, and computational competence."
-   "Determine readiness for using this material."
-   "Explain what 'done' looks like for the computational component of a small or medium-sized research project."
-   "Determine whether a particular research project meets that standard."
keypoints:
-   "Research is 'open' if everyone can read it, 'reproducible' if people who have access can regenerate it, and 'competent' if it was built in reasonable time and without heroic effort."
-   "Computational competence is the digital equivalent of knowing how to use lab equipment properly."
-   "A project is 'done' when stakeholders can be reasonably sure the results are correct and the software can be understood, run, and extended by people other than the original authors without heroic effort."
---

-   Distinguish between:
    -   Open science: everyone can read it
    -   Reproducible research: people can re-do the analysis
    -   Computational competence: get reliable results without late nights and heartbreak
-   Computational competence requires the programming equivalent of good laboratory skills
    -   Because software is just another kind of lab equipment
-   Why would you want to make your work open source?
    -   Academia doesn't yet know how to reward it
    -   Fear of looking foolish or harming career isn't just impostor syndrome
    -   But things *are* improving
    -   Being open is a big step toward a (non-academic) career path, which is where ~80% of Ph.D.s go
-   Goals of this training:
    -   Other people (including our future selves) can re-do analyses
    -   All stakeholders can be confident in the results
    -   Re-using software is cheaper than rewriting it
    -   In short, the coding equivalent of [tidy data](#g:tidy-data) [[Wick2014](#CITE)]
-   We will cover:
    -   Writing code that is readable, testable, and maintainable ([s:style](#CHAPTER))
    -   Building software tools that play nicely with others ([s:tools](#CHAPTER))
    -   Automating analyses with build tools ([s:automate](#CHAPTER))
    -   Checking and demonstrating correctness via automated tests ([s:correct](#CHAPTER))
    -   Using a branch-per-feature workflow, rebasing, and tags to manage work ([s:workflow](#CHAPTER))
    -   Organizing the code, data, results, and reports in a small or medium-sized project ([s:structure](#CHAPTER))
    -   Building reusable software with classes and higher-order functions ([s:reuse](#CHAPTER))
-   Prerequisites
    -   Python: lists, loops, conditionals, functions, importing and using libraries
    -   Unix shell: paths, editing/renaming/deleting files, wildcards, redirection, pipes and filters, shell scripts
    -   Git: add/commit, log, merge, resolving conflicts, push, pull
    -   The [Software Carpentry][swc] lessons cover these topics

These lessons can be used for self-study by people who plan to enroll in
something like the [Insight Data Science][insight] Fellows Program,
or as part of a one-semester course for graduate students or senior undergraduates
who are already comfortable writing two-page programs in Python using lists, functions, and libraries.

## What Does 'Done' Look Like? {#s:intro-done}

1.  Analysts are reasonably confident that results are correct.
    -   Not the same as "absolutely sure".
    -   As trustworthy as lab experiments or careful manual analysis.
2.  Software can be used by people other than original authors without heroic effort.
    -   I.e., people other than the authors can figure it out and use it in less time than it would take to write their own.
3.  Small changes and extensions are easy.
    -   So that the software can be re-used as problems and questions evolve.

## Sources {#s:intro-sources}

-   "A Quick Guide to Organizing Computational Biology Projects" [[Nobl2009](#CITE)]
-   "Ten Simple Rules for Making Research Software More Robust" [[Tasc2017](#CITE)]
-   "Best Practices for Scientific Computing" [[Wils2014](#CITE)]
-   "Good Enough Practices in Scientific Computing" [[Wils2017](#CITE)]
-   *Teaching Tech Together* [[Wils2018](#CITE)]

## Contributing {#s:intro-contrib}

Contributions of all kinds are welcome, from errata and minor
improvements to entirely new sections and chapters. All proposed
contributions will be managed in the same way as edits to Wikipedia or
patches to open source software, and all contributors will be credited
for their work each time a new version is released.  please file an
issue in our [GitHub repository]({{site.repo}}) or [email the author
directly](mailto:{{site.email}}).  Please note that all contributors
are required to abide by our code of conduct ((s:joining)[#APPENDIX]).

## Exercises {#s:intro-exercises}

FIXME

{% include links.md %}
