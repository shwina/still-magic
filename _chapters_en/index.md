---
permalink: "/en/"
root: true
redirect_from: "/"
---

> It's still magic even if you know how it's done.
>
> -- Terry Pratchett

As research becomes more computing intensive,
researchers need more computing skills.
Being able to write code and use version control is a start;
the goal of this training is to help you take your next steps
so that:

-   other people (including your future self) can re-do your analyses,
-   you and the people using your results can be confident that they're correct,
-   and re-using your software is easier than rewriting it.

These lessons are based on:

-   "A Quick Guide to Organizing Computational Biology Projects" [[Nobl2009](#CITE)]
-   "Ten Simple Rules for Making Research Software More Robust" [[Tasc2017](#CITE)]
-   "Best Practices for Scientific Computing" [[Wils2014](#CITE)]
-   "Good Enough Practices in Scientific Computing" [[Wils2017](#CITE)]
-   The [Software Carpentry][swc] and [Data Carpentry][dc] lessons

For notes on how these lessons were designed, please see [[Wils2018](#CITE)].

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
    -   Use a build tool with pattern rules to make analyses reproducible.
    -   Use a unit testing harness to run and manage tests.
    -   Use a coverage tool to identify unused or untested code.
    -   Use stubs and mocks to isolate hard-to-test components.
    -   Produce identical results when given identical inputs.
    -   Use a branch-per-feature/merge-to-master workflow.
    -   Rebase to consolidate work.
    -   Use tags and semantic versioning to identify production versions of software.
    -   Separate code, raw data, processed data, and reports, and use matchable names for directories and files.
    -   Use CC-0 for data, CC-BY for reports, and the MIT License for code.
    -   Use a documentation generator to extract and format embedded documentation.
    -   Use higher-order functions to create reusable abstractions and frameworks.
1.  What technologies will learners use?
    -   `pep8` for checking style.
    -   `coverage.py` for code coverage.
    -   `make` for build automation.
    -   `pydoc` for documentation generation.
    -   `getopt` for parsing command-line arguments.
    -   `virtualenv` for environment management.
    -   `conda` for package installation.
    -   `yaml` for configuration files.
    -   `logging` for logging.
    -   Noble's Rules for project organization [[Nobl2009](#CITE)].
    -   Taschuk's Rules for robust software [[Tasc2017](#CITE)].
    -   `unittest` for unit testing.
    -   `StringIO` for testing text streams.
    -   `git rebase -i` to consolidate work.
    -   `git tag` to tag releases.
1.  What do learners already need to know?
    -   Python: lists, loops, conditionals, functions, importing and using libraries
    -   Unix shell: paths, editing/renaming/deleting files, wildcards, redirection, pipes and filters, shell scripts
    -   Git: add/commit, log, merge, resolving conflicts, push, pull
    -   Note that the core [Software Carpentry][swc] lessons cover these topics
1.  What *won't* be covered?
    -   Statistics: not the focus of this course.
    -   Object-oriented programming: higher-order functions are enough abstraction for one day.
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

### [s:style](#CHAPTER): Make a Short Program More Readable

The program `check_datasets.py` is supposed to read one or more CSV data files
and check that they all contain the same fields
and that there are no missing values in mandatory fields.

1.  Rewrite `check_datasets.py` so that it is PEP-8 compliant.
2.  Did you uncover any bugs during your rewrite?
    If so,
    what is the smallest or simplest test case that demonstrates the incorrect behavior?
3.  Compare your cleaned-up version with the sample solution
    and (if you are working through this material with others)
    with one of your peers' rewrites.
    Where did you make different changes?
    Do any of those differences change the program's behavior?

### [s:tools](#CHAPTER): Build a Full-Featured Command-Line Filter

Write a command-line utility called `combine` that selects fields from two or more CSV datasets
and combines records with the same keys.

1.  `combine left.csv right.csv` combines the two named files and sends the result to standard output.
    The first column of each file is used as the join key;
    the output contains one copy of the key,
    and all the other columns of both files (in order, left then right).
1.  `combine -L 2 -R 3 left.csv right.csv`
    uses the second column of `left.csv` and the third column of `right.csv`
    as the join keys.
1.  `combine -l 1,2,3 -r 1,3,5 left.csv right.csv` only outputs columns 1, 2, and 3 of `left.csv`
    and columns 1, 3, and 5 of `right.csv`.
    (Columns are numbered starting at 1, not 0.)
1.  `combine` on its own or `combine --help` produces a usage message.
1.  `combine -o result.csv left.csv right.csv` sends the output to `result.csv`
    rather than to standard output.
1.  `combine - first.csv` combines standard input with `first.csv`,
    so `combine first.csv second.csv | combine - third.csv | combine - fourth.csv`
    does the right thing.
1.  If an input file does not exist or cannot be read,
    or if the output file cannot be created,
    `combine` prints an error message to stderr and exits with a status code of 1.
1.  If any of the columns designed by `-L`, `-R`, `-l`, or `-r` do not exist,
    or if columns are given out of order for `-l` or `-r`,
    `combine` prints an error message to stderr and exits with a status code of 1.

Your program must follow the style rules in PEP-8.

### [s:automate](#CHAPTER): Automating a Small Project

The directory `occupancy` contains data files and scripts
used to produce regular reports of hospital room occupancy rates;
the file `README.txt` explains how each script is used,
what files it consumes,
and what files it produces.
Write a Makefile with appropriate targets so that:

1.  `make` on its own prints a list of available targets with explanations of each.
1.  `make monthly/2018-05.csv` ensures that the May 2018 summary is up to date.
1.  `make monthly/index.csv` ensures that all monthly data for all years is up to date,
    and that the index file showing what data is available is also up to date.
1.  `make annual/YYYY.csv` ensures that the summary for the year YYYY is up to date
    (e.g., `make annual/2018.csv` ensures that 2018's summary is up to date).
1.  `make trends/YYYY.png` ensures that the trend visualization for the year YYYY
    is up to date.
1.  `make trends/all.png` ensures that the combined trend visualization for all years
    is up to date.

Your Makefile should use pattern rules wherever possible.

### [s:correct](#CHAPTER): Finding and Testing Hard-to-Reach Code

1.  Clone the `match` repository on your personal computer.
2.  Run the unit test suite.
3.  Look at the coverage report: what function isn't being tested?
4.  Write at least three tests for this function using `StringIO` to capture output.

### [s:workflow](#CHAPTER): Git Workflow

1.  Clone the `health` repository on your personal computer.
2.  Create a new branch from `master`, using your user name as the name of the branch.
3.  Edit and commit `CONTRIBUTORS.md` three times:
    1.  Add your name.
    2.  Add your email.
    3.  Add your GitHub user ID.
4.  Use `git rebase -i` to squash those three commits into one.
5.  Merge your changes into `master`.
6.  Create a tag for the merge commit.

### [s:structure](#CHAPTER): Reorganize a Small Project

The directory `latest` contains data files downloaded from several websites,
analysis scripts,
data summaries produced by those scripts,
and a few plots of those summaries;
the file `README.txt` contains
a transcript of the operations used to produce these files and plots.

1.  Reorganize these files so that they conform to Noble's Rules.
2.  Compare your reorganization to the sample solution
    and (if you are working through this material with others)
    with what one of your peers has done.
    Where did you make different changes?
    Do any of those differences change the program's behavior?
3.  Create a Pip package that will install the scripts as a Python package.
4.  Test your package by installing it in a virtual environment called `combine-test`.

### [s:reuse](#CHAPTER): A Generic Data Windowing Function

Write a function `window` that takes three parameters:

-   `values`: a list of numbers.
-   `width`: the integer width of a filtering window.
-   `filter`: a filtering or smoothing function.

When run, `window` creates a new list of the same size as the original
by sliding a window of size `width` over the input data,
passing that set of values to `filter`,
and storing the result in the output.
At the edges of the data, `window` passes in `None` for missing values;
it is up to the filtering function to handle these correctly.
For example,
if `filter` returns the maximum and `width` is 3,
then the output for the values `[1, 3, 2, 5, 4, 2]` will be `[3, 3, 5, 5, 5, 4]`,
while if `filter` returns the minimum and the width is also 3,
the output will be `[1, 1, 2, 2, 2, 2]`.

## Lesson Plan

We budget two hours for each of these topics, divided evenly between instruction, worked examples, and exercises.
It should therefore be possible to cover everything in an intensive two-day workshop.

1.  Writing code that is readable, testable, and maintainable ([s:style](#CHAPTER)).
1.  Building software tools that play nicely with others ([s:tools](#CHAPTER)).
1.  Managing libraries in a reproducible way ([s:libs](#CHAPTER)).
1.  Automating analyses with build tools ([s:automate](#CHAPTER)).
1.  Checking and demonstrating correctness via automated tests ([s:correct](#CHAPTER)).
1.  Using a branch-per-feature workflow, rebasing, and tags to manage work ([s:workflow](#CHAPTER)).
1.  Organizing the code, data, results, and reports in a small or medium-sized project ([s:project](#CHAPTER)).
1.  Building reusable software with higher-order functions ([s:reuse](#CHAPTER)).

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
