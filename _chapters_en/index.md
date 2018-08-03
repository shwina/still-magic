---
permalink: "/en/"
root: true
redirect_from: "/"
---

> *It's still magic even if you know how it's done.*
>
> -- Terry Pratchett

## Who Are These Lessons For?

**Samira** completed a Master's in epidemiology five years ago, and
has worked since then for a small NGO.  She did a biostatistics course
during her degree, and has learned some more about R and Python by
doing a couple of online data science courses on her own, but has no
formal training in programming.

Samira would like to tidy up the scripts, data sets, and reports she
has created over the past few years in order to share them with two
junior staff the NGO has just hired.  These lessons will show her what
her first steps should be and what "done" looks like.

**Jun** completed an Insight Data Science fellowship last year, and
now works for a company that does forensic audits.  He has used a wide
variety of machine learning and visualization software, and has
collaborated on a couple of open source R packages.

Jun is supposed to spend 10% of his time on community projects, and
has decided to help review research papers for a forensic accounting
journal.  This course will show him what a mature data science project
should look like so that he can evaluate the papers he is sent.  It
will also show him what improvements his firm's clients should make to
their internal analysis pipelines.

## Brainstorming

1.  What questions will this course answer?
    -   How can I write code that is readable, testable, and maintainable?
    -   How can I build software tools that play nicely with others?
    -   How can I manage packages and libraries in a reproducible way?
    -   How should I organize the code, data, results, and reports in a small or medium-sized project?
    -   How can I automate my analyses to make them reproducible?
    -   How can I make it easier to re-use the software I build?
    -   How can I check and demonstrate the correctness of my analyses?
    -   What version control workflow should I use when collaborating with others?
1.  What concepts and techniques will learners meet?
    -   Follow the naming conventions of your chosen language.
    -   Use style checking tools to ensure consistent naming and structure.
    -   Divide code into functions with no more than half a dozen parameters and no more than three levels of control flow.
    -   Embed documentation in code.
    -   Use standard libraries to parse command-line arguments idiomatically.
    -   Follow the Unix stdin/stdout conventions for file handling.
    -   Eliminate fixed paths in software.
    -   Use command-line parameters for commonly-changed options and configuration files for everything else.
    -   Have all programs, however small, print a short usage message.
    -   Use a logging framework to report activity.
    -   Always install software using a package manager.
    -   Use virtual environments to avoid conflicts between projects.
    -   Separate code, raw data, processed data, and reports, and use matchable names for directories and files.
    -   Use a build tool with pattern rules to make analyses reproducible.
    -   Use higher-order functions and classes to create reusable abstractions and frameworks.
    -   Use a documentation generator to extract and format embedded documentation.
    -   Use a unit testing harness to run and manage tests.
    -   Use a coverage tool to identify unused or untested code.
    -   Use dynamic loading to isolate testable components.
    -   Use CC-0 for data, CC-BY for reports, and the MIT License for code.
    -   Produce identical results when given identical inputs.
    -   Use a branch-per-feature/merge-to-master workflow.
    -   Rebase to consolidate work.
    -   Use tags and semantic versioning to identify production versions of software.
1.  What technologies will learners use?
    -    `pep8` for checking style.
    -    `coverage.py` for code coverage.
    -    `make` for build automation.
    -    `pydoc` for documentation generation.
    -    `getopt` for parsing command-line arguments.
    -    `virtualenv` for environment management.
    -    `conda` for package installation.
    -    `yaml` for configuration files.
    -    `logging` for logging.
    -    Noble's Rules for project organization [[Nobl2009](#CITE)].
    -    Taschuk's Rules for robust software [[Tasc2017](#CITE)].
    -    `unittest` for unit testing.
    -    `importlib` for dynamic loading.
    -    `git rebase -i` to consolidate work.
    -    `git tag` to tag releases.
1.  What do learners already need to know?
    -   Python: lists, loops, conditionals, functions, importing and using libraries
    -   Unix shell: paths, editing/renaming/deleting files, wildcards, redirection, pipes and filters, shell scripts
    -   Git: add/commit, log, merge, resolving conflicts, push, pull
    -   Note that the core [Software Carpentry][swc] lessons cover these topics
1.  What *won't* be covered?
    -   Statistics: not the focus of this course.
    -   Data management (beyond the four key characteristics of [tidy data](#g:tidy-data)).
    -   Building `conda` packages: basic ideas are illustrated by `pip`.
    -   Performance profiling: useful but not crucial (will be briefly mentioned when discussing coverage).
    -   Parallelism: see above.
    -   Hosting options other than GitHub: mention in passing.
    -   Code reviews: hard to teach without direct contact (and in practice, most people at this level won't do them)
    -   Object-oriented design patterns: too advanced for this material.
    -   Relational or non-relational databases: not core to program design and construction.
    -   Continuous integration: a useful next step, but manual runs are good enough at this level
    -   Scrum: a useful next step, but out of scope for this audience.
    -   Test-driven development: will be mentioned when talking about testing, but the evidence doesn't support its effectiveness.
    -   Recruiting, mentoring, and community building: out of scope.
    -   Marketing: out of scope.

## Key Exercises

FIXME

## Lesson Plan

We budget two hours for each of these topics, divided evenly between instruction, worked examples, and exercises.
It should therefore be possible to cover everything in an intensive two-day workshop.

1.  Writing code that is readable, testable, and maintainable ([s:style](#CHAPTER)).
1.  Building software tools that play nicely with others ([s:tools](#CHAPTER)).
1.  Managing libraries in a reproducible way ([s:libs](#CHAPTER)).
1.  Organizing the code, data, results, and reports in a small or medium-sized project ([s:project](#CHAPTER)).
1.  Automating analyses with build tools ([s:automate](#CHAPTER)).
1.  Building reusable software with classes and higher-order functions ([s:reuse](#CHAPTER)).
1.  Checking and demonstrating correctness via automated tests ([s:correct](#CHAPTER)).
1.  Using a branch-per-feature workflow, rebasing, and tags to manage work ([s:workflow](#CHAPTER)).

## Summary

For researchers and data scientists who have a basic understanding of the Unix shell, Python, and Git,
and who want to be more productive and have more confidence in their results,
this training course
provides a pragmatic, tools-based introduction to program design and maintenance.
Unlike academic software engineering courses and most books aimed at professional software developers,
this course uses data analysis as a motivating example
and assumes that the learner's ultimate goal is to answer a question rather than ship an application.

Learners must be comfortable with the basics of the Unix shell, Python, and Git
at the level covered by the core [Software Carpentry][swc] lessons.
They will need a personal computer with Internet access,
the Bash shell,
Python 3,
and a GitHub account.

{% include links.md %}
