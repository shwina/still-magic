---
permalink: "/en/workflow/"
title: "A Scalable Workflow"
undone: true
questions:
-   "How can a growing number of people coordinate work on a single project?"
-   "How can I tell what needs to be done and who is doing it?"
objectives:
-   "Explain what rebasing is and use it interactively to collapse a sequence of commits into a single commit."
-   "Describe a branch-per-feature workflow and explain why to use it."
-   "Describe what a repository tag is and create an annotated tag in a Git repository."
-   "Explain what an issue tracking tool does and what it should be used for."
-   "Explain how to use labels on issues to manage work."
-   "Describe the information a well-written issue should contain."
keypoints:
-   "Create a new branch for every feature, and only work on that feature in that branch."
-   "Always create branches from `master`, and always merge to `master`."
-   "Use rebasing to combine several related commits into a single commit before merging."
-   "Create issues for bugs, enhancement requests, and discussions."
-   "Add people to issues to show who is responsible for working on what."
-   "Add labels to issues to identify their purpose."
-   "Use rules for issue state transitions to define a workflow for a project."
---

-   A common Git workflow for single-author/single-user projects:
    -   Make some changes
    -   `git add` and `git commit` as you go along
    -   `git push` to remote repository
    -   Switch machines
    -   `git pull` to get changes (and possibly resolve merge conflicts)
    -   Occasionally `git checkout -- .` or `git reset --hard VERSION` to discard changes
    -   (Even less frequently) recover old version(s) of file(s)
    -   Or `rm -rf` the repository and clone a new copy because everything is messed up
-   Essentially using Git for multi-version backup
-   But:
    -   Sometimes you have to work on several things at once
    -   Or need to set aside current work for a high-priority interrupt
    -   And this workflow doesn't provide guidance for collaborating with others
-   Following a few rules and using some of Git's more advanced capabilities solves these problems

## How Can I Use Branches to Manage Development of New Features? {#s:workflow-branch}

-   Use a [branch-per-feature][branch-per-feature] workflow
    -   `git checkout master`
    -   `git pull origin master` (or `git pull upstream master`) to make sure you're up to date
    -   `git checkout -b feature-name`
    -   Do some work
    -   `git push origin feature-name` to upload or update that branch
    -   `git pull origin master` again and resolve any conflicts
    -   `git merge feature-name master` (command line) to merge into master when work is done
-   Better:
    -   Create a [pull request](../gloss/#g:pull-request) on GitHub
    -   Within one repository (which may be shared with other people) or between repositories (from your fork to the upstream repository)
    -   Get someone to look over the changes and leave comments
    -   Make fixes: the pull request is updated in place
    -   Merge when done
-   But what's a "feature"?
    -   A pure addition that doesn't change anything else (e.g., a new analysis run)
    -   A change that you might want to undo as a unit
    -   E.g., a new parameter with configuration, option parsing, help, and effect on execution
    -   If you then re-run analyses, do those as separate features (because you might want to undo them separately)
-   Don't do several things in one branch
    -   Commit work (don't use `git stash`)
    -   Do the other thing
    -   Squash the history (described below)
    -   Merge to `master`
    -   Merge from master to the original branch
-   What's hard about branch-per-feature?
    -   Doing work in one branch while large refactoring is going on in another
    -   So don't do this

## How Can I Keep My Project's History Clean When Working on Many Branches? {#s:workflow-rebase}

-   [Rebasing](../gloss/#g:rebase) means moving or combining some commits from one branch to another
    -   Replay changes on one branch on top of changes made to another
    -   And/or collapse several consecutive commits into a single commit
    -   We will just use the latter ability
-   `git rebase -i BASE`
    -   `BASE` is the most recent commit *before* the sequence to be compressed
    -   Which is always confusing
-   Brings up a display of recent commits
    -   `pick` the first and `squash` the rest
    -   Then see the combination of recent changes and messages
    -   Edit to combine into one
-   Why go to this trouble?
    -   Because you may have done a commit, switched branches to work on something else, and then come back
    -   (You could use `git stash`, but that just makes life even more confusing)
    -   Or it may have taken you several tries to get something right
    -   Either way, only want one change in the final log in order to make undo and comprehension easier
-   What if you have pushed a branch to GitHub (or elsewhere) and then combine the commits to change its history?
    -   Use `git push --force` to overwrite the remote history
    -   This is a sign that you should have done something differently a while back
    -   "It's tough to make predictions, especially about the future" - Yogi Berra
-   Don't rebase branches that are shared with other people
    -   Creating a pull request from a branch effectively makes that branch shared

## How Can I Label Specific Versions of My Work? {#s:workflow-tag}

-   A [tag](../gloss/#g:git-tag) is a permanent label on a particular state of the repository
    -   Theoretically redundant, since the [commit hash](../gloss/#g:commit-hash) identifies that state as well
    -   But commit hashes are (deliberately) random and therefore hard to remember or find
-   Use [annotated tags](../gloss/#g:annotated-tag) to mark every major event in the project's history
    -   Annotated because they allow a message, just like a commit
-   Software projects use [semantic versioning](../gloss/#g:semantic-versioning) for software releases
    -   `major.minor.patch`
    -   Increment `major` every time there's an incompatible externally-visible change
    -   Increment `minor` when adding functionality without breaking any existing code
    -   Increment `patch` for bug fixes that don't add any new features ("now works as previously documented")
-   Research projects often use `report-date-event` instead of semantic versioning
    -   E.g., `jse-2018-06-23-response` or `pediatrics-2018-08-15-summary`
    -   Do not tempt fate by calling something `-final`
-   For simple projects, only tag the master branch
    -   Because everything that is finished is merged to master
-   Larger software projects may create a branch for each released version and do minor or patch updates on that branch
    -   Outside the scope of this lesson

## How Can I Manage the Work I Still Have To Do? {#s:workflow-issues}

-   Version control tells you where you've been; [issues](../gloss/#g:issue) tells us where you're going
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

<figure id="f:workflow-lifecycle"> <figcaption>Issue State Transitions</figcaption> <img src="../../figures/issue-lifecycle.svg"/> </figure>

## How Can I Write a Good Bug Report? {#s:workflow-bugs}

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

## How Can I Set Up a Consistent Workflow for My Project? {#s:workflow-status}

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

## Summary {#s:workflow-summary}

FIXME: create concept map for workflow

{% include links.md %}
