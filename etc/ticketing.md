---
permalink: "/en/ticketing/"
title: "Ticketing"
undone: true
objectives:
- "FIXME"
keypoints:
- "FIXME"
---

You probably have a to-do list somewhere.  It might be scribbled in a
calendar or lab notebook, kept in a text file on your laptop, or in
your head; wherever and however you maintain it, it lists the things
you're supposed to do, when they're due, and (possibly) how urgent
they are.

At its simplest, a **ticketing system** is a shared to-do list.
Ticketing systems are also called **bug trackers**, because most
software projects use one to keep track of the bugs that developers
and users find.  These days, ticketing systems are almost invariably
web-based.  To create a new ticket, you enter a title and a short
description; the system then assigns it a unique serial number.  You
can usually also specify:

- who is responsible for the ticket (e.g., who's supposed to fix the
  bug, or test the fix, or update the documentation);

- what kind of ticket it is (a bug report, a request for a new
  feature, a question to be answered, or some other task);

- how important it is; and

- when it's due.

If version control keeps track of where your project has been, your
ticketing system keeps track of where you're going.  After version
control, ticketing is therefore the most essential part of a team
project.  Without it, you and your teammates will have to constantly
ask each other "What are you working on?", "What am I supposed to be
working on?", and "Who was supposed to do that?"  Once you start using
one, on the other hand, it's easy to find out what the project's
status is: just look at the open tickets, and at those that have been
closed recently.  You can use this to create agendas for your [status
meetings](#meetings), and to remind yourself what you were doing three
months ago when the time comes to write your [final
report](#the-final-report).

Of course, a ticketing system is only as useful as what you put into
it.  If you're describing a bug in a large application, you should
include enough information to allow someone (possibly yourself two
weeks from now) to reproduce the problem, and someone else to figure
out how urgent the bug is, who should work on it, and what other parts
of the application might be affected by a fix.  This is why
industrial-strength ticketing systems like [Bugzilla][bugzilla] have
upwards of two dozen fields per ticket to record:

- what version of the software you were using

- what platform it was running on;

- what you did to make it crash;

- any data or configuration files the program relies on;

- whatever stack traces, error reports, or log messages the
  program produced

- its severity (i.e., how much damage the bug might do);

- its priority (how urgently the bug needs to be fixed); and

- other tickets that might be related.

This is a lot more information than student projects require.  In
addition, students are almost always working on several courses at
once, and it's common for students to have to put their team project
aside for a few days to work on assignments for other courses.  For
these reasons, I've found that most student teams won't actually use
anything more sophisticated than a web-base to-do list unless they're
forced to by the course's grading scheme.  In that case, most come
away with the impression that tickets are something you only use when
you have to, rather than a vital team coordination tool.

{% include links.md %}
