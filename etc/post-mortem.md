---
permalink: "/en/post-mortem/"
title: "The Post Mortem"
undone: true
objectives:
- "FIXME"
keypoints:
- "FIXME"
---

The most valuable part of your project isn't the software you write,
or the grade you're given.  It's the project's **post mortem**.
Literally, this is an examination of a deceased person; in a software
project, it's a look back at what went right, and what went wrong.

The aim of a post mortem is to help the team and its members do better
next time by giving everyone a chance to reflect on what they've just
accomplished.  It is *not* to point the finger of shame at
individuals, although if that has to happen, the post mortem is the
best place for it.

Post mortems are pretty easy to run---just add the following to the
rules for [running a meeting](#meetings):

Get a moderator who wasn't part of the project
:   and doesn't have a stake in it.  Otherwise, the meeting will either
    go in circles, or focus on only a subset of important topics.  In
    the case of student projects, this moderator might be the course
    instructor, or (if the course is too large, or the instructor is
    lazy) a TA.

Set aside an hour, and only an hour.
:   In my experience, nothing useful is said in the first ten minutes of
    anyone's first post mortem, since people are naturally a bit shy
    about praising or damning their own work.  Equally, nothing useful
    is said after the first hour: if you're still talking, it's probably
    because one or two people have a *lot* they want to get off their
    chests.

Require attendance.
:   Everyone who was part of the project ought to be in the room for the
    post mortem.  This is more important than you might think: the
    people who have the most to learn from the post mortem are often
    least likely to show up if the meeting is optional.

Make two lists.
:   When I'm moderating, I put the headings "Good" and "Bad" on the
    board, then do a lap around the room and ask every person to give me
    one item (that hasn't already been mentioned) for each list.

Comment on actions, rather than individuals.
:   By the time the project is done, some people simply won't be able to
    stand one another.  Don't let this sidetrack the meeting: if someone
    has a specific complaint about another member of the team, require
    him to criticize a particular event or decision.  "He had a bad
    attitude" does *not* help anyone improve their game.

Once everyone's thoughts are out in the open, organize them somehow so
that you can make specific recommendations about what to do next time.
This list is one of the two major goals of the post mortem (the other
being to give people a chance to be heard).  For example, here are the
recommendations that came out of a post mortem I did with students in
2006:

-   Do a better job of tracking actual progress, rather than reported
    progress.  Maybe require a one-minute demo every time a feature is
    supposedly completed?

-   Teams should find one block of 2-3 hours per week when they can work
    side by side: IM meetings and email resulted in a lot of dropped
    balls.

-   Having someone who worked on the project in the previous term come
    in to get the new team up to speed made a huge difference.

-   Team members should read each other's code, at least during the
    early stages of the project, to make sure everyone is actually
    following the coding guidelines.

-   A large number of small commits is better than a small number of
    massive commits.

-   Ticketing system was too complicated for students' needs: really
    just want a shared online to-do list.

-   Teams should have to report test coverage at every progress meeting
    to make sure that a lot of untested code doesn't pile up during the
    term.

{% include links.md %}
