---
permalink: "/en/tools/"
title: "Building Tools"
questions:
-   FIXME
objectives:
-   FIXME
keypoints:
-   FIXME
---

FIXME: introduction

## Parsing Command-Line Arguments {#s:tools-args}

FIXME
-   use a dictionary for results (or define a class for more sophisticated applications)
-   check values before doing any operations
-   do not set defaults when there isn't a universal obvious value
-   report *all* errors to save people effort
-   use positive sense for flags (to avoid conditionals like `if not settings['discard']`)

## Input, Output, and Exit {#s:tools-stdio}

FIXME
-   reading from stdin and writing to stdout
-   so put file open/close in `main` and have function that executes action
    -   helps with testing later on
-   usually have one output in order to play nicely with pipes
    -   if you want one output for each input, write a shell loop
-   use streams wherever possible so that your tool can handle very large inputs
-   exit status (so that other tools can do the right thing)

## Usage {#s:tools-usage}

FIXME
-   include version number
-   build your own help *or* use `argparse`
-   emphasize declarative programming
-   http://jeromebelleman.gitlab.io/posts/publishing/manpages/

## Logging {#s:tools-logging}

FIXME
-   version number
-   problem of storing settings in output (not tidy data)
-   `assert` versus logging
-   throw exception and log for anything that should cause halt

## Configuration Files {#s:tools-config}

FIXME
-   the confusion of formats
-   the need for nesting
-   INI
-   YAML

{% include links.md %}
