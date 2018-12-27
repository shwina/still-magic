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

-   One of the things that distinguishes research programmers is that they're writing code in order to figure out what the right answer is
-   One of the things they struggle with is the transition from exploration to infrastructure
    -   I.e., from "coding to figure out what the problem is" to "I'm building a reusable tool"
    -   Habits from the first are often carried over to the second
-   One possible analogy is game development
    -   Lots of individual developers trying to get something that works well enough to ship
    -   A handful of large, stable organizations doing software engineering to create things like Mario Kart 8
    -   The latter tend to look down on the methods and standards of the former
    -   But the methods and standards of the latter aren't helpful for the former
-   Distinguish between:
    -   Open science: everyone can read it
    -   Reproducible research: people can re-do the analysis
    -   Computational competence: get reliable results without late nights and heartbreak
-   Computational competence requires the programming equivalent of good laboratory skills
    -   Because software is just another kind of lab equipment
-   Reasons not to make your work open
    -   Academia doesn't yet know how to reward it, so your effort may not be rewarded
    -   Fear of looking foolish or harming career isn't just impostor syndrome (particularly for members of marginalized groups)
-   Reasons to do it
    -   Being open is a big step toward a (non-academic) career path, which is where ~80% of Ph.D.s go
    -   Proven benefits: work is cited more often than closed (FIXME: citation)
-   Goal of this training is to produce more (correct) results in less time and with less effort
    -   Stakeholders need to be confident that you did things the right way so that they can be confident in your results (good lab practices)
    -   Need to be able to re-do your analyses (trust, but verify)
    -   You (and others) need to be able to re-use your data, software, and reports instead of constantly rewriting
-   We will cover:
    -   Writing code that is readable, testable, and maintainable
    -   Automating analyses with build tools
    -   Checking and demonstrating correctness via automated tests
    -   Publishing science in the 21st Century
    -   Using a branch-per-feature workflow, rebasing, and tags to manage work
    -   Organizing the code, data, results, and reports in a small or medium-sized project
-   Prerequisites
    -   Python: lists, loops, conditionals, functions, importing and using libraries
    -   Unix shell: paths, editing/renaming/deleting files, wildcards, redirection, pipes and filters, shell scripts
    -   Git: add/commit, log, merge, resolving conflicts, push, pull
    -   The [Software Carpentry][swc] lessons cover these topics

These lessons can be used for self-study by people who plan to enroll in
something like the [Insight Data Science][insight] Fellows Program,
or as part of a one-semester course for graduate students or senior undergraduates.

## Running Example {#s:intro-example}

-   [Zipf's Law][zipfs-law]: frequency of a word is inversely proportional to rank
    -   I.e., second most common word occurs half as often as most common, third most common a third as often, etc.
-   We want to test books against this distribution

## What Does 'Done' Look Like? {#s:intro-done}

1.  Analysts are reasonably confident that results are correct.
    -   Not the same as "absolutely sure".
    -   As trustworthy as lab experiments or careful manual analysis.
2.  Software can be used by people other than original authors without heroic effort.
    -   I.e., people other than the authors can figure it out and use it in less time than it would take to write their own.
3.  Small changes and extensions are easy.
    -   So that the software can be re-used as problems and questions evolve.

## Sources {#s:intro-sources}

-   "A Quick Guide to Organizing Computational Biology Projects" [Nobl2009](#BIB)
-   "Ten Simple Rules for Making Research Software More Robust" [Tasc2017](#BIB)
-   "Best Practices for Scientific Computing" [Wils2014](#BIB)
-   "Good Enough Practices in Scientific Computing" [Wils2017](#BIB)
-   *Teaching Tech Together* [Wils2018](#BIB)

## Contributing {#s:intro-contrib}

Contributions of all kinds are welcome, from errata and minor
improvements to entirely new sections and chapters. All proposed
contributions will be managed in the same way as edits to Wikipedia or
patches to open source software, and all contributors will be credited
for their work each time a new version is released.  please file an
issue in our [GitHub repository][config-repo] or [email the author
directly][config-email].  Please note that all contributors
are required to abide by our code of conduct ((s:conduct)[#APPENDIX]).

{% include links.md %}
