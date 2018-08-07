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
-   How to play nicely with other command-line tools?
    -   Play nicely with pipelines
    -   Signal success or failure for shell scripts and tools like Make ([s:automate](#CHAPTER))
-   How to connect to other programs?
    -   Use a shell script to combine everything: universal but limited
    -   Run your program in a sub-process: ditto
    -   Build a library with a command-line wrapper: flexible, but more work for users

## Parsing Command-Line Arguments {#s:tools-args}

FIXME
-   use a dictionary for results (or define a class for more sophisticated applications)
-   check values before doing any operations
-   do not set defaults when there isn't a universal obvious value
-   report *all* errors to save people effort
-   use positive sense for flags (to avoid conditionals like `if not settings['discard']`)
-   Eliminate fixed paths in the software
    -   `/Users/standage/run_5/try-this.config` probably doesn't exist on other people's machines...

## Input, Output, and Exit {#s:tools-stdio}

FIXME
-   reading from stdin and writing to stdout
-   so put file open/close in `main` and have function that executes action
    -   helps with testing later on
-   usually have one output in order to play nicely with pipes
    -   if you want one output for each input, write a shell loop
-   use streams wherever possible so that your tool can handle very large inputs
-   exit status (so that other tools can do the right thing)
-   Produce identical results when given identical inputs
    -   Absolutely necessary for reproducible research
    -   Means external control of random number generation seeds,
        sorting for dates and names,
        etc.
    -   Probably the hardest thing on this list for many projects

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
-   Use configuration files for less frequently changed options
-   Frequently use multiple overlaid configuration files
    -   System-level configuration file created during installation for things like cluster name
    -   User-level configuration file in `~/.programrc` for user's credentials
        -   `rc` suffix is old Unix abbreviation for "resource control"
    -   Job-level configuration file for particular runs
-   Use a standard syntax for configuration files
    -   Windows INIT files are widely supported
    -   YAML is increasingly popular
    -   "If you have to write a parser, you've done something wrong."
    - ...or someone upstream from you did
-   But be careful [[Xu2015](#CITE)]
    -   Only a small percentage (6.1%-16.7%) of configuration parameters
        are set by the majority of users; a significant percentage (up to
        54.1%) of parameters are rarely set by any user.
    -   A small percentage (1.8%-7.8%) of parameters are configured by more than 90% of the users.
    -   Software developers often choose more "flexible" data types for
        configuration parameters to give users more flexibility of
        settings (e.g., using numeric types instead of the simple Boolean
        or enumerative ones). However, users seem not to take full
        advantage of such flexibility. A significant percentage (up to
        47.4%) of numeric parameters have no more than five distinct
        settings among all the users' settings.
    -   Similarly, for enumerative parameters with many options, typically
        only two to three of the options are actually used by the users,
        indicating once again the over-designed flexibility.
    -   A significant percentage (up to 48.5%) of configuration
        issues are about users' difficulties in finding or setting the
        parameters to obtain the intended system behavior
    -   A significant percentage (up to 53.3%) of configuration errors are
        introduced due to users' staying with default values incorrectly.
    -   Searching user manuals by keywords is not efficient to help users
        identify the target parameter(s).

{% include links.md %}
