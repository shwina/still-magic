---
title: "Introduction"
questions:
-   "What is the difference between open, reproducible, and sustainable?"
-   "What is computational competence?"
-   "What is the scope of this training?"
-   "What are the prerequisites for this training?"
objectives:
-   "Explain the difference between open science, reproducible research, sustainability, and competence."
-   "Determine readiness for using this material."
-   "Explain what 'done' looks like for the computational component of a small or medium-sized research project."
-   "Determine whether a particular research project meets that standard."
keypoints:
-   "Research is 'open' if everyone can read it."
-   "Research is 'reproducible' if people who have access can regenerate it."
-   "Research is 'sustainable' if it was built in reasonable time and without heroic effort."
-   "Computational competence is the digital equivalent of knowing how to use lab equipment properly."
-   "A project is 'done' when stakeholders can be reasonably sure the results are correct and the software can be understood, run, and extended by people other than the original authors without heroic effort."
---

Most books and courses about software engineering are aimed at product development,
but research has different aims and needs.
A research programmer's goal is to answer a question;
she might build software in order to do that,
but the software is only a means to an end.

But just as some astronomers spend their entire careers designing better telescopes,
some researchers choose to spend their time building software
that will primarily be used by their colleagues.
People who do this may be called [research software engineers](#g:rse) (RSEs)
or [data engineers](#g:data-engineering),
and the aim of these lessons is to help you get ready for these roles---to go from
writing code on your own, for your own use,
to working in a small team creating tools to help your entire field advance.

One of the many challenges you will face is
to find the appropriate mix of tools and methods for each problem you have to solve.
If you want to reformat a handful of text files so that your program can read them in,
you shouldn't bother writing a comprehensive test suite or setting up automated builds.
On the other hand,
if you *don't* do this,
and that "handful of text files" turns into a pile,
and then a mountain,
you will quickly reach a point where you wish you had.
We hope this training will help you understand what challenges have already been solved
and where to find those solutions
so that when you need them,
you'll be able to find them.

## What does "done" look like? {#s:intro-goals}

In order to answer the question posed in this section's title,
we need to distinguish between three key ideas.
The first is [open science](#g:open-science),
which aims to make research methods and results available for everyone to read and re-use.
The second is [reproducible research](#g:reproducible-research),
which means that anyone with access to the raw materials can easily reproduce the results.
Openness and reproducibility are closely related,
but are *not* the same thing:

-   If I share my data and analysis scripts,
    but haven't documented the manual steps in the analysis,
    my work is open but not reproducible.
-   If I completely automate the analysis,
    but it's only available to people in my company or lab,
    it's reproducible but not open.

The third key idea is [sustainability](#g:sustainability).
A piece of software is being sustained
if people are using it, fixing it, and improving it
rather than replacing it.
Sustainability isn't just a property of the software:
it also depends on the culture of its actual and potential users.
If "share, mend, and extend" is woven into the fabric of their culture,
even Fortran-77 can thrive
(though of course good tooling and packaging can lower costs and barriers to entry).
Conversely,
it doesn't matter whether a library has automated tests and is properly packaged
if potential users suffer from [Not Invented Here](#g:not-invented-here) syndrome.
More importantly,
if the software is being maintained by a couple of post-docs
who are being paid a fraction of what they could earn in industry,
and who have no realistic hope of promotion because their field looks down on tool building,
those people will eventually move on
and their software will start to suffer from [bit rot](#g:bit-rot).

What ties these three ideas together is the notion of
[computational competence](#g:computational-competence),
which is the the programming equivalent of good laboratory skills.
Software is just another kind of lab equipment;
just as an archaeologist should know how to prepare and catalog an artefact,
any researcher writing software should know how to make their work reproducible
and share it with the world
without staying up until dawn.

> **Why "Computational Competence"?**
>
> The term [computational thinking](#g:computational-thinking)
> has been widely used since [Wing2006](#BIB) introduced it a decade ago.
> It has also been used in such a wide variety of ways
> that no one really knows what it means.
> I therefore prefer to talk about computational competence---about
> someone's ability to do computing well.

## Why isn't all of this normal already? {#s:intro-against}

Nobody argues that research should be irreproducible or unsustainable,
but "not against it" and actively supporting it are very different things.
Academia doesn't yet know how to reward people for writing useful software,
so while you may be thanked,
the extra effort you put in may not translate into job security or decent pay.

And some people still argue against openness,
Being open is a big step toward a (non-academic) career path,
which is where approximately 80% of PhDs go,
and for those staying in academia,
open work is cited more often than closed (FIXME: citation).
However,
some people still worry that if they make their data and code generally available,
someone else will use it and publish a result they have come up with themselves.
This is almost unheard of in practice
(over twenty years, I know of only one case),
but that doesn't stop people using it as a boogeyman.

Other people are afraid of looking foolish or incompetent by sharing code that might contain bugs.
This isn't just [impostor syndrome](#g:impostor-syndrome):
members of marginalized groups are frequently judged more harshly than others (FIXME: CITE).

## What will this book accomplish? {#s:intro-coverage}

The goal of this book is to help you produce more correct results in less time and with less effort:
stakeholders will be confident that you did things the right way,
which in turn will allow them to be confident in your results,
and you and others will be able to re-use your data, software, and reports instead of constantly rewriting them.
To achieve this, we will cover:

-   Writing code that is readable, testable, and maintainable
-   Automating analyses with build tools
-   Checking and demonstrating correctness via automated tests
-   Publishing science in the 21st Century
-   Using a branch-per-feature workflow, rebasing, and tags to manage work
-   Organizing the code, data, results, and reports in a small or medium-sized project

These lessons can be used for self-study
by people who are taking part in something like the [Insight Data Science][insight] Fellows Program,
or as part of a one-semester course for graduate students or senior undergraduates.
You will know you're done when:

1.  You are reasonably confident that your results are correct.
    This is not the same as "absolutely sure":
    our goal is to make digital work
    as trustworthy as lab experiments or careful manual analysis.
2.  Your software can be used by other people without heroic effort,
    I.e., people you have never met can find it
    and figure out how to install it and use it
    in less time than it would take them to write something themselves.
3.  Small changes and extensions are easy
    so that your software can grow as your problems and questions evolve.

## What will we use as running examples? {#s:intro-example}

In order to make this material as accessible as possible,
we will use two text processing problems as running examples.
The first is an exploration of [Zipf's Law][zipfs-law],
which states that frequency of a word is inversely proportional to rank,
i.e.,
that the second most common word in some text
occurs half as often as most common,
the third most common occurs a third as often,
and so on.
We will write some simple software to test a corpus of text against this rule.
The files we will use are taken from the [Project Gutenberg][gutenberg]
and contain this many words:

| Book                            | Words  |
| ------------------------------- | -----: |
| anne_of_green_gables.txt        | 105642 |
| common_sense.txt                |  24999 |
| count_of_monte_cristo.txt       | 464226 |
| dracula.txt                     | 164424 |
| emma.txt                        | 160458 |
| ethan_frome.txt                 |  37732 |
| frankenstein.txt                |  78098 |
| jane_eyre.txt                   | 188455 |
| life_of_frederick_douglass.txt  |  43789 |
| moby_dick.txt                   | 215830 |
| mysterious_affair_at_styles.txt |  59604 |
| pride_and_prejudice.txt         | 124974 |
| sense_and_sensibility.txt       | 121590 |
| sherlock_holmes.txt             | 107533 |
| time_machine.txt                |  35524 |
| treasure_island.txt             |  71616 |

This is how often the most common words appear in this corpus as a whole:

| Word | Count |
| ---- | ----: |
| the  | 97278 |
| and  | 59385 |
| to   | 56028 |
| of   | 55190 |
| I    | 45680 |
| a    | 40483 |
| in   | 30030 |
| was  | 24512 |
| that | 24386 |
| you  | 22123 |
| it   | 21420 |

The frequencies aren't an exact match---we would expect about 48,600 occurrences of "and", for example---but
there certainly seems to be a decay curve of some kind.
We'll look more closely at this data as we go along.

The second project is a simple form of [computational stylometry](#g:computational-stylometry).
Different writers have different styles;
can a computer detect those differences,
and if so,
can it determine who the likely author of a text actually was?
Computational stylometry has been used to explore
which parts of Shakespeare's plays might have been written by other people,
which presidential tweets were composed by other people,
and who wrote incriminating emails in several high-profile legal cases.

The authors of our books are listed below.
Three of them were purportedly written by Jane Austen;
we will see if the similarity measures we develop show that.

| Author                      | Book                            |
| ----------------------------| ------------------------------- |
| Jane Austen                 | emma.txt                        |
| Jane Austen                 | pride_and_prejudice.txt         |
| Jane Austen                 | sense_and_sensibility.txt       |
| Charlotte Brontë            | jane_eyre.txt                   |
| Agatha Christie             | mysterious_affair_at_styles.txt |
| Frederick Douglass          | life_of_frederick_douglass.txt  |
| Arthur Conan Doyle          | sherlock_holmes.txt             |
| Alexandre Dumas             | count_of_monte_cristo.txt       |
| Herman Melville             | moby_dick.txt                   |
| Lucy Maud Montgomery        | anne_of_green_gables.txt        |
| Thomas Paine                | common_sense.txt                |
| Mary Wollstonecraft Shelley | frankenstein.txt                |
| Robert Louis Stevenson      | treasure_island.txt             |
| Bram Stoker                 | dracula.txt                     |
| H. G. Wells                 | time_machine.txt                |
| Edith Wharton               | ethan_frome.txt                 |

## Acknowledgments {#s:intro-ack}

This book owes its existence to
the hundreds of researchers I met through [Software Carpentry][carpentries].
I am also grateful to [Insight Data Science][insight] for sponsoring the early stages of this work,
to everyone who has contributed ({% include xref key="s:citation" %}),
and to:

-   *Practical Computing for Biologists* [Hadd2010](#BIB)
-   "A Quick Guide to Organizing Computational Biology Projects" [Nobl2009](#BIB)
-   "Ten Simple Rules for Making Research Software More Robust" [Tasc2017](#BIB)
-   "Best Practices for Scientific Computing" [Wils2014](#BIB)
-   "Good Enough Practices in Scientific Computing" [Wils2017](#BIB)

Before any of that, though,
four books written by [Brian Kernighan][kernighan-brian] and his colleagues
forever changed the way I think about programming
[Kern1978,Kern1988,Kern1983,Kern1981](#BIB).
*The Elements of Programming Style*,
*The C Programming Language*,
*The Unix Programming Environment*,
and *Software Tools in Pascal*
didn't just show my generation how to write software we could be proud of:
they also showed us that books about programming could be a pleasure to read.

## Contributing {#s:intro-contrib}

{% include contributing.md %}

{% include links.md %}
