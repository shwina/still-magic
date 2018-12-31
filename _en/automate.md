---
permalink: "/en/automate/"
title: "Automating Analyses"
undone: true
questions:
-   "How can I make my analyses easier to reproduce?"
-   "How can I make it easier to repeat analyses when I get new data, or when my data or scripts change?"
objectives:
-   "Explain what a build tool is and how build tools aid reproducible research."
-   "Describe and identify the three parts of a Make rule."
-   "Write a Makefile that re-runs a multi-stage data analysis."
-   "Explain and trace how Make chooses an order in which to execute rules."
-   "Explain what phony targets are and define a phony target."
-   "Explain what automatic variables are and correctly identify three commonly-used automatic variables."
-   "Rewrite Make rules to use automatic variables."
-   "Explain why and how to write a pattern rule in a Makefile."
-   "Rewrite Make rules to use patterns."
-   "Define variables in a Makefile explicitly and by using functions."
-   "Make a self-documenting Makefile."
keypoints:
-   "A build tool re-runs commands to bring files up to date with respect to the things they depend on."
-   "Make is a widely-used build tool that uses files' timestamps to find out-of-date prerequisites."
-   "A Make rule has targets, prerequisites, and actions."
-   "A target can correspond to a file or be a phony target (used simply to trigger actions)."
-   "When a target is out of date with respect to its prerequisites, Make executes the actions associated with its rule."
-   "Make executes as many rules as it needs to when updating files, but always respect prerequisite order."
-   "Make defines the automatic variables `$@` (target), `$^` (all prerequisites), and `$<` (first prerequisite)."
-   "Pattern rules can use `%` as a placeholder for parts of filenames."
-   "Makefiles can define variables using `NAME=value`."
-   "Makefiles can also use functions such as `$(wildcard ...)` and `$(patsubst ...)`."
-   "Specially-formatted comments can be used to make Makefiles self-documenting."
---

As [the introduction said](../intro/#s:intro-example),
Zipf's Law states that the second most common word in a body of text
appears half as often as the most common,
the third most common appears a third as often,
and so on.
The analyses we want to do include:

-   Analyze one input file to see how well it conforms to Zipf's Law.
-   Analyze multiple input files to how well then conform in aggregate.
-   Plot individual and aggregate word frequency distributions and expected values.

The project we have inherited as a starting point contains the following:

1.  The books we are analyzing are in <code>data/<em>title</em>.txt</code>.
2.  A program called `bin/countwords.py` can read a text file
    and produce a CSV file with two columns:
    the words in the text
    and the number of times that word occurs.
3.  `bin/countwords.py` can analyze several files at once if we provide many filenames on the command line
    or concatenate the files and send them to standard input in a pipeline
    using something like `cat data/*.txt | bin/countwords.py`.
4.  Another program, `bin/plotcounts.py`, will create a visualization for us
    that shows word rank on the X axis and word counts on the Y axis.
    (It doesn't show the actual words.)
5.  A third program, `bin/collate.py`,
    takes one or more CSV files as input and merges them
    by combining the counts for words they have in common.
6.  Finally,
    `bin/testfit.py` will compare actual distributions against expectations
    and give a fitting score.

It's easy enough to run these programs by hand if we only want to analyze a handful of files,
but doing this becomes tedious and error-prone as the number of files grows.
Instead,
we can write a shell script or another Python program to do multi-file analyses.
Doing this documents the pipeline so that our colleagues (and future selves) can understand it,
and enables us to re-do the entire analysis with a single command if we get new data
or change our methods, parameters, or libraries.
It also prevents us from making lots of little errors:
there's no guarantee we'll get the script right the first time,
but once we've fixed it, it will stay fixed.

However,
re-running the entire analysis every time we get a new file is inefficient:
we don't need to re-count the words in our first thousand books
when we add the thousand and first.
This isn't a problem when calculations can be done quickly,
but many can't,
and anyway,
the point of this chapter is to introduce a tool for handling cases in which
we really want to avoid doing unnecessary work.

What we want is a way to describe which files depend on which other files
and how to generate or update a file when necessary.
This is the job of a [build tool](../gloss/#g:build-tool).
As the name suggests,
a build tool's job is to build new files out of old ones.
The most widely used build tool,
[Make][make],
was written in 1976 to recompile programs
(which at the time was a slow process).
[GNU Make][gnu-make] is a free, fast, and well-documented version of Make;
we will use it throughout this book.

> #### Alternatives
>
> [Many better build tools][build-tools] have been developed since Make---so many,
> in fact,
> that none has been able to capture more than a small fraction of potential users.
> [Snakemake][snakemake] has a lot of fans,
> and a future version of this tutorial might well use it.

## How can I update a file when its prerequisites change? {#s:automate-first}

Make is based on three key ideas:

1.  The operating system automatically records a [timestamp](../gloss/#g:timestamp)
    every time a file is changed.
    By checking this,
    Make can tell whether files are newer or older than other files.
2.  A programmer writes a [Makefile](../gloss/#g:makefile)
    to tell Make how files depend on each other.
    For example,
    the Makefile could say that `results/moby-dick.csv` depends on `data/moby-dick.txt`,
    or that `plots/aggregate.svg` depends on all of the CSV files in the `results/` directory.
3.  The Makefile includes shell commands to create or update files that are out of date.
    For example,
    it could include a command to (re-)run `bin/countwords.py`
    to create `results/moby-dick.csv` from `data/moby-dick.txt`.
    (Make's use on shell commands is one reason for its longevity,
    since it allows programmers to write tools for updating files
    in whatever language they want.)

Let's start by creating a file called `Makefile` that contains the following three lines:

```make
# Regenerate data for "Moby Dick"
results/moby-dick.csv : data/moby-dick.txt
        python bin/countwords.py data/moby-dick.txt > results/moby-dick.csv
```
{: title="automate/single-rule.mk"}

The `#` character starts a comment,
which runs to the end of a line (just as it does in Python or R).
`results/moby-dick.csv` is the [target](../gloss/#g:make-target) of a [rule](../gloss/#g:make-rule),
i.e., something that may need to be created or updated.
Every rule in a Makefile has one or more targets,
and must be written flush against the left margin.

`data/moby-dick.txt` is a [prerequisite](../gloss/#g:make-prerequisite) in that rule,
i.e.,
something that the garget of the rule depends on.
A single colon separates the target from its prerequisites,
and a rule can have any number of prerequisites---we'll see examples soon.

The indented line that uses Python to run `bin/countwords.py`
is the rule's [action](../gloss/#g:make-action).
It creates or updates the target when it is out of date.
A rule can have any number of actions,
but they *must* be indented by a single tab character.
Notice that the output of `bin/countwords.py` is [redirected](#../gloss/#g:redirection) using `>`
to create the output file:
we will look [later](../configure/) at modifying the script
so that it can take the name of an output file as an argument.

Together,
the three parts of this rule tell Make when and how to re-create `results/moby-dick.csv`.
To test that it works,
run this command in the shell:

```shell
$ make
```

Make automatically looks for a file called `Makefile` and checks the rules it contains.
In this case,
one of three things will happen:

1.  Make won't be able to find the file `data/moby-dick.csv`,
    so it will run the script to create it.
2.  Make will see that `data/moby-dick.txt` is newer than `results/moby-dick.csv`,
    in which case it will run the script to update the results file.
3.  Make will see that `results/moby-dick.csv` is newer than its prerequisite,
    so it won't do anything.

In the first two cases,
Make will show the command it runs,
along with anything the command prints to the screen
via [standard output](../gloss/#g:stdout) or [standard error](../gloss/#g:stderr).
In this case,
there is no screen output,
so we only see the command.

> #### Indentation Errors
>
> If `Makefile` contains spaces instead of tabs to indent the rule's action,
> we will see an error message like this:
> 
> ```text
> Makefile:3: *** missing separator.  Stop.
> ```
>
> The requirement to use tabs is a legacy of Make's origins as a student intern project,
> and no,
> I'm not kidding.

If we run `make` again right away it doesn't re-run our script
because we're in situation #3 from the list above:
the target is newer than its prerequisites,
so no action is required.
We can check this by listing the files with their timestamps,
ordered by how recently they have been updated:

```shell
$ ls -l -t data/moby-dick.txt results/moby-dick.csv
```
```text
-rw-r--r--  1 gvwilson  staff   219107 31 Dec 08:58 results/moby-dick.csv
-rw-r--r--  1 gvwilson  staff  1276201 31 Dec 08:58 data/moby-dick.txt
```

When Make sees that a target is newer than its prerequisites
it displays a message like this:

```text
make: `results/moby-dick.csv' is up to date.
```

To test that Make is actually doing the right thing, we can:

1.  Delete `results/moby-dick.csv` and type `make` again (situation #1).
2.  Run the command `touch data/moby-dick.txt` to update the timestamp on the source file,
    then run `make` (situation #2).

## How can I tell Make where to find rules? {#s:automate-naming}

We don't have to call our file of rules `Makefile`.
If we want,
we can rename the file `single-rule.mk`
and then run it with `make -f single-rule.mk`.
Most people don't do this in real projects,
but in a lesson like this,
which includes many example Makefiles,
it comes in handy.

Using `-f` doesn't change our [working directory](../gloss/#g:working-directory).
If, for example, we are in `/home/gvwilson/still-magic` and run `make -f src/automate/single-rule.mk`,
our working directory remains `/home/gvwilson/still-magic`.
This means that Make will look for the rule's prerequisite in `/home/gvwilson/still-magic/data/moby-dick.txt`,
not in `/home/gvwilson/still-magic/src/automate/data/moby-dick.txt`.

FIXME: diagram

## How Can I Update Multiple Files When Their Prerequisites Change? {#s:automate-extend}

-   Add another rule to the end of `pipeline.mk`

```
# Regenerate data for "Jane Eyre"
results/jane-eyre.csv : data/jane-eyre.txt
        python bin/countwords.py data/jane-eyre.txt results/jane-eyre.csv
```

-   Run `make -f pipeline.mk`

```
make: `results/moby-dick.csv' is up to date.
```

-   Nothing happens because Make attempts to build the first target it finds in `project.mk`
    -   Called the [default target](../gloss/#g:default-target)
-   Need to tell Make to build `results/jane-eyre.csv`:

```
$ make -f project.mk results/jane-eyre.csv
```

-   Now Make runs:

```
python bin/countwords.py data/jane-eyre.txt results/jane-eyre.csv
```

-   Note the difference between "up to date" and "nothing to be done"
    -   If we ask Make to build a file that already exists and is up to date,
        Make tells us it is up to date
    -   If we ask Make to build a file that exists but for which there is no rule,
        it tells us "Nothing to be done"
    -   Get the latter message when there is a rule with no actions

## How Can I Clean Up Temporary Files That I Don't Need? {#s:automate-phony}

-   Add another target to `pipeline.mk` to delete all generated files
    -   By convention, this target is called `clean`

```
# Remove all generated files.
clean :
        rm -f results/*.csv
```

-   A [phony target](../gloss/#g:phony-target): doesn't correspond to any files
    -   Also doesn't have any prerequisites
    -   Just a way to save useful commands in a Makefile
-   Use it with:

```
$ make -f pipeline.mk clean
```

-   Phony targets are useful as a way of documenting actions in a project
-   But there's a catch
    -   Create a directory called `clean`
    -   Run `make -f pipeline.mk clean`

```
make: `clean' is up to date.
```

-   Make finds something called `clean` and assumes that's what the rule is referring to
    -   Since the rule has no prerequisites, it can't be out of date
    -   So no actions are executed
-   Solution #1: don't have phony targets with the same names as files or directories
-   Solution #2: tell Make that the target is phony by putting this at the top of `pipeline.mk`

```
.PHONY : clean
```

## How Can I Make One Update Depend On Another? {#s:automate-chain}

-   To re-make all the results files, provide multiple targets on the command line:

```
$ make -f pipeline.mk results/moby-dick.csv results/jane-eyre.csv
```

-   This requires users to know what files they might want to create
-   Better approach: create a phony target that rebuilds all the output files
    -   And make it the first rule in the file so that it is the default

```
# Phony targets.
.PHONY : clean everything

# Regenerate all results.
everything : results/moby-dick.csv results/jane-eyre.csv
```

-   Now run `make -f pipeline.mk`
    -   Make reads rules from `pipeline.mk`
    -   Uses the rule for `everything` as its default
    -   `everything` is only "up to date" if the two CSV files are up to date
    -   So Make looks in `pipeline.mk` for a rule for each
    -   And runs each of those rules
-   `pipeline.mk` now looks like this:

```
# Phony targets.
.PHONY : clean everything

# Regenerate all results.
everything : results/moby-dick.csv results/jane-eyre.csv

# Regenerate data for "Moby Dick"
results/moby-dick.csv : data/moby-dick.txt
        python bin/countwords.py data/moby-dick.txt results/moby-dick.csv

# Regenerate data for "Jane Eyre"
results/jane-eyre.csv : data/jane-eyre.txt
        python bin/countwords.py data/jane-eyre.txt results/jane-eyre.csv

# Remove all generated files.
clean :
        rm -f results/*.csv
```

-   We can draw the prerequisites as a [dependency graph](../gloss/#g:dependency-graph):
    -   Arrows show what each target depends on
-   Note: no guarantee of order when the graph is executed
    -   Make can rebuild either results file first

FIXME: dependency graph

## How Can I Abbreviate My Update Rules? {#s:automate-automatic}

-   Add a third book to `pipeline.mk`, then a fourth
    -   Lots of duplication, which means lots of future maintenance effort
-   Make lets us write [pattern rules](../gloss/#g:pattern-rule) to express general ideas
-   In order to use these, we first need to use [automatic variables](../gloss/#g:automatic-variable)
-   Step 1: don't duplicate the target filename

```
# Regenerate data for "Moby Dick"
results/moby-dick.csv : data/moby-dick.txt
        python bin/countwords.py data/moby-dick.txt $@
```

-   `$@` means "the target of the current rule"
    -   Cryptic name is unfortunate, but we're stuck with it
-   Step 2: replace the prerequisites in the action with `$^`

```
# Regenerate data for "Moby Dick"
results/moby-dick.csv : data/moby-dick.txt
        python bin/countwords.py $^ $@
```

-   `$^` is another automatic variable meaning "all the prerequisites of the current rule"
-   What if we want to regenerate results when our script changes?
    -   Make the result depend on the script

```
# Regenerate data for "Moby Dick" - WRONG
results/moby-dick.csv : data/moby-dick.txt bin/countwords.py
        python bin/countwords.py $^ $@
```

-   Doesn't do the right thing, since the action expands to:

```
python bin/countwords.py data/moby-dick.txt bin/countwords.py results/moby-dick.csv
```

-   Make helpfully provides another automatic variable `$<` meaning "the first prerequisite"
-   Rewrite our improved rule like this:

```
# Regenerate data for "Moby Dick" - RIGHT
results/moby-dick.csv : data/moby-dick.txt bin/countwords.py
        python bin/countwords.py $^ $<
```

## How Can I Write One Rule To Update Many Different Files in the Same Way? {#s:automate-pattern}

-   We can now replace the repeated rules for results files with one [pattern rule](../gloss/#g:pattern-rule)
-   Use `%` as a [wildcard](../gloss/#g:wildcard) on the left and right sides

```
results/%.csv : data/%.txt bin/countwords.py
        python bin/countwords.py $< $@
```

-   `%` cannot be used in actions, which is why `$<` and `$@` are needed
-   `pipeline.mk` is now:

```
# Phony targets.
.PHONY : clean everything

# Regenerate all results.
everything : results/moby-dick.csv results/jane-eyre.csv

# Regenerate data for a single book.
results/%.csv : data/%.txt bin/countwords.py
        python bin/countwords.py $< $@

# Remove all generated files.
clean :
        rm -f results/*.csv
```

-   Clean and build:

```
$ make -f pipeline.mk clean
$ make -f pipeline.mk everything
```

-   Output is:

```
rm -f results/*.csv
python bin/countwords.py data/moby-dick.csv results/moby-dick.txt
python bin/countwords.py data/jane-eyre.csv results/jane-eyre.txt
```

-   Can still rebuild individual files:

```
$ make -f pipeline.mk results/jane-eyre.txt
```

## How Can I Define Sets of Files Automatically? {#s:automate-variables}

-   Our automated build is still not fully automated
    -   If we add another book to `raw`, we have to remember to also add it to `pipeline.mk`
-   Fix this in steps
-   Step 1: define a variable of our own for the list of files we want to generate
    -   Put the definition near the top of the file to make it easy to find
    -   Variables don't have to be in ALL CAPS, but it's conventional

```
RESULTS = results/moby-dick.csv results/jane-eyre.csv
```

-   Step 2: change the `everything` target to depend on these files

```
# Regenerate all results.
everything : ${RESULTS}
```

-   We use a variable by putting its name in `${...}`
    -   If we just use `$NAME`, as we do with the shell,
        Make interprets this as a variable called `$N` followed by the literal characters `"AME"`
    -   Another leftover from the 1970s
-   Step 3: test the change

```
$ make -f pipeline.mk clean
$ make -f pipeline.mk everything
```
```
rm -f results/*.csv
python bin/countwords.py data/moby-dick.csv results/moby-dick.txt
python bin/countwords.py data/jane-eyre.csv results/jane-eyre.txt
```

-   But how is this better?  We still have to remember to add a file's name to this list
-   Or we can get Make to generate the list for us
-   Step 4: define a variable using a [function](../gloss/#g:make-function)
    -   The syntax is a bit ugly, because functions were added to Make long after it was first created

```
RAW = $(wildcard data/*.txt)
```

-   This calls the function `wildcard` with the argument `data/*.txt`
-   Result is a list of all the text files in the `raw` directory
-   To check, add another phony target to the end of the file called `settings`

```
.PHONY: clean everything settings

...

settings :
        echo RAW: ${RAW}
```

-   `echo` is a shell command that simply prints its arguments
-   Running this gives:

```
$ make -f pipeline.mk settings
```
```
echo RAW: data/moby-dick.txt data/jane-eyre.txt
RAW: data/moby-dick.txt data/jane-eyre.txt
```

-   Output appears twice because Make shows us the command, then runs it
-   If we put `@` before the command, Make doesn't show it before running it

```
settings :
        @echo RAW: ${RAW}
```
```
$ make -f pipeline.mk settings
```
```
RAW: data/moby-dick.txt data/jane-eyre.txt
```

-   Step 5: generate the list of desired output files from the list of input files
    -   Use the same kind of patterns used in rules themselves with a function called `patsubst`

```
RESULTS = $(patsubst data/%.txt,results/%.csv,${RAW})
```

-   `$(patsubst ...)` calls the pattern substitution function
-   First argument is what to look for
    -   In this case, a text file in the `raw` directory
    -   `%` matches the [stem](../gloss/#g:filename-stem) of the file's name, which is the part we want to keep
-   Second argument is what to replace matches with
    -   Keep the stem, but create a CSV file in the `results` directory
-   Third argument is the list to look in
    -   In this case, the list of raw filenames
-   Check that this has worked by adding to the `settings` target

```
settings :
        @echo RAW: ${RAW}
        @echo RESULTS: ${RESULTS}
```
```
$ make -f pipeline.mk settings
```
```
RAW: data/moby-dick.txt data/jane-eyre.txt
RESULTS: results/moby-dick.csv results/jane-eyre.csv
```

-   Step 6: test

```
$ make -f pipeline.mk clean
$ make -f pipeline.mk everything
```
```
rm -f results/*.csv
python bin/countwords.py data/moby-dick.csv results/moby-dick.txt
python bin/countwords.py data/jane-eyre.csv results/jane-eyre.txt
```

-   Step 7: add another source file and see what happens
    -   If we've done everything right, Make will automatically generate the results file for it

```
$ cp /tmp/life-of-frederick-douglass.txt raw
$ make -f pipeline.mk
```
```
python bin/countwords.py data/life-of-frederick-douglass.csv results/life-of-frederick-douglass.txt
```

-   And there we have it: a fully automated, reproducible data analysis pipeline

## How Can I Document My Update Rules? {#s:automate-doc}

-   Every well-behaved program can print a help message
-   `make --help` shows help for Make itself, not for our Makefile
-   Option 1: provide a special target like `settings` to print available targets

```
.PHONY: clean everything help settings

...

help :
        @echo "everything: rebuild all results"
        @echo "clean: remove all generated files"
        @echo "help: show available targets"
        @echo "settings: show variable values"
```

-   This is easy to set up and does the job, but once again:
    -   Redundancy: this information ought to appear as a comment on each rule as well
    -   Relies on human memory: author has to remember to update `help` when adding or changing rules
-   A better way:
    -   Format some comments specially
    -   Extract and print only those comments
-   Use `grep` to find these special comments and print those lines
-   Step 1: decide how to mark the comments we want to extract
    -   By convention, use `##` instead of a single `#`

```
# Phony targets.
.PHONY : clean everything settings

# Define input and output files.
RAW = $(wildcard data/*.txt)
RESULTS = $(patsubst data/%.txt,results/%.csv,${RAW})

## everything: regenerate all results.
everything : ${RESULTS}

# Regenerate data for a single book.
results/%.csv : data/%.txt
        python bin/countwords.py $< $@

## clean: remove all generated files.
clean :
        @rm -f ${RESULTS}

## settings: show variable values
settings :
        @echo RAW: ${RAW}
        @echo RESULTS: ${RESULTS}
```

-   Step 2: add a rule to find and print these lines

```
.PHONY : clean everything settings

...

## help: show available targets
help :
        @grep -e '##' pipeline.mk
```

-   Step 3: test

```
$ make -f pipeline.mk help
```
```
## everything: regenerate all results.
## clean: remove all generated files.
## settings: show variable values
## help: show available targets
```

-   That's *almost* what we want
-   Can get rid of the leading `##` markers by using the venerable Unix stream editor `sed` instead of `grep`

```
help :
        @sed -n -e 's/## //p' pipeline.mk
```
```
$ make -f pipeline.mk help
```
```
everything: regenerate all results.
clean: remove all generated files.
settings: show variable values
help: show available targets
```

-   Taking the `sed` command apart:
    -   `-n` means "do not print every line" (default is to do so)
    -   `-e` means "here's the expression to match"
    -   The `s` and `p` in `'s/## //p'` mean "search for lines that match this pattern and print them"
    -   The pattern `/## //` means "find two #'s followed by a space and replace them with nothing (i.e., delete them)"
-   None of this is part of Make, so most people simply copy this rule from file to file

## Summary {#s:automate-summary}

<figure id="f:automate-concept"> <figcaption>Make Concept Map</figcaption> <img src="../../figures/automate.svg"/> </figure>

This introduction based on
the [Software Carpentry lesson on Make][swc-make] maintained by [Gerard Capes][capes-gerard]
and on [Jonathan Dursi][dursi-jonathan]'s [introduction to pattern rules][dursi-pattern-rules].
[Smit2011](#BIB) describes the design and implementation of several build tools in detail.

{% include links.md %}
