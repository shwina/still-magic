---
title: "Including Everyone"
undone: true
questions:
-   "Why should I make my project welcoming for everyone?"
-   "Why do I need a license for my work?"
-   "What license should I use for my work?"
-   "How should I tell people what they can and cannot do with my work?"
-   "Why should my project have an explicit Code of Conduct?"
-   "How can I be a good ally?"
objectives:
-   "Explain the purpose of a Code of Conduct and the essential features an effective one must have."
-   "Explain why adding licensing information to a repository is important."
-   "Explain differences in licensing and social expectations."
-   "Choose an appropriate license."
-   "Explain where and how to communicate licensing."
-   "Explain steps a project lead can take to be a good ally."
keypoints:
-   "Create an explicit Code of Conduct for your project modelled on the Contributor Covenant."
-   "Be clear about how to report violations of the Code of Conduct and who will handle such reports."
-   "People who are not lawyers should not try to write licenses."
-   "Every project should include an explicit license to make clear who can do what with the material."
-   "People who incorporate GPL'd software into their own software must make their software also open under the GPL license; most other open licenses do not require this."
-   "The Creative Commons family of licenses allow people to mix and match requirements and restrictions on attribution, creation of derivative works, further sharing, and commercialization."
-   "Be proactive about welcoming and nurturing community members."
---

The previous lesson talked about the physical organization of projects.
This one talks about the social structure,
which is more important to the project's success.
A project can survive badly-organized code;
none will survive for long if people are confused,
pulling in different directions,
or hostile.
This lesson therefore talks about what projects can do to make newcomers feel welcome
and to make things run smoothly after that.
It draws on [Foge2005](#BIB),
which describes how good open source software projects are run,
and on [Boll2014](#BIB),
which explains what a [commons](#g:commons) is and when it's the right model to use.

## Why does a project need explicit rules? {#s:inclusive-rules}

Jo Freeman's influential essay
"[The Tyranny of Structurelessness][tyranny-structurelessness]" pointed out that
every group has a power structure;
the only question is whether it is formal and accountable
or informal and unaccountable [Free1972](#BIB).
Thirty-five years after the free software movement took on its modern, self-aware form,
its successes and failures have shown that if a project doesn't clearly state
who has the right to do what,
it will wind up being run by whoever argues loudest and longest.

## How should I license my software? {#s:inclusive-software-license}

If the law or a publication agreement prevents people from reading your work or using your software,
you're excluding them
(and probably hurting your own career).
You may need to do this in order to respect personal or commercial confidentiality,
but the first and most important rule of inclusivity
is to be open by default.

However,
that is easier said than done,
not least because the law hasn't kept up with everyday practice.
[Mori2012](#BIB) and [this blog post][vanderplas-licensing] are good starting points from a scientist's point of view,
while [Lind2008](#BIB) is a deeper dive for those who want details.
In brief,
creative works are automatically eligible for intellectual property (and thus copyright) protection.
This means that every creative work has some sort of license:
the only question is whether authors and users know what it is.

Every project should therefore include an explicit license.
This license should be chosen early:
if you don't set it up right at the start,
then each collaborator will hold copyright on their work
and will need to be asked for approval when a license *is* chosen.
By convention,
the license is usually put in a file called `LICENSE` or `LICENSE.txt` in the project's root directory.
This file should clearly state the license(s) under which the content is being made available;
the plural is used because code, data, and text may be covered by different licenses.

> *Don't write your own license*,
> even if you are a lawyer:
> legalese is a highly technical language,
> and words don't mean what you think they do.

To make license selection as easy as possible,
GitHub allows you to select one of the most common licenses when creating a repository.
The Open Source Initiative maintains [a list of licenses][osi-license-list],
and [choosealicense.com][choose-license] will help you find a license that suits your needs.
Some of the things you will need to think about are:

1.  Do you want to license the code at all?
2.  Is the content you are licensing source code?
3.  Do you require people distributing derivative works to also distribute their code?
4.  Do you want to address patent rights?
5.  Is your license compatible with the licenses of the software you depend on?
    For example, as we will discuss below,
    you can use MIT-licensed code in a GPL-licensed project but not vice versa.

The two most popular licenses for software are
the [MIT license](#g:mit-license) and the [GNU Public License](#g:gpl) (GPL).
The MIT license (and its close sibling the BSD license)
say that people can do whatever they want to with the software as long as they cite the original source,
and that the authors accept no responsibility if things go wrong.
The GPL gives people similar rights,
but requires them to share their own work on the same terms:

> You may copy, distribute and modify the software as long as you track changes/dates in source files.
> Any modifications to or software including (via compiler) GPL-licensed code must also be made available under the GPL
> along with build & install instructions.
>
> --- [tl;dr][tldr-gpl]

We recommend the MIT license:
it places the fewest restrictions on future action,
it can be made stricter later on,
and the last thirty years shows that it's good enough to keep work open.

## How should I license my data and reports? {#s:inclusive-software-text}

The MIT license and the GPL apply to software.
When it comes to data and reports,
the most widely used family of licenses are those produced by [Creative Commons][creative-commons],
which have been written and checked by lawyers and are well understood by the community.

The most liberal license is referred to as [CC-0](#g:cc-0),
where the "0" stands for "zero restrictions".
CC-0 puts work in the public domain,
i.e.,
allows anyone who wants to use it to do so however they want with no restrictions.
This is usually the best choice for data,
since it simplifies aggregate analysis.
For example,
if you choose a license for data that requires people to cite their source,
then anyone who uses that data in an analysis must cite you;
so must anyone who cites *their* results,
and so on,
which quickly becomes unwieldy.

The next most common license is the Creative Commons - Attribution license,
usually referred to as [CC-BY](#g:cc-by).
This allows people to do whatever they want to with the work
as long as they cite the original source.
This is the best license to use for manuscripts,
since you *want* people to share them widely
but also want to get credit for your work.

Other Creative Commons licenses incorporate various restrictions on specific use cases:

-   ND (no derivative works) prevents people from creating modified versions of your work.
    Unfortunately, this also inhibits translation and reformatting.
-   NC (no commercial use) does *not* mean that people cannot charge money for something that includes your work,
    though some publishers still try to imply that in order to scare people away from open licensing.
    Instead,
    the NC clause means that people cannot charge for something that uses your work without your explicit permission,
    which you can give under whatever terms you want.
-   Finally,
    SA (share-alike) requires people to share work that incorporates yours
    on the same terms that you used.
    Again,
    this is fine in principle,
    but in practice makes aggregation a headache.

## Why Should I Establish a Code of Conduct for My Project? {#s:inclusive-conduct}

-   FIXME: [Auro2018](#BIB)
-   A CoC lays out the expectations for personal interaction in your project
    -   Explicitly communicate standards to which this project holds its participants
    -   Encourages newcomers to engage with the project
-   Important to make clear how to report and who handles
    -   Without that, it's meaningless
-   We recommend the [Contributor Covenant][covenant]
    -   Provides examples of acceptable and unacceptable behavior for your project
    -   Specifies how unacceptable behavior will be handled
    -   Specifically designed for project contributors rather than conference participants
    -   Use the [model code of conduct][model-coc] from the [Geek Feminism Wiki][geek-feminism] for in-person events
-   Reduces the uncertainty that project participants face about what is acceptable and unacceptable behavior
    -   While you might think this is obvious,
        long experience suggests that articulating it clearly and concisely reduces problems caused by have different expectations
    -   You don't expect to have a fire, but every large building or event should have a fire safety plan
-   Welcomes newcomers specifically, which can help grow your project and encourage user feedback
    -   Particularly important for people from marginalized groups, who have probably experienced harassment or unwelcoming behavior before
    -   Having a CoC signals that your project is trying to be a better place than YouTube, Twitter, and other cesspools
-   It delineates responsibilities within the project and provides specific points of contact in case of misconduct or harassment,
    as well as specifying the process to be followed in these cases
-   Some people may (still) push back claiming that it's unnecessary, or that it infringes freedom of speech, or...
    -   What they really mean is that thinking about unfairness that may have benefited from makes them uncomfortable
    -   In our experience, that is also a very useful filter on contributors...

## How Can I Be a Good Ally for Members of Marginalized Groups? {#s:inclusive-ally}

-   Drawn primarily from [Frameshift Consulting Ally Skills Workshop][ally-skills]
    -   Which you should attend if you can
-   Privilege: an unearned advantage given by society to some people but not all
-   Oppression: systemic, pervasive inequality that benefits the privileged and harms those without privilege
-   Target: someone who suffers from oppression
    -   Often called "a member of a marginalized group", but that phrasing is deliberately passive
    -   Targets don't choose to be marginalized: those with privilege marginalize them
-   Ally: a member of a privileged group who is working to understand their own privilege and end oppression
-   Example
    -   Privilege: being able to walk into a store and have the owner assume you're there to buy things, not to steal them
    -   Oppression: the self-perpetuating stories told about (for example) indigenous people being thieves,
        and the actions people take as a result of them
    -   Target: an indigenous person who wants to buy milk
    -   Ally: a white person who pays attention to lesson like this one (raising their own awareness),
        calls out peers who spread racist stories (peer action),
        or asks the shopkeeper whether they should leave too (situational action)
-   Why be an ally?
    -   Because you can:
        taking action to value diversity results in worse performance ratings for minority and female leaders,
        while ethnic majority or male leaders who do this aren't penalized [Hekm2017](#BIB)
    -   Because you have benefited, even if you don't realize it
    -   As soon as you acknowledge that (for example) women are called on less often than men,
        or are less likely to get an interview or a publication given identical work,
        you have to acknowledge that white and Asian males are *more* likely to get these benefits than their performance alone deserves
    -   See discussion above about willingness or refusal to acknowledge this being a good filter on project participants
1.  Be short, simple, firm
1.  Don't try to be funny
1.  Play for the audience
1.  Practice simple responses
1.  Pick your battles
1.  Don't shame or insult one group when trying to help another
    -   E.g., don't call someone ugly or stupid when what you really mean is that they're racist or homophobic
-   [Captain Awkward][captain-awkward] has useful advice
-   [Charles' Rules of Argument][charles-rules] are very useful online
    1.  Don't go looking for an argument
    1.  State your position once, speaking to the audience
    1.  Wait for absurd replies
    1.  Reply once more to correct any misunderstandings of your original statement
    1.  Do not reply again - go do something fun instead
-   Recognize that good principles sometimes conflict
    -   "A manager consistently uses male pronouns to refer to software and people of unknown gender.
        When you tell them it makes you uncomfortable to treat maleness as the norm,
        they say that male is the default gender in their first language
        and you should be more considerate of people from other cultures."
    -   Respect for other cultures vs. being inclusive of women
    -   In this case, discomfort of changing pronouns is less than career harm caused by being exclusionary
-   Change the terms of the debate
    -   "Why should we take diversity into account when hiring? Why don't we just hire the best candidate?"
    -   Because taking diversity into account *is* hiring the best candidate
    -   If you can run a mile in four minutes, and I can do it in 4:15 with a ball and chain on my leg, which one of us is the better athlete?
    -   Which one of us will perform better *if the impediment is removed*?
    -   So sure, if you intend to preserve an exclusionary culture in this lab,
        considering how much someone has achieved despite systemic unfairness might not make sense,
        but you're not arguing for that, are you?

## Summary {#s:inclusive-summary}

FIXME: create concept map for making an inclusive project

{% include links.md %}
