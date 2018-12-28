---
permalink: "/en/integrate/"
title: "Continuous Integration"
undone: true
questions:
-   "How can I tell what state my project is actually in?"
objectives:
-   "Explain how continuous integration works."
-   "Configure continuous integration for a small software project."
keypoints:
-   "Continuous integration rebuilds and/or re-tests software every time something changes."
-   "Use continuous integration to check changes before they are inspected."
-   "Check style as well as correctness."
---

-   [Continuous integration](../gloss/#g:integrate-integration) is a simple idea
    -   Build and test code and documentation every time someone commits code
    -   Post results somewhere everyone can see them (you, the team, users, ...)
    -   If build or tests fail, send out notifications
-   Even better: build and test changes *before* they're merged
    -   Only do code review on changes that have passed mechanical checks
-   Most widely used system is [Travis CI][travis-ci]
    -   Easy integration with [Github][github]
    -   Will run tests on multiple platforms and with multiple versions of tools
-   Developers still have to build the tests
    -   CI only as good as the tests it runs
-   Check style as well as correctness by running [pep8][pep-8] or [formatR][format-r] as part of the build

## How Can I Run Commands Automatically Every Time a Repository Is Updated? {#s:integrate-basic}

-   Tell Travis to care about your repository
    -   Log in to [Travis-CI][travis-ci] with your GitHub credentials
    -   On the left, beside "My Repositories", click "+" to add a new repository
    -   Find the repository you want to connect to Travis-CI
    -   Flick the switch
-   Create a file called `.travis.yml` in the root directory of the repository (note the leading '.')

```
language: "python"
python:
-   "3.6"
install:
-   "pip install -r requirements.txt"
script:
-   "python src/continuous/hello.py"
```

-   Four keys:
    -   `language` tells Travis what language we're using
    -   `python` specifies the version (or versions) of Python to use
    -   `install` tells Travis how to install the software we need for testing
        -   Have a list of packages in `requirements.txt` for `pip` to use ([s:packages](#CHAPTER))
    -   `script` tells Travis what to run on our behalf
-   Create a "test" script that just prints a message

```py
#!/usr/bin/env python

print('Hello, continuous')
```

-   Note the first line
    -   `#!` means "use the following program to run this script instead of Bash"
    -   So `#!/Users/standage/anaconda3/bin/python` woul run a particular version of Python
    -   But `/usr/bin/env some_program_name` finds the program you want
    -   So if Python is installed somewhere else, this still works
-   Every time a commit is made to this branch, Travis will:
    -   Create a new Linux image
    -   Install the desired version of Python (or clone an existing image that has it, which is faster)
    -   Install the software described by `requirements.txt`
    -   Run the script
    -   Report the results at `https://travis-ci.org/USER/REPO`
-   Summary report tells you what happened

<figure id="f:integrate-summary"> <figcaption>Travis Summary Report</figcaption> <img src="../../files/travis-summary.png"/> </figure>

-   Detailed log has *lots* of information
    -   397 lines hidden under "Build system information"
    -   Another 23 under "pip install" heading

<figure id="f:integrate-log"> <figcaption>Travis Log</figcaption> <img src="../../files/travis-log.png"/> </figure>

-   Most important thing is the test program's [exit status](../gloss/#g:exit-status)
-   Exit status of 0 means "nothing went wrong"
    -   The default if you don't specify anything else
    -   You can do it explicitly with `sys.exit(0)`
-   Any non-zero status is interpreted as a shell error code
    -   `sys.exit(1)` means "something went wrong"
    -   Don't worry about other codes (like 127 for "command not found" and 130 for "terminated with Control-C")
-   Test this by adding a second script to `.travis.yml`

```
language: "python"
python:
-   "3.6"
install:
-   "pip install -r requirements.txt"
script:
-   "python src/continuous/hello.py"
-   "python src/continuous/failure.py"
```
```py
#!/usr/bin/env python

import sys

print('And this command fails')
sys.exit(1)
```

-   Commit and view
-   Initially told that the build is queued

<figure id="f:integrate-queued"> <figcaption>Travis Queued</figcaption> <img src="../../files/travis-queued.png"/> </figure>

-   Don't need to refresh the page
    -   When the build starts, the page automatically starts updating
    -   And when the build finishes, the summary is red and the log displays this

<figure id="f:integrate-failure"> <figcaption>Travis Failure</figcaption> <img src="../../files/travis-failure.png"/> </figure>

## How Can I Display the Status of a Repostiory? {#s:integrate-display}

-   Display build status on GitHub because that's where most people look
-   Look at the top of the status page for the build icon

<figure id="f:integrate-build-icon"> <figcaption>Travis Build Icon</figcaption> <img src="../../files/travis-build-icon.png"/> </figure>

-   Click on it to bring up a dialog
-   Select the Markdown you need for the `master` branch
-   Paste it into `README.md` in your repository's root directory
    -   Which is the project's home page on GitHub, *not* the root of the GitHub Pages site
    -   Unless you've configured it that way, which is confusing, because then the GitHub repo page has a table of header values
-   Commit this to `master`
-   While we're waiting for the build, take a look at the "Branches" tab
    -   Clicking on a check mark or an X will bring up details of that build on that branch

<figure id="f:integrate-overall"> <figcaption>Travis Overall</figcaption> <img src="../../files/travis-overall.png"/> </figure>

-   Sure enough, once the build on `master` completes, the page displays a red X
-   Modify `.travis.yml` to remove the failing script
-   Commit
-   Wait for email to arrive
-   Go to project on GitHub

<figure id="f:integrate-github-icon"> <figcaption>Travis GitHub Icon</figcaption> <img src="../../files/travis-github-icon.png"/> </figure>

## How Can I Automatically Run Tests for My Project When Things Change?  {#s:integrate-tests}

FIXME: describe how to run actual tests with Travis-CI

## Summary {#s:integrate-summary}

FIXME: create concept map

{% include links.md %}
