---
permalink: "/en/testability/"
title: "Testability"
undone: true
objectives:
- "FIXME"
keypoints:
- "FIXME"
---

Test-driven development's advocates claim that writing tests first helps keep people honest,
clarify requirements,
ensure that code is actually testable,
and avoid confirmation bias.
In other words,
if you write tests *after* you write code you are less likely to actually write them,
more likely to miss corner cases,
more likely to have written code that's hard to test,
and more likely to look at the output and say, "Yeah, that seems OK."

All of this makes sense,
but empirical studies have found that TDD actually has little effect.
What *does* seem to matter is using very short iterations:
it's better to code and test in alternating ten-minute bursts
than an hour or a day at a time.

When most developers hear the word "design", they think about either
the application's structure or its user interface.  If you don't think
about how you're going to test your application while you're designing
it, though, the odds are very good that you'll build something that
can't (or cannot easily) be tested.  Conversely, if you
**design for test**, it'll be a lot easier to check whether your
finished application actually does what it's supposed to.

For example, let's consider a typical three-tier web site that uses
the Model-View-Controller (MVC) design pattern.  The model, which is
stored in a relational database, is the data that the application
manipulates, such as purchase orders and game states.  The controller
layer encapsulates the application's business rules: who's allowed to
cancel games while they're in progress, how much interest to add on
out-of-province orders, and so on.  Finally, the view layer translates
the application's state into HTML for display to the user.

This architecture presents (at least) three challenges from the point
of view of testing:

- Unit testing libraries like [JUnit][junit] (and its clones in other
  languages) aren't built to handle this: as the word "library"
  implies, they're made up of code that's meant to be called *within*
  a process.  Despite the ubiquity of multi-process applications, most
  debuggers and testing libraries cannot track "calls" *between*
  processes.

- Configuring a test environment is a pain: you have to set up a
  database server, clear the browser's cache, make sure the right
  clauses are in your Apache configuration file, and so on.

- Running tests is slow. In order to ensure that tests are
  independent, you have to create an entirely new fixture for each
  test.  This means reinitializing the database, restarting the web
  server, and so on, which can take several seconds *per test*. That
  translates into an hour or more for a thousand tests, which is
  pretty much a guarantee that developers won't run them routinely
  while they're coding, and might not even run them before checking
  changes in.

The first step in fixing this is to get rid of the browser and web
server. One way to do this is to replace the browser with a script
that generates HTTP requests as multi-line strings and passes them to
a "fake CGI" library via a normal function call.  After invoking our
actual program, the fake CGI library passes the text of an HTTP
response back to our script, which then checks that the right values
are present (about which more in a moment). The "fake CGI" library's
job is to emulate the environment the web app under test would see if
it was being invoked as a CGI by Apache: environment variables are
set, standard input and output are replaced by string I/O objects, and
so on, so that the web app has no (easy) way of knowing that it's
being invoked via function call, rather than being forked.

Why go through this rigmarole? Why not just have a top-level function
in the web app that takes a URL, a dictionary full of header keys and
values, and a string containing the POST data, and check the HTML page
it generates? The answer is that structuring our tests in this way
allows us to run them both in this test harness, and against a real
system. By replacing the fake CGI adapter with code that sends the
HTTP request through a socket connected to an actual web server, and
reads that server's response, we can check that our application still
does what it's supposed to when it's actually deployed. The tests will
run much more slowly, but that's OK: if we've done our job properly,
we'll have caught most of the problems in our faked environment, where
debugging is much easier to do.

Now, how to check the result of the test? We're expecting HTML, which
is just text, so why not store the HTML page we want in the test and
do a string comparison? The problem with that literal approach is that
every time we make any change at all to the format of the HTML, we
have to rewrite every test that produces that page.  Even something as
simple as introducing white space, or changing the order of attributes
within a tag, will break string comparison.

A better strategy is to add unique IDs to significant elements in the
HTML page, and only check the contents of those elements. For example,
if we're testing login, then somewhere on the page there ought to be
an element like this:

```
<div id="currentuser">Logged in as <strong>gvwilson</strong>
(<a href="http://www.drproject.org/logout">logout</a>
|
<a href="http://www.drproject.org/preferences">preferences</a>)
</div>
```

We can find that pretty easily with an **XPath** query, or by crawling
the DOM tree produced by parsing the HTML ourselves (assuming we're
generating well-formed HTML, which we should be).  We can then move
the `div` around without breaking any of our tests; if we were a
little more polite about formatting its internals (i.e., if we used
something symbolic to highlight the user name, and trusted CSS to do
the formatting), we'd be in even better shape.

We've still only addressed half of our overall problem, though: our
web application is still talking to a database, and reinitializing it
each time a test runs is sloooooooow.

We can solve this by moving the database into memory.  Most
applications rely on an external database server, which is just a
long-lived process that manages data on disk. An increasingly-popular
alternative is the *embedded* database, in which the database
manipulation code runs inside the user's application as a normal
library.  [Berkeley DB][bdb] (now owned by [Oracle][oracle]) and
[SQLite][sqlite] (still open source) are probably the best known of
these; their advocates claim they are simpler to build and faster to
run, although there are lots of advantages to using servers as well.

The advantage of embedded databases from a testing point of view is
that they can be told to store data in memory, rather than on
disk. This would be a silly thing to do in a production environment
(after all, the whole point of a database is that it persists), but in
a testing environment, it can speed things up by a factor of a
thousand or more, since the hard drive never has to come into
play. The cost of doing this is that you have to either commit to
using one database in both environments, or avoid using the
"improvements" that different databases have added to SQL.

Once these changes have been made, the application zips through its
tests quickly enough that developers actually will run the test suite
before checking in changes to the code. The downside is the loss of
**fidelity**: the system we're testing is a close cousin to what
we're deploying, but not exactly the same. However, this is a good
economic tradeoff: we may miss a few bugs because our fake CGI layer
doesn't translate HTTP requests exactly the same way Apache and
Python's libraries do, but we catch (and prevent) a lot more by making
testing cheap.

This example just scratches the surface of designing for testability.
If you want to go further, [[Meszaros2007](#meszaros2007)] includes
some good discussion of how to make things more testable, and in 2007,
Michael Bolton posted a fairly complete list of things developers can
do to the Agile Testing list:

- scriptable interfaces to the product, so that we can drive it more
  easily with automation

- logging of activities within the program

- monitoring of the internals of the application via another window or
  output over the network

- simpler setup of the application

- the ability to change settings or configuration of the application
  on the fly

- clearer error/exception messages, including unique identifiers for
  specific points in the code, or *which* damn file was not found

- availability of modules separately for earlier integration-level
  testing

- information about how the system is intended to work (ideally in the
  form of conversation or "live oracles" when that's the most
  efficient mode of knowledge transfer)

- information about what has already been tested (so we don't repeat
  someone else's efforts)

- access to source code for those of us who can read and interpret
  it

- improved readability of the code (thanks to pairing and
  refactoring)

- overall simplicity and modularity of the application

- access to existing ad hoc (in the sense of "purpose-built") test
  tools, and help in creating them where needed

- proximity of testers to developers and other members of the project
  community

Adam Goucher added two more:

- a "stub mode" where you can test a module without needing another
  module reading/working

- information about what has changed since the last code delivery in
  order to better target testing

Of these, numbers 2, 6, 7, 9, and 15 are the most important for
students' projects; most of the others only really come into play when
you're building something very large, or have a team that's so big
that it has to be broken down into functional groups.  That said,
they're all still good ideas at every level of development.

{% include links.md %}
