---
permalink: "/en/workflow/"
title: "A Scalable Workflow"
questions:
-   FIXME
objectives:
-   FIXME
keypoints:
-   FIXME
---

-   A common Git workflow for single-author/single-user projects:
    -   Make some changes
    -   `git add` and `git commit` as you go along
    -   `git push` to remote repository
    -   Switch machines
    -   `git pull` to get changes (and possibly resolve merge conflicts)
    -   Occasionally `git checkout -- .` or `git reset --hard VERSION` to discard changes
    -   (Even less frequently) recover old version(s) of file(s)
-   Essentially using Git for multi-version backup
-   But:
    -   Sometimes you have to work on several things at once
    -   Or need to set aside current work for a high-priority interrupt
    -   And this workflow doesn't provide guidance for collaborating with others
-   Following a few rules and using some of Git's more advanced capabilities solves these problems

## Rebasing {#s:workflow-rebase}

FIXME:
-   What rebasing is and when/how to use it
-   The Golden Rule: never rebase shared branches
    -   Creating a pull request from a branch implicitly makes that branch shared
-   Common error messages and what to do next
-   `git push --force` is sometimes necessary
    -   But usually a sign that you should have done something differently a while back

## Branch Per Feature {#s:workflow-branch}

FIXME:
-   [branch-per-feature][branch-per-feature] workflow
-   Always branch from `master`
-   Don't do several things in one branch
    -   Commit work (don't use `git stash`)
    -   Do the other thing
    -   Merge to `master`
    -   Merge from master to the original branch
    -   Rebase as necessary to clean up history
-   What's a "feature"?
    -   A change that you might want to undo
    -   E.g., a new parameter with configuration, option parsing, help, and effect on execution
-   What's hard about branch-per-feature?
    -   Doing work in one branch while large refactoring is going on in another (so don't do this)

## Tagging {#s:workflow-tag}

FIXME:
-   Why and how to tag
-   Use [annotated tags](#g:annotated-tag) to mark every major event in the project's history
    -   Annotated because they allow a message, just like a commit
    -   Use semantic versioning for software releases
    -   Use `manuscript-date-event` for publications
        -   E.g., `jse-2018-06-23-response`
-   Semantic versioning
-   Treat each release branch as its own `master`
-   Porting bug fixes and features across releases is complicated
    -   Outside the scope of this tutorial

## Using Issues {#s:workflow-issues}

FIXME
-   Version control tells you where you've been; [ticketing](#g:ticketing) tells us where you're going
    -   Ticketing tools are often called bug trackers,
        since they were created to keep track of work that nees to be done and bugs that needed fixing
    -   Or issue trackers, since that sounds more corporate
-   Every ticket has:
    -   Unique ID/link
    -   One-line summary to aid browsing and search
    -   Status (discussed below)
    -   Creator's ID
    -   Other people's IDs
    -   Full description that may include screenshots, error messages, etc.
    -   Threaded discussion
-   Use it to:
    -   Describe bugs, and solicit/collect bug reports from community
    -   Request, plan, and discuss new features
        -   "Discuss" because most allow reply-to discussion threads, and will notify people who are already on the thread of updates
    -   Ask questions
        -   Repurposes the discussion capability
        -   If search is good and someone's willing to add tags, old issues can act as a FAQ
-   Use ticketing to prioritize work
    -   Create a tag for the next work sprint (typically called `V3.1` or `2018-03`)
    -   Assign that tag to tickets that the group is going to try to close by that time
-   More sophisticated systems allow people to:
    -   Record dependencies between tickets
    -   Estimate how long work will take
    -   Record how long work actually took
    -   Don't worry about any of this until people are actually using tickets...

## How to Write a Good Bug Report {#s:workflow-bugs}

1.  Make sure it actually *is* a bug.
2.  Try to come up with a short, repeatable way to trigger it.
    -   You'll be surprised how often you can solve the problem yourself as you do this...
3.  Write a descriptive short summary (something better than "program crashes")
4.  Describe how to reproduce
    -   Describe both what you expected and what it actually does
5.  Attach screenshots, input files, etc.
6.  Make sure to describe software version, operating system, etc.
7.  Describe each problem separately

~~~
ID: 1278
Creator: standage
Owner: malvika
Tags: Bug, Verified
Summary: wordbase.py fails on accented characters
Description:
1.  Create a text file called 'accent.txt' containing the word "Pümpernickel"
    with an umlaut over the 'u'.

2.  Run 'python wordbase.py --all --message accent.txt'

Program should print "Pümpernickel" on a line by itself, but instead
it fails with the message:

    No encoding for [] on line 1 of 'accent.txt'.

([] shows where a solid black box appears in the output instead of a
printable character.)

python wordbase.py --version reports 0.13.1; using on Windows 10.
~~~

## Status and Lifecycle {#s:workflow-status}

-   Use tags to distinguish:
    -   Bug: something should work but doesn't
    -   Enhancement: something could/should be added
    -   Task: something needs to be done, but won't show up in code (e.g., we need to get the next release out by February)
    -   Question: how is something supposed to work?
    -   Discussion: we need to make a decision about something
        -   All tickets can have discussion - this category is for ones that start that way
-   Add extra tags to distinguish:
    -   High Priority: small projects typically can't take advantage of multiple priority levels, so don't bother with them
    -   Won't Fix/Works as Designed/Duplicate: reasons for closing without acting
    -   Verified/Accepted/Decided: yes, this bug needs fixed, this feature should be added, or we've decided what to do
    -   Ready for Review/Ready to Merge: self-explanatory
    -   Accomplished: this task has been done
-   And assign people:
    -   Creator: usually added automatically by the system
    -   Owner: who's doing the work/moderating the discussion
    -   Reviewer: who's checking
-   Helpful to have one more tag: *Suitable for Newcomer* or *Beginner*
    -   If you help potential new contributors find places to start, they're more likely to do so
-   Can use ticket status to make the development lifecycle explicit
    -   I.e., only allow certain state transitions
    -   And notify interested parties of state transitions
-   Don't worry about any of this until people are actually using tickets...

{% include links.md %}
