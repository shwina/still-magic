---
permalink: "/en/design/"
title: "Design Notes"
---

## Brainstorming

1.  What questions will this course answer?
    -   How can I write code that is readable, testable, and maintainable?
    -   How should I organize and share my software, data, and results?
    -   How can I make my work more efficient and reproducible?
    -   How can I check and demonstrate that my work is correct?
    -   How should I publish my work in the early 21st Century?
    -   How can I make it easy for other people to collaborate with me?
1.  What concepts and techniques will learners meet?
    -   Use a build tool with pattern rules to make analyses reproducible.
    -   Use a unit testing harness to run and manage tests.
    -   Use a coverage tool to identify unused or untested code.
    -   Use stubs and mocks to isolate hard-to-test components.
    -   Produce identical results when given identical inputs.
    -   Define tolerances for production runs of data analysis pipelines.
    -   Use a logging framework to report activity.
    -   Use command-line parameters and configuration files to control program behavior.
    -   Use standard libraries to parse command-line arguments idiomatically.
    -   Have all programs, however small, print a short usage message.
    -   Use Markdown and GitHub Pages to publish documentation and reports.
    -   Use a branch-per-feature workflow to manage work.
    -   Rebase to consolidate work.
    -   Use tags and semantic versioning to identify production versions of software.
    -   Configure continuous integration to tell you what state your project is in.
    -   Follow the naming conventions of your chosen language.
    -   Use style checking tools to ensure consistent naming and structure.
    -   Apply standard refactorings to clean up code as needs evolve.
    -   Separate code, raw data, processed data, and reports.
    -   Use meaningful, matchable names for directories and files.
    -   Use CC-0 for data, CC-BY for reports, and the MIT License for code.
    -   Adopt a code of conduct for your project to clarify expectations and standards.
    -   Be a proactive ally for members of marginalized or targeted groups.
    -   Always install software using a package manager.
    -   Use virtual environments to avoid conflicts between projects.
    -   Embed the documentation for software in the software itself.
    -   Use a documentation generator to extract and format embedded documentation.
1.  What technologies will learners use?
    -   `make` for build automation.
    -   `pytest` for unit testing.
    -   `StringIO` for testing text streams.
    -   `coverage` for coverage analysis.
    -   `tdda` for constraint inference and checking.
    -   `logging` for logging.
    -   `yaml` for configuration files.
    -   `getopt` for parsing command-line arguments.
    -   Markdown for authoring.
    -   Jekyll for generating websites.
    -   `git rebase -i` to consolidate work.
    -   `git tag` to tag releases.
    -   Travis-CI for continuous integration.
    -   `pep8` for checking style.
    -   Noble's Rules for project organization [[Nobl2009](#CITE)].
    -   Taschuk's Rules for robust software [[Tasc2017](#CITE)].
    -   Creative Commons and MIT licenses for data, reports, and software.
    -   The Contributor Covenant as a code of conduct.
    -   `pip` for package creationg and installation.
    -   `virtualenv` for environment management.
    -   `pydoc` for documentation generation.
1.  What do learners already need to know?
    -   Python: lists, loops, conditionals, functions, importing and using libraries
    -   Unix shell: paths, editing/renaming/deleting files, wildcards, redirection, pipes and filters, shell scripts
    -   Git: add/commit, log, merge, resolving conflicts, push, pull
    -   The core [Software Carpentry][swc] lessons cover these topics, as does the [prerequisite course][one-extra-thing] in this series
1.  What *won't* be covered?
    -   Statistics: not the focus of this course.
    -   Higher-order functions and object-oriented programming: higher-level programming isn't the focus of this material.
    -   Building `conda` packages: basic ideas are illustrated by `pip`.
    -   Performance profiling: useful but not crucial (will be briefly mentioned when discussing coverage).
    -   Parallelism: out of scope for most learners at this level (and very dependent on local setup).
    -   Hosting options other than GitHub: mention in passing.
    -   Code reviews: hard to teach without direct contact (and in practice, most people at this level won't do them)
    -   Relational or non-relational databases: not core to program design and construction.
    -   Scrum: out of scope for this audience (and not something most will be able to follow in practice).
    -   Test-driven development: will be mentioned when talking about testing, but the evidence doesn't support its effectiveness.
    -   Recruiting, mentoring, marketing, and community building: out of scope.

## Exercises

-   Use [Zipf's Law][zipfs-law] as a running example
    -   Do individual works by different authors obey this rule?
    -   Do aggregate texts?
-   Simple to understand, but the software, data, and results aren't one-liners

## Lesson Plan

{% include summary.html which="questions" language=page.language h="p" %}

{% include links.md %}
