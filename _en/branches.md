---
permalink: "/en/branches/"
title: "A Branching Workflow"
undone: true
questions:
-   "How can a growing number of people coordinate work on a single project?"
objectives:
-   "Explain what rebasing is and use it interactively to collapse a sequence of commits into a single commit."
-   "Describe a branch-per-feature workflow and explain why to use it."
-   "Describe what a repository tag is and create an annotated tag in a Git repository."
keypoints:
-   "Create a new branch for every feature, and only work on that feature in that branch."
-   "Always create branches from `master`, and always merge to `master`."
-   "Use rebasing to combine several related commits into a single commit before merging."
---

A common Git workflow for single-author/single-user projects is:

1.  Make some changes, running `git add` and `git commit` as you go along.
2.  `git push` to send those changes to a remote repository for backup and sharing.
3.  Switch computers (e.g., go from your laptop to the cluster where you're going to process full-sized data sets).
4.  `git pull` to get your changes from the remote repository,
    and possibly resolve merge conflicts if you made some changes on the cluster the last time you were there
    but forgot to push them to the remote repo.

Occasionally,
you'll run `git checkout -- .` or `git reset --hard VERSION` to discard changes.
Less frequently,
you'll use `git diff -r abcd1234 path/to/file` or `git show abcd1234:path/to/file`
to look at what's changed in files,
or `git checkout abcd1234 path/to/file` followed by `git add` and `git commit`
to restore an old version of a file.
And every once in a while,
you'll [jenny](#g:jenny) the repository and clone a new copy because everything is messed up.

This workflow essentially uses Git to do backups and as a replacement for `scp`
(or `ftp`, if you're of an older generation).
But sometimes you have to work on several things at once in a single project,
or need to set aside current work for a high-priority interrupt.
And even if those situations don't arise,
this workflow doesn't provide guidance for collaborating with others.

This lesson introduces a few working practices that will help you do these things.
Along the way, it shows you how to use some of Git's more advanced capabilities.
As with everything involving Git,
the syntax for commands is more complicated than it needs to be [Pere2013,Pere2016](#BIB),
but if used carefully,
they can make you much more productive.

## How can I use branches to manage development of new features? {#s:branches-branch}

Experienced developers tend to use a [branch-per-feature workflow](#g:branch-per-feature-workflow),
even when they are working on their own.
Whenever they want to create a new feature,
they create a new branch from `master` and do the work there.
When it's done,
they merge that branch back into `master.

More specifically,
a branch-per-feature workflow looks like this:

1.  `git checkout master` to make sure you're working in the `master` branch.

2.  `git pull origin master` (or `git pull upstream master`) to make sure that
    your starting point is up to date
    (i.e., that the changes you committed while working on the cluster yesterday are now in your local copy,
    or that the fix your colleague did last week has been incorporated).

3.  <code>git checkout -b <em>name-of-feature</em></code> to create a new branch.
    The branch's name should be as descriptive as the name of a function
    or of a file containing source code:
    `"stuff"` or `"fixes"` saves you a couple of seconds of typing when you create the branch,
    and will cost you much more time than that later on
    when you're juggling half a dozen branches
    and trying to figure out what's in each.

4.  Do the work you want to do.
    If some other task occurs to you while you're doing it---for example,
    if you're writing a new function and realize that the documentation for some other function should be updated---*don't*
    do that work in this branch just because you happen to be there.
    Instead,
    commit your changes,
    switch back to `master`,
    create a new branch for the other work,
    and carry on.

5.  Periodically,
    you may <code>git push origin <em>name-of-feature</em></code> to save your work to GitHub.

6.  When the work is done,
    you `git pull origin master` to get any changes that anyone else has put in the master copy
    into your branch
    and merge any conflicts.
    This is an important step:
    you want to do the merge *and test that everything still works* in *your* branch,
    not in `master`.

7.  Finally,
    use `git checkout master` to switch back to the `master` branch on your machine
    and <code>git merge <em>name-of-feature</em> master</code> to merge your changes into `master`.
    Test it one more time,
    and then `git push origin master` to send your changes to the remote repository
    for everyone else to admire and use.

It takes longer to describe this workflow than to use it.
Right now,
for example,
I have six active branches in the repository for this material:
`master` (which is the published version),
`explain-branch-per-feature` (which is where I'm writing this),
and four others that I've created from `master` to remind myself to fix a glossary entry,
to rewrite the description in `README.md` of how to generate a PDF of these notes,
and so on.
I am essentially using branches as a to-do list,
which is no more expensive than typing a brief note about the feature into a text file
or writing it in a lab notebook,
and much easier to share.

## What *is* a feature? {#s:branches-thinking}

But what is a "feature", exactly?
What's large enough to merit creation of a new branch?
On small projects,
with or without collaborators,
I try to follow these rules?

1.  Anything cosmetic that is only one or two lines long can be done in `master` and committed right away.
    "Cosmetic" means changes to comments or documentation:
    nothing that affects how code runs---not even a simple variable renaming---is done this way,
    because experience has taught that things that aren't supposed to often do.

2.  A pure addition that doesn't change anything else is a feature and goes into a branch.
    For example,
    if you run a new analysis and save the results,
    that should be done on its own branch
    because it might take several tries to get the analysis to run,
    and you might interrupt yourself several times to fix things that you've discovered aren't working.

3.  Every change to code that someone might want to undo later in one step gets done as a feature.
    For example,
    if a parameter is added to a function,
    every call to the function has to be updated;
    since neither alteration makes sense without the other,
    it's considered a single feature and should be done in one branch.

The hardest thing about using a branch-per-feature workflow is actually doing it for small changes.
As the first point in the list above suggests,
most people are pragmatic about this on small projects;
on large ones,
where dozens of people might be committing,
even the smallest and most innocuous change needs to be in its own branch
so that it can be reviewed (which we discuss below).

The other thing that's hard to do with a branch-per-feature workflow is a major code reorganization.
If many files are being moved, renamed, and altered in order to restructure the project,
merging branches where those changes *haven't* been made can be tedious and error-prone.
The solution is to not get into this situation:
as we'll discuss later,
[refactoring](../refactor/) should be done in many small steps,
not one big one.

## How can I make it easy for people to review my work before I merge it? {#s:branches-pull-request}

The biggest benefit of having a second person work on a programming project
is not getting twice as much code written,
but having a second pair of eyes look at the software.
We'll discuss how to do code review [later](../review/),
but a good first step depends on using a branch-per-feature workflow.

In order for someone to review your change,
that change and the original have to somehow be put side-by-side.
The usual way to do this is to create a [pull request](#g:pull-request),
which is a marker saying, "Someone would like to merge branch A into branch X".
The pull request does *not* contain the changes:
instead,
it points at two branches,
so that if either branch is changed,
the differences displayed are always up to date.

FIXME: figure

Pull requests can be created between two branches in a single repository,
or between branches of different repositories.
The latter is common in projects with many contributors:
each contributor works in a branch in their own [fork](#g:fork) of the repository,
and when they're done,
they create a pull request offering to merge their changes into the `master` branch
of the original repository.
In order to update their own repository,
they pull changes from the original:

FIXME: figure

A pull request can store more than the location of the source and destination branch.
In particular,
it can store comments that people have made about the proposed merge.
GitHub and other [forges](#g:forge) allow users to add comments on the pull request as a whole,
or on particular lines,
and can mark old comments as out of date if the lines of code the comment is attached to are updated.

Pull requests aren't just for code.
If you are using a [typesetting language](#g:typesetting-language) like Markdown or LaTeX to write your papers,
you can create pull requests for changes
so that your colleagues can comment on them,
then revise and push again when you incorporate their suggestions.
This workflow has all the benefits of adding comments to Google Docs,
but scales to large projects or large numbers of contributors.
The downside,
of course,
is that you have to use a typesetting language rather than a [WYSIWYG](#g:wysiwyg) editor,
because the programmers who created Git and other version control systems
still don't support anything that couldn't be put on a punchcard in 1965.

## How can I switch between branches when work is only partly done? {#s:branches-switching}

-   Don't do several things in one branch
-   Commit work (don't use `git stash`)
-   Do the other thing
-   Squash the history (described below)
-   Merge to `master`
-   Merge from master to the original branch

## How Can I Keep My Project's History Clean When Working on Many Branches? {#s:branches-rebase}

-   [Rebasing](#g:rebase) means moving or combining some commits from one branch to another
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

## How Can I Label Specific Versions of My Work? {#s:branches-tag}

-   A [tag](#g:git-tag) is a permanent label on a particular state of the repository
    -   Theoretically redundant, since the [commit hash](#g:commit-hash) identifies that state as well
    -   But commit hashes are (deliberately) random and therefore hard to remember or find
-   Use [annotated tags](#g:annotated-tag) to mark every major event in the project's history
    -   Annotated because they allow a message, just like a commit
-   Software projects use [semantic versioning](#g:semantic-versioning) for software releases
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

## Summary {#s:branches-summary}

FIXME: create concept map for workflow

{% include links.md %}
