---
permalink: "/en/"
root: true
redirect_from: "/"
---

> It's still magic even if you know how it's done.
>
> -- Terry Pratchett

As research becomes more computing intensive,
researchers need more computing skills.
Being able to use version control and to write small programs and shell scripts is a start;
these lessons will help you take your next steps so that:

-   other people (including your future self) can re-do your analyses;
-   you and the people using your results can be confident that they're correct; and
-   re-using your software is easier than rewriting it.

This course are the second part of [Merely Useful][config-organization]:

1.  The first part,
    [One Extra Fact][one-extra-fact]
    covers what every researcher ought to know about the Unix shell, version control with Git,
    and programming in either R or Python.
2.  This part,
    [Still Magic][config-website],
    is more advanced material for people who are building research software for others to use
    or find themselves doing some [data engineering](../gloss/#g:data-engineering).
3.  Finally,
    [Set On Fire][set-on-fire]
    is intended for people running larger projects with external collaborators.

## Who Are These Lessons For? {:#s:index-personas}

Amira:
    Completed a Master's in epidemiology five years ago,
    and has worked since then for a small NGO.
    She did a biostatistics course during her degree,
    and has learned some R and Python by doing data science courses online,
    but has no formal training in programming.
    Amira would like to tidy up the scripts, data sets, and reports she has created
    in order to share them with her colleagues.
    These lessons will show her how to do this and what "done" looks like.

Jun:
    Completed an Insight Data Science fellowship last year after doing a PhD in Geology,
    and now works for a company that does forensic audits.
    He has used a variety of machine learning and visualization software,
    and has made a few small contributions to a couple of open source R packages.
    He would now like to make his own code available to others;
    this course will show him how such projects should be organized.

Sami:
    Learned a fair bit of numerical programming while doing a BSc in applied math,
    then started working for the university's supercomputing center.
    Over the past few years,
    the kinds of applications they are being asked to support
    have shifted from fluid dynamics to data analysis.
    This course will teach them how to build and run data pipelines
    so that they can teach those skills to their users.

## Summary {#s:index-summary}

For researchers and data scientists who have a basic understanding of the Unix shell, Python, and Git,
and who want to be more productive and have more confidence in their results,
this training course
provides a pragmatic, tools-based introduction to program design and maintenance.
Unlike academic software engineering courses and most books aimed at professional software developers,
this course uses data analysis as a motivating example
and assumes that the learner's ultimate goal is to answer a question rather than ship an application.

Learners must be comfortable with the basics of
the [Unix shell][swc-shell], [Python][swc-python] or [R][swc-r], and [Git][swc-git].
They will need a personal computer with Internet access,
the Bash shell,
Python 3,
and a GitHub account.

## Acknowledgments {#s:index-acknowledgments}

This material is based on [Nobl2009,Tasc2017,Wils2014,Wils2017](#BIB)
and on the [Carpentries][carpentries] lessons;
please see [Wils2018](#BIB) and [this appendix](../design/) for design notes.
We are grateful to [Insight Data Science][insight] for sponsoring the early stages of this work,
and to [everyone who has contributed](../citation/#s:citation-contributors).

## Contributing {#s:index-contributing}

{% include contributing.md %}

{% include links.md %}
