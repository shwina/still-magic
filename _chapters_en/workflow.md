---
permalink: "/en/workflow/"
title: "A Scalable Workflow"
questions:
-   "How can a growing number of people coordinate work on a single project?"
-   "How can I tell what state my project is actually in?"
objectives:
-   "Explain what rebasing is and use it interactively to collapse a sequence of commits into a single commit."
-   "Describe a branch-per-feature workflow and explain why to use it."
-   "Describe what a repository tag is and create an annotated tag in a Git repository."
-   "Explain what an issue tracking tool does and what it should be used for."
-   "Explain how to use labels on issues to manage work."
-   "Describe the information a well-written issue should contain."
-   "Explain how continuous integration works."
-   "Configure continuous integration for a small software project."
keypoints:
-   "Create a new branch for every feature, and only work on that feature in that branch."
-   "Always create branches from `master`, and always merge to `master`."
-   "Use rebasing to combine several related commits into a single commit before merging."
-   "Create issues for bugs, enhancement requests, and discussions."
-   "Add people to issues to show who is responsible for working on what."
-   "Add labels to issues to identify their purpose."
-   "Use rules for issue state transitions to define a workflow for a project."
-   "Continuous integration rebuilds and/or re-tests software every time something changes."
-   "Use continuous integration to check changes before they are inspected."
-   "Check style as well as correctness."
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
-   Version control tells you where you've been; [issues](#g:issue) tells us where you're going
    -   Issue tracking tools are often called ticketing systems or bug trackers,
        since they were created to keep track of work that nees to be done and bugs that needed fixing
-   Every issue has:
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
-   Use issues to prioritize work
    -   Create a tag for the next work sprint (typically called `V3.1` or `2018-03`)
    -   Assign that tag to issues that the group is going to try to close by that time
-   More sophisticated systems allow people to:
    -   Record dependencies between issues
    -   Estimate how long work will take
    -   Record how long work actually took
    -   Don't worry about any of this until people are actually using issues...
-   More sophisticated systems also constrain the transitions between states and who can make them
    -    Defines the project's workflow

<figure>
  <figcaption>Issue State Transitions</figcaption>
  <img id="f:workflow-lifecycle" src="../../files/issue-lifecycle.svg" alt="Issue State Transitions" />
</figure>

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
1.  Create a text file called 'accent.txt' containing the word "Pumpernickel"
    with an umlaut over the 'u'.

2.  Run 'python wordbase.py --all --message accent.txt'

Program should print "Pumpernickel" on a line by itself with the umlaut, but
instead it fails with the message:

    No encoding for [] on line 1 of 'accent.txt'.

([] shows where a solid black box appears in the output instead of a
printable character.)

python wordbase.py --version reports 0.13.1; using on Windows 10.
~~~

## Status and Lifecycle {#s:workflow-status}

-   Use labels to distinguish:
    -   Bug: something should work but doesn't
    -   Enhancement: something could/should be added
    -   Task: something needs to be done, but won't show up in code (e.g., we need to get the next release out by February)
    -   Question: how is something supposed to work?
    -   Discussion: we need to make a decision about something
        -   All issues can have discussion - this category is for ones that start that way
-   Add extra labels to distinguish:
    -   High Priority: small projects typically can't take advantage of multiple priority levels, so don't bother with them
    -   Won't Fix/Works as Designed/Duplicate: reasons for closing without acting
    -   Verified/Accepted/Decided: yes, this bug needs fixed, this feature should be added, or we've decided what to do
    -   Ready for Review/Ready to Merge: self-explanatory
    -   Accomplished: this task has been done
-   And assign people:
    -   Creator: usually added automatically by the system
    -   Owner: who's doing the work/moderating the discussion
    -   Reviewer: who's checking
-   Helpful to have one more label: *Suitable for Newcomer* or *Beginner*
    -   If you help potential new contributors find places to start, they're more likely to do so
-   Can use issue status to make the development lifecycle explicit
    -   I.e., only allow certain state transitions
    -   And notify interested parties of state transitions
-   Don't worry about any of this until people are actually using issues...

## Continuous Integration {#s:workflow-continuous}

-   [Continuous integration](#g:continuous-integration)
    -   Build and test code and documentation every time someone commits code
    -   Post results somewhere the team can see them
    -   If build or tests fail, send out notifications
-   Even better: build and test changes *before* they're merged
    -   Only do code review on changes that have passed mechanical checks
-   Most widely used system is [Travis CI][travis-ci]
    -   Easy integration with [Github][github]
    -   Will run tests on multiple platforms and with multiple versions of tools
-   Developers still have to build the tests
    -   CI only as good as the tests it runs
-   Check style as well as correctness by running [pep8][pep-8] or [formatR][format-r] as part of the build

### Exercises

#### Lint Your Code

1.  Find and install a [lint][lint]-like tool for your preferred language and run it on your code.
2.  What does it complain about?
3.  Which of its complaints do you disagree with?

#### Setting Up Continuous Integration

Follow the steps in [this tutorial][python-travis-tutorial] to set up Travis-CI testing for the SNDS repository.
How long did it take you to set this up?

{% include links.md %}
