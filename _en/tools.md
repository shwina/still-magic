---
title: "Other Tools"
undone: true
questions:
- "FIXME"
objectives:
- "FIXME"
keypoints:
- "FIXME"
---

The next most important tool after a version control system is your
editor.  There are literally thousands to choose from; if you want a
plain text editor, your choices range from the very small (such as
Pico, which is included in most Linux installations) to the very large
(like Emacs, whose name doesn't actually stand for "eighty
megabytes and constantly swapping", and which isn't actually a
Lisp-based operating system in disguise).  There are also editors that
understand the syntax of particular file formats, and can
automatically indent text, complete phrases, and colorize the stuff
you're typing: JEdit for Java, Amaya for HTML, and many
others.  Finally, there are WYSIWYG tools like Microsoft Word
and LibreOffice; these usually *can't* be used for
programming, since they insert non-ASCII characters and formatting
information in files (even files that look unformatted).

You probably already have a favorite editor.  If you're like most
programmers, you will change jobs, languages, operating systems, and
nationality before you'll switch to another, because it's taken weeks
or months for your hands to master the current one.  However, if your
editor doesn't pass the following tests, switching now will save you
enough time and grief in the future to make the temporary loss of
productivity worthwhile:

Is it kind to your wrists?
:   I was an Emacs power user for many years, and have paid a heavy
    price for it: I can't type for more than half an hour now before my
    hands start to hurt from all those control-key combinations and long
    reaches for the escape key.  If ergonomics was a standard part of
    the undergraduate curriculum, programming editors would probably be
    used as examples of bad design.

Is it portable?
:   I'm writing this on Windows; an hour from now I'll be using my Mac
    laptop, and on Monday I'll be back on a Linux machine at work.  I
    don't know what I'll be using next year; what I'm sure of is that I
    won't want to have to retrain my hands to use it.  The moral is,
    pick an editor that's portable.  In practice, that means one that is
    open source: you don't want to have to trust other people to care
    about the platforms you do.

Is it syntax-aware?
:   Human beings shouldn't have to indent code, or count parentheses to
    make sure they have closed all the ones they opened.  They equally
    shouldn't have to type every character in the name of every function
    or method they call: their editor should do these things for them.
    This won't just save wear and tear on your wrists: letting the
    machine do it will make the text you create more uniform, and hence
    more readable.

Is it programmable?
:   Just like spreadsheets, games, and other applications, editors are
    built out of functions.  Good ones let you call those functions
    yourself, so that you can write small programs (usually called
    "macros") to automate common operations. For example, back in my
    Emacs power user days, I could type escape-X, "cfl" (for "C for
    loop"), "i", and "N", and my editor would insert:

        for (i=0; i<N; i++) {
            _
        }

    (The underscore shows where the cursor was left.)  I also had macros
    to reformat the spacing in functions, keep track of how many lines
    of code I'd added or removed, and many other tasks.  I'll return to
    this idea below; what's important is that as a programmer, you have
    the skills to make your tools do more than their creators intended,
    so you should find tools that allow you to.

Does it handle Unicode characters?
:   Most programmers don't speak English as a first language, and spell
    their names using symbols that aren't in the old 7-bit ASCII
    character set.  Programming languages haven't caught up yet---they
    still insist on using `<=`, for example---but at the very least, you
    have to be able to edit data and documentation (including comments
    in code) that include Greek, Tamil, and the like. (See
    [Spolsky2003] for a developer-oriented introduction
    to character sets in general, and Unicode in particular.)

A **symbolic debugger** is a program that allows you to control and
inspect the execution of another program.  You can step through the
target program a line at a time, display the values of variables or
expressions, look at the call stack, or (my personal favorite) set
**breakpoints** to say "pause the program when it reaches this
line". Depending on the language you're using, you may have to compile
your program with certain options turned on to make it debuggable, but
that's a small price to pay for the hours or days a debugger can save
you when you're trying to track down a problem.

Some debuggers, like GDB, are standalone programs; others are
build into IDEs.  Both are better than adding `print` statements to
your program, recompiling it, and re-running it, because:

- adding `print` statements takes longer than clicking on a line and
  setting a breakpoint;

- adding `print` statements distorts the code you're debugging by
  moving things around in memory, altering the flow of control, and/or
  changing the timing of thread execution; and

- it's all too easy to make a mistake in the `print` statement---few
  things are as frustrating as wasting an afternoon debugging a
  problem, only to realize that the `print` statement you copied and
  pasted isn't displaying the values you thought it was.

A company I used to work for never hired people immediately.  Instead,
prospective employees were put on a three-month contract.  This gave
us a chance to see how well they worked, and them a chance to see if
they actually wanted to work with us.

Two things meant automatic disqualification in the assessment at the
end of those three months: checking broken code into version control,
and using `print` statements instead of a symbolic debugger.  The
first was justified because we didn't want to hire people who put
themselves ahead of their teammates.  The second was justified because
we didn't want to hire people who were too stupid or stubborn to
program efficiently.

Over the years, I've been surprised by how strongly some programmers
resist using a debugger.  The reason can't be the five or ten minutes
it takes to learn how to use one---that pays for itself almost
immediately.  The only explanation I've been able to come up with is
that some people *enjoy* being inefficient.  Typing in
`print` statements and paging through screens of output lets them
feel like they're being productive, when in fact they're just being
busy (which isn't the same thing at all).  If your brain needs a break
(which it sometimes will), then take a break: stretch your legs, stare
out a window, practice your juggling, or do whatever else you can to
take your mind away from your problem for a few minutes.  Don't drag
out the process of finding and fixing your bug by using sloppy
technique just to let your brain idle for a while.

And by the way: if you're allowed to choose your teammates at the
start of the course, treat it like a job interview.  Ask the people
you think you might want to work with whether they use a debugger.  If
they say "no", ask yourself what impact that's going to have on your
grade in the course...

A smart editor, a build system, and a debugger, all talking to one
another: that's a pretty good description of an **integrated
development environment**, or IDE.  These were invented in the 1970s,
but didn't really catch on until Borland released Turbo Pascal in the
1980s. (Its inventor, Anders Hejlsberg, went on to design C#, which
also shows how far a good tool can take you.)  Along with the tools
described above, modern IDEs usually include:

- a **code browser** that displays an overview of the packages,
  classes, methods, and data in your program;

- a **GUI designer** that lets you build GUIs by dragging and dropping
  components;

- an **interactive prompt** so that you can type in expressions or
  call functions and see the results without having to start (or
  restart) your program;

- a **style checker** that can warn you when your code doesn't meet
  naming and indentation conventions;

- some **refactoring tools** to help you reorganize your code; and

- a **test runner** to display the results of tests, and let you jump
  directly to ones that have failed.

In short, an IDE is to programming what a well-equipped workbench is
to a carpenter.  The most popular one among open source developers is
undoubtedly Eclipse , which has hundreds of plugins of varying
quality to support database design, reverse engineering, a dozen
different programming languages, and more.  Microsoft Visual
Studio is still my personal favorite, largely because of how well its
debugger handles multithreaded programs; as of May 2007, the Express
Edition is still free.

There are dozens of others, any of which will make you more productive
than their disconnected counterparts.  Since most of these store
project data (including build instructions) in a proprietary format,
your team will do much better if you all adopt the same IDE.  This
will also let you help one another solve problems and share
plugins. (Having to agree on *which* IDE to use may be another reason
why some programmers resist adopting any IDE at all, since they
require even more investment to master than editors.)

FIXME: add profiling.

FIXME: add cron or equivalents.

{% include links.md %}
