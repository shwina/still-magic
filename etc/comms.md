---
permalink: "/en/comms/"
title: "Communication"
undone: true
objectives:
- "FIXME"
keypoints:
- "FIXME"
---

Tickets are the best way to keep track of where you are, but there are
lots of other ways the team can and should communicate.  The most
popular is easily *email*, which has been used to run projects
since the 1970s.  It brings content directly to people while allowing
everyone to deal with issues when it's convenient for them, and
supports long-running conversations.  Email really comes into its own,
though, when messages are routed through a central mailing list, so
that people don't have to remember to CC the other five people on
their team, and a shared archive can be created for later searching.
The second point is as important as the first: if you can't go back
and find out what was said a month ago---or, just as importantly, if
someone *else* can't do that---you might as well not have said
it.

*Wikis* seem like a good way to keep notes, create documentation,
and so on.  Their strengths are a syntax that's (a little) simpler
than HTML, and the fact that content is automatically and immediately
visible on the web.  In practice, you'll probably get as much mileage
out of a bunch of HTML pages under version control---you have to set
up a repository anyway, and version control systems are much better at
reconciling conflicts between concurrent authors than wikis.

*Blogs*, on the other hand, have proven more useful.  One kind of
project blog consists of articles written by the team's members as a
journal of their progress.  This is most useful for people who are
watching the project from the outside, like instructors.

The second kind of blog is one created automatically by tools.  In
[drproject][drproject], for example, every project has a blog called its
**event log**.  Every time someone checks code into version
control, creates or closes a ticket, or sends email, an entry is added
to the event log.  This allows the project's members to see changes
scroll by in their usual blog reader, which is a handy way to keep
track of what their teammates are doing.

The problem with blogs, at least right now, is that the RSS family of
standards that blogging relies on does not provide for authentication:
there's no uniform way for blog readers to pass credentials like
passwords to blog sites.  In practice, this means that blogs have to
be open for everyone to read.  This is OK for open source projects,
but it's problematic for students, since instructors usually don't
want Team A to be able to see what Team B is doing, and vice versa.
Emerging standards like [OpenID][openid] may eventually solve this
problem, but for now, per-project blogs are something that instructors
have to think about very carefully.

Finally, there's *instant messaging*.  I realize it's the
communication medium of choice for all you hip young things, but I'm
not a fan:

- IM is the most effective method ever invented for disrupting the
  state of flow that is so essential to
  [productivity](#time-management).

- Most chat systems don't provide "always-on" chat rooms ([IRC][irc]
  being a notable exception), so every time you want to talk to all
  your teammates, you have to round them up.

- Most IM systems don't archive conversations in the way that mailing
  lists do, so participants have to save the chat on their personal
  machines, then upload it to the project's site.  In my experience,
  that's just enough trouble for most people to never get around to
  doing it...

- IM conversations tend to be permanently out of phase: if you ask,
  "Can we move on to the next item?", and someone doesn't say either
  "yes" or "no", what usually happens is that you wait a minute, then
  move on, and then they pop up with a lengthy comment on the
  preceding item.

I think these faults can all be fixed, but until they are---oh, who am
I kidding?  You're going to use IM no matter what I say.  If there's
more than two people in the conversation, follow the same rules you
would for a meeting.  In particular, post a summary of the
conversation to your project's web site, just as you would post
meeting minutes.  And if you want to figure out how to make IM a
productivity enhancer, please send me email: I'm always looking for
good graduate students.

{% include links.md %}
