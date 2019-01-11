---
permalink: "/en/backlog/"
title: "Managing Backlog"
undone: true
questions:
-   "How can I tell what needs to be done and who is doing it?"
objectives:
-   "Explain what an issue tracking tool does and what it should be used for."
-   "Explain how to use labels on issues to manage work."
-   "Describe the information a well-written issue should contain."
keypoints:
-   "Create issues for bugs, enhancement requests, and discussions."
-   "Add people to issues to show who is responsible for working on what."
-   "Add labels to issues to identify their purpose."
-   "Use rules for issue state transitions to define a workflow for a project."
---

-   Version control tells you where you've been; [issues](#g:issue) tells us where you're going
    -   Issue tracking tools are often called ticketing systems or bug trackers,
        since they were created to keep track of work that nees to be done and bugs that needed fixing

## How Can I Manage the Work I Still Have To Do? {#s:backlog-issues}

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

<figure id="f:workflow-lifecycle"> <figcaption>Issue State Transitions</figcaption> <img src="../../figures/issue-lifecycle.svg"/> </figure>

## How Can I Write a Good Bug Report? {#s:backlog-bugs}

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

## How Can I Set Up a Consistent Workflow for My Project? {#s:backlog-status}

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

## Summary {#s:backlog-summary}

FIXME: create concept map for workflow

{% include links.md %}
