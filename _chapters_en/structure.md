---
permalink: "/en/structure/"
title: "Projects and Packages"
questions:
-   FIXME
objectives:
-   FIXME
keypoints:
-   FIXME
---

FIXME
-   Project organization is like a diet
    -   There is no such thing as "no diet", just a good one or a bad one
    -   Similarly, there is no such thing as "no project organization"
    -   Your project is either organized *well* or organized *poorly*
-   Small pieces in predictable places are easier to recombine than large chunks that have to be re-read
-   Organizing software into installable packages is more than just convention
    -   Certain things have to be in certain places in order for Python to find them
-   Using [virtual environments](#g:virtual-environment) allows you to work on many projects at once without tripping over yourself
    -   Slowly being superceded by more general solutions like [Docker][docker], but still the easiest solution for most of us

## Noble's Rules {#g:structure-noble}

-   From [[Nobl2009](#CITE)]
-   Top level is logical, next level is chronological
    -   Source code in `src/` (short for "source")
        -   Shell scripts and Python or R programs go here
        -   Source for C/C++ and the like go here
    -   Compiled programs in `bin/` (short for "binary", meaning "not text")
        -   Executables for C/C++ programs go here
        -   Usually *isn't* put under version control (since they can be rebuilt)
    -   Raw data in `data/`
        -   If it's too large, use `data/` to store data references
    -   Results in `results/`
    -   Documentation and manuscripts in `doc/`
-   Directory names under `data/` and `results/` are `YYYY-MM-DD` so that they can be sorted chronologically
-   Filenames should be easy to match consistently with shell wildcards
    -   E.g., `species-organ-treatment.csv`, like `human-kidney-cm200.csv`
    -   Allows `human-*-cm200.csv` to match all human organs, or `*-kidney-*.csv` to match all kidney data
    -   Don't worry about long directory names: [tab completion](#g:tab-completion) means you only have to type them once

FIXME: diagram

-   A few files Noble didn't mention that have become conventional
    -   `README`: one-paragraph description of the project
    -   `LICENSE`: the project's license
    -   `CONDUCT`: its code of conduct
    -   `CITATION`: how the work should be cited
        -  May have a separate `CONTRIBUTORS` file, or list contributors in `CITATION`
    -   These files may be plain text or Markdown, or have no suffix at all, but please use the principal names as given

## Virtual Environments {#s:structure-virtualenv}

FIXME
-   How Python finds packages
-   How `virtualenv` changes the search order
-   How to create, update, and change virtual environments

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

{% include links.md %}
