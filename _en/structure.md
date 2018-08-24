---
permalink: "/en/structure/"
title: "Project Structure"
questions:
-   "How should I organize the files and directories in my project?"
objectives:
-   "Describe and justify Noble's Rules for organizing projects."
-   "Explain the purpose of README, LICENSE, CONDUCT, and CITATION files."
keypoints:
-   "Put source code for compilation in `src/`, runnable code in `bin/`, raw data in `data/`, results in `results/`, and documentation and manuscripts in `doc/`."
-   "Use file and directory names that are easy to match and include dates for the level under `data/` and `results/`."
-   "Create README, LICENSE, CONDUCT, and CITATION files in the root directory of the project."
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

## What Are Noble's Rules? {#s:structure-noble}

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

### Common Problems

FIXME: common problems for Noble's Rules

### Exercises

FIXME: create exercises for Noble's Rules

## Summary {#s:structure-summary}

FIXME: create concept map for project structure

{% include links.md %}
