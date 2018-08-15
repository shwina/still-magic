---
permalink: "/en/structure/"
title: "Projects and Packages"
questions:
-   "How should I organize the files and directories in my project?"
-   "Why should my project have an explicit Code of Conduct?"
-   "How can I manage the libraries my project relies on?"
-   "How can I package up my work for others to use?"
objectives:
-   "Describe and justify Noble's Rules for organizing projects."
-   "Explain the purpose of README, LICENSE, CONDUCT, and CITATION files."
-   "Explain the purpose of a Code of Conduct and the essential features an effective one must have."
-   "Create and use virtual environments to manage library versions without conflict."
-   "Create and test a citable, shareable Pip package."
keypoints:
-   "Put source code for compilation in `src/`, runnable code in `bin/`, raw data in `data/`, results in `results/`, and documentation and manuscripts in `doc/`."
-   "Use file and directory names that are easy to match and include dates for the level under `data/` and `results/`."
-   "Create README, LICENSE, CONDUCT, and CITATION files in the root directory of the project."
-   "Create an explicit Code of Conduct for your project modelled on the Contributor Covenant."
-   "Be clear about how to report violations of the Code of Conduct and who will handle such reports."
-   "Use `virtualenv` to create a separate virtual environment for each project."
-   "Use `pip` to create a distributable package containing your project's software, documentation, and data."
-   "Use Zenodo to give your releases DOIs."
-   "Publish your software as you would a paper."
---

-   Project organization is like a diet
    -   There is no such thing as "no diet", just a good one or a bad one
    -   Similarly, there is no such thing as "no project organization"
    -   Your project is either organized *well* or organized *poorly*
-   Small pieces in predictable places are easier to recombine than large chunks that have to be re-read
-   Organizing software into installable packages is more than just convention
    -   Certain things have to be in certain places in order for Python to find them
-   Using [virtual environments](#g:virtual-environment) allows you to work on many projects at once without tripping over yourself
    -   Slowly being superceded by more general solutions like [Docker][docker], but still the easiest solution for most of us

### Exercises

FIXME

## Noble's Rules {#s:structure-noble}

-   From [[Nobl2009](#CITE)]
-   Top level is logical, next level is chronological
    -   Source code in `src/` (short for "source")
        -   Source for C/C++ and the like go here
    -   Compiled programs in `bin/` (short for "binary", meaning "not text")
        -   Executables for C/C++ programs go here (but not under version control)
        -   Shell scripts and Python or R programs go here (but under version control, which can be confusing)
    -   Raw data in `data/`
        -   If it's too large, use `data/` to store data references
    -   Results in `results/`
    -   Documentation and manuscripts in `doc/`
-   Directory names under `data/` and `results/` are `YYYY-MM-DD` so that they can be sorted chronologically
-   Filenames should be easy to match consistently with shell wildcards
    -   E.g., `species-organ-treatment.csv`, like `human-kidney-cm200.csv`
    -   Allows `human-*-cm200.csv` to match all human organs, or `*-kidney-*.csv` to match all kidney data
    -   Don't worry about long directory names: [tab completion](#g:tab-completion) means you only have to type them once

<figure>
  <figcaption>Project Layout</figcaption>
  <img id="f:structure-layout" src="../../files/noble.svg" alt="Project Layout" />
</figure>

-   A few files Noble didn't mention that have become conventional
    -   `README`: one-paragraph description of the project
    -   `LICENSE`: the project's license
    -   `CONDUCT`: its code of conduct (discussed below)
    -   `CITATION`: how the work should be cited
        -  May have a separate `CONTRIBUTORS` file, or list contributors in `CITATION`
    -   These files may be plain text or Markdown, or have no suffix at all, but please use the principal names as given

### Exercises

FIXME

## Code of Conduct {#s:structure-conduct}

A CoC lays out the expectations for interpersonal interaction in your project.
The CoC that we suggest using is the [Contributor Covenant][covenant],
which provides examples of acceptable and unacceptable behavior for your project,
and specifies how unacceptable behavior will be handled.
The goal of this is to explicitly communicate the standards of interaction to which this project holds its participants,
and encourage newcomers to the project to engage with the project.

This serves several purposes:

-   It reduces the uncertainty that project participants face about what is acceptable and unacceptable behavior.
    While you might think this is obvious,
    long experience suggests that articulating it clearly and concisely reduces problems caused by have different expectations.

-   It welcomes newcomers specifically, which can help grow your project and encourage user feedback.

-   It delineates responsibilities within the project and provides specific points of contact in case of misconduct or harassment,
    as well as specifying the process to be followed in these cases.

We find that most people agree with the standards laid out in the Contributor Covenant,
and believe that posting it entails no disadvantage.

-   Important to make clear:
    -   How to report
    -   Who handles

### Exercises

FIXME

## Virtual Environments {#s:structure-virtualenv}

FIXME
-   How Python finds packages
-   How `virtualenv` changes the search order
-   How to create, update, and change virtual environments

### Exercises

FIXME

## Creating Packages {#s:structure-package}

FIXME
-   What a package needs to have to be installable
-   The confusion of Python packaging solutions
-   Structure of a Pip package
-   Commands to create a package
-   How to test that a package installs correctly
    -   Hint: `virtualenv`
-   How to make the package available
    -   On PyPI
    -   From GitHub

### Exercises

FIXME

## Publishing Packages {#s:structure-publish}

FIXME
-   Connect GitHub to [Zenodo][zenodo] to create [citable code][citable-code]
    -   Create a release
    -   Tag it
    -   Create a DOI
-   Publish in [JOSS][joss] or [F1000 Research][f1000-research]

### Exercises

FIXME

## Summary {#s:structure-summary}

FIXME: create concept map

{% include links.md %}
