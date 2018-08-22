---
permalink: "/en/automate/"
title: "Automating Analyses"
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
-   "Make is a widely-used build tool that uses files' timestamps to find out-of-date dependencies."
-   "A Make rule has targets, dependencies, and actions."
-   "A target can correspond to a file or be a phony target (used simply to trigger actions)."
-   "When a target is out of date with respect to its dependencies, Make executes the actions associated with its rule."
-   "Make executes as many rules as it needs to when updating files, but always respect depdendency order."
-   "Make defines the automatic variables `$@` (target), `$^` (all dependencies), and `$<` (first dependency)."
-   "Pattern rules can use `%` as a placeholder for parts of filenames."
-   "Makefiles can define variables using `NAME=value`."
-   "Makefiles can also use functions such as `$(wildcard ...)` and `$(patsubst ...)`."
-   "Specially-formatted comments can be used to make Makefiles self-documenting."
---

-   [Zipf's Law][zipfs-law]: frequency of a word is inversely proportional to rank
    -   I.e., second most common word occurs half as often as most common, third most common a third as often, etc.
-   We want to test books against this distribution
-   Each book is in `raw/title.txt`
-   Use `bin/countwords.py` to produce `results/title.csv`
    -   Each row is rank, word, number of occurrences
-   Use `bin/plotcounts.py` to visualize counts
-   Use `bin/testfit.py` to compare actual distributions against expectations
-   Can also use `bin/countwords.py` to analyze multiple files, then plot and test aggregate results
-   Common workflow:
    -   Analyze one input file to create one output file
    -   Write the analysis results to a new file
    -   Analyze multiple input files to create an aggregate output file
    -   Plot individual and aggregate analyses
    -   Test individual and aggregate data statistically
-   Easy to do this for a handful of files
    -   But also easy to get wrong
    -   Becomes tedious and error-prone as the number of files grows
-   Can write a shell script or another Python program to do the analysis
    -   Explicitly documents the pipeline so that our colleagues (and future selves) can understand it
    -   Enables us to re-do the entire analysis with a single command
        if we change methods, parameters, libraries, etc.
    -   Prevents us from making lots of little errors -
        no guarantee we'll get the script right the first time,
        but once we've fixed it,
        it will stay fixed.
-   But it's inefficient
    -   Re-analyze all individual files whenever a new file is added
    -   Regenerate all plots, even for data sets (files) that haven't changed
    -   Not a problem when computation is fast, but many computations aren't
-   What we want is a way to describe:
    -   Which files depend on which other files
    -   How to generate or update a file when necessary
-   This is the job of a [build tool](#g:build-tool)
    -   So-called because it builds new files out of old ones
-   Most widely used build tool is [Make][make]
    -   First written in 1976 to recompile programs (which at the time was a slow process)
    -   [Many better tools][build-tools] have been developed since, but none has been as widely adopted
    -   In particular, [Snakemake][snakemake] has a lot of fans, and a future version of this tutorial might well use it
-   Make uses:
    -   [Timestamps](#g:timestamp) on files to determine what's out of date
    -   Shell commands to create or update files
    -   Reliance on shell commands is a reason for its longevity: Make can run pretty much any command
-   [GNU Make][gnu-make] is a free, fast, and well-documented implementation of Make
-   This introduction based on:
    -   The [Software Carpentry lesson on Make][swc-make] maintained by [Gerard Capes][capes-gerard]
    -   [Jonathan Dursi][dursi-jonathan]'s [introduction to pattern rules][dursi-pattern-rules]

## Our First Build {#s:automate-first}

-   Create a file called `Makefile` containing the following:

```
# Regenerate data for "Moby Dick"
results/moby-dick.csv : raw/moby-dick.txt
        python bin/countwords.py raw/moby-dick.txt results/moby-dick.csv
```

-   `#` starts a comment, which runs to the end of a line (just as it does in Python)
-   `results/moby-dick.csv` is the [target](#g:make-target) of a [rule](#g:make-rule)
    -   I.e., something that may need to be created or updated
    -   Every rule has one or more targets
-   `raw/moby-dick.txt` is a [dependency](#g:make-dependency) in that rule
    -   I.e., a file that some other file depends on
    -   A rule can have zero or more dependencies
-   A colon separates targets from dependencies
-   `python bin/countwords.py raw/moby-dick.txt results/moby-dick.csv`
    is an [action](#g:make-action) that creates or updates the target when it is out of date
    -   A rule can have zero or more actions
-   Actions are indented by a single tab character
    -   A legacy of Make's distant origins
-   Together, this tells Make when and how to re-create `results/moby-dick.csv`
-   To test creation:
    -   Delete `results/moby-dick.csv` and type `make`
    -   Make automatically reads commands from `Makefile` and runs the action
-   To test update:
    -   Use `touch raw/moby-dick.txt` to update the timetamp on the input file
    -   Run `make`: sure enough, `results/moby-dick.csv` is updated
-   Might get an error message if `Makefile` contains spaces instead of tabs for indent:

```
Makefile:3: *** missing separator.  Stop.
```

-   Don't have to call the instructions `Makefile`
-   Rename the file `pipeline.mk`
-   Run `make -f pipeline.mk`

```
make: `results/moby-dick.csv' is up to date.
```

-   Means our target does not need any work
-   Use `ls -l -t` to list files most recently changed first, with timestamps

### Common Problems

FIXME: common problems for first Makefile

### Exercises

FIXME: exercises for first Makefile

## Extending Our Pipeline {#s:automate-extend}

-   Add another rule to the end of `pipeline.mk`

```
# Regenerate data for "Jane Eyre"
results/jane-eyre.csv : raw/jane-eyre.txt
        python bin/countwords.py raw/jane-eyre.txt results/jane-eyre.csv
```

-   Run `make -f pipeline.mk`

```
make: `results/moby-dick.csv' is up to date.
```

-   Nothing happens because Make attempts to build the first target it finds in `project.mk`
    -   Called the [default target](#g:default-target)
-   Need to tell Make to build `results/jane-eyre.csv`:

```
$ make -f project.mk results/jane-eyre.csv
```

-   Now Make runs:

```
python bin/countwords.py raw/jane-eyre.txt results/jane-eyre.csv
```

-   Note the difference between "up to date" and "nothing to be done"
    -   If we ask Make to build a file that already exists and is up to date,
        Make tells us it is up to date
    -   If we ask Make to build a file that exists but for which there is no rule,
        it tells us "Nothing to be done"
    -   Get the latter message when there is a rule with no actions

### Common Problems

FIXME: common problems for extending the Make pipeline

### Exercises

FIXME: exercises for extending the Make pipeline

## Cleaning Up {#s:automate-phony}

-   Add another target to `pipeline.mk` to delete all generated files
    -   By convention, this target is called `clean`

```
# Remove all generated files.
clean :
        rm -f results/*.csv
```

-   A [phony target](#g:phony-target): doesn't correspond to any files
    -   Also doesn't have any dependencies
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
    -   Since the rule has no dependencies, it can't be out of date
    -   So no actions are executed
-   Solution #1: don't have phony targets with the same names as files or directories
-   Solution #2: tell Make that the target is phony by putting this at the top of `pipeline.mk`

```
.PHONY : clean
```

### Common Problems

FIXME: common problems for phony targets

### Exercises

FIXME: exercises for phony targets

## Chaining Dependencies {#s:automate-chain}

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
results/moby-dick.csv : raw/moby-dick.txt
        python bin/countwords.py raw/moby-dick.txt results/moby-dick.csv

# Regenerate data for "Jane Eyre"
results/jane-eyre.csv : raw/jane-eyre.txt
        python bin/countwords.py raw/jane-eyre.txt results/jane-eyre.csv

# Remove all generated files.
clean :
        rm -f results/*.csv
```

-   We can draw the dependencies as a [dependency graph](#g:dependency-graph):
    -   Arrows show what each target depends on
-   Note: no guarantee of order when the graph is executed
    -   Make can rebuild either results file first

FIXME: dependency graph

### Common Problems

FIXME: common problems for chaining dependencies

### Exercises

FIXME: exercises for chaining dependencies

## Automatic Variables {#s:automate-automatic}

-   Add a third book to `pipeline.mk`, then a fourth
    -   Lots of duplication, which means lots of future maintenance effort
-   Make lets us write [pattern rules](#g:pattern-rule) to express general ideas
-   In order to use these, we first need to use [automatic variables](#g:automatic-variable)
-   Step 1: don't duplicate the target filename

```
# Regenerate data for "Moby Dick"
results/moby-dick.csv : raw/moby-dick.txt
        python bin/countwords.py raw/moby-dick.txt $@
```

-   `$@` means "the target of the current rule"
    -   Cryptic name is unfortunate, but we're stuck with it
-   Step 2: replace the dependencies in the action with `$^`

```
# Regenerate data for "Moby Dick"
results/moby-dick.csv : raw/moby-dick.txt
        python bin/countwords.py $^ $@
```

-   `$^` is another automatic variable meaning "all the dependencies of the current rule"
-   What if we want to regenerate results when our script changes?
    -   Make the result depend on the script

```
# Regenerate data for "Moby Dick" - WRONG
results/moby-dick.csv : raw/moby-dick.txt bin/countwords.py
        python bin/countwords.py $^ $@
```

-   Doesn't do the right thing, since the action expands to:

```
python bin/countwords.py raw/moby-dick.txt bin/countwords.py results/moby-dick.csv
```

-   Make helpfully provides another automatic variable `$<` meaning "the first dependency"
-   Rewrite our improved rule like this:

```
# Regenerate data for "Moby Dick" - RIGHT
results/moby-dick.csv : raw/moby-dick.txt bin/countwords.py
        python bin/countwords.py $^ $<
```

### Common Problems

FIXME: common problems for automatic variables

### Exercises

FIXME: exercises for automatic variables

## Pattern Rules {#s:automate-pattern}

-   We can now replace the repeated rules for results files with one [pattern rule](#g:pattern-rule)
-   Use `%` as a [wildcard](#g:wildcard) on the left and right sides

```
results/%.csv : raw/%.txt bin/countwords.py
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
results/%.csv : raw/%.txt bin/countwords.py
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
python bin/countwords.py raw/moby-dick.csv results/moby-dick.txt
python bin/countwords.py raw/jane-eyre.csv results/jane-eyre.txt
```

-   Can still rebuild individual files:

```
$ make -f pipeline.mk results/jane-eyre.txt
```

### Common Problems

FIXME: common problems for pattern rules

### Exercises

FIXME: exercises for pattern rules

## Using Variables {#s:automate-variables}

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
python bin/countwords.py raw/moby-dick.csv results/moby-dick.txt
python bin/countwords.py raw/jane-eyre.csv results/jane-eyre.txt
```

-   But how is this better?  We still have to remember to add a file's name to this list
-   Or we can get Make to generate the list for us
-   Step 4: define a variable using a [function](#g:make-function)
    -   The syntax is a bit ugly, because functions were added to Make long after it was first created

```
RAW = $(wildcard raw/*.txt)
```

-   This calls the function `wildcard` with the argument `raw/*.txt`
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
echo RAW: raw/moby-dick.txt raw/jane-eyre.txt
RAW: raw/moby-dick.txt raw/jane-eyre.txt
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
RAW: raw/moby-dick.txt raw/jane-eyre.txt
```

-   Step 5: generate the list of desired output files from the list of input files
    -   Use the same kind of patterns used in rules themselves with a function called `patsubst`

```
RESULTS = $(patsubst raw/%.txt,results/%.csv,${RAW})
```

-   `$(patsubst ...)` calls the pattern substitution function
-   First argument is what to look for
    -   In this case, a text file in the `raw` directory
    -   `%` matches the [stem](#g:filename-stem) of the file's name, which is the part we want to keep
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
RAW: raw/moby-dick.txt raw/jane-eyre.txt
RESULTS: results/moby-dick.csv results/jane-eyre.csv
```

-   Step 6: test

```
$ make -f pipeline.mk clean
$ make -f pipeline.mk everything
```
```
rm -f results/*.csv
python bin/countwords.py raw/moby-dick.csv results/moby-dick.txt
python bin/countwords.py raw/jane-eyre.csv results/jane-eyre.txt
```

-   Step 7: add another source file and see what happens
    -   If we've done everything right, Make will automatically generate the results file for it

```
$ cp /tmp/life-of-frederick-douglass.txt raw
$ make -f pipeline.mk
```
```
python bin/countwords.py raw/life-of-frederick-douglass.csv results/life-of-frederick-douglass.txt
```

-   And there we have it: a fully automated, reproducible data analysis pipeline

### Common Problems

FIXME: common problems for using variables in Make

### Exercises

FIXME: exercises for using variables in Make

## Documenting Makefiles {#s:automate-doc}

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
RAW = $(wildcard raw/*.txt)
RESULTS = $(patsubst raw/%.txt,results/%.csv,${RAW})

## everything: regenerate all results.
everything : ${RESULTS}

# Regenerate data for a single book.
results/%.csv : raw/%.txt
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

### Common Problems

FIXME: common problems for documenting Makefiles

### Exercises

FIXME: exercises for documenting Makefiles

## Summary {#s:automate-summary}

<figure>
  <figcaption>Make Concept Map</figcaption>
  <img id="f:automate-concept" src="../../files/automate.svg" alt="Make Concept Map" />
</figure>

{% include links.md %}
