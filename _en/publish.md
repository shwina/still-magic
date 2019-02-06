---
title: "Publishing"
questions:
-   "How and where should I publish my reports?"
-   "What should I include in my publications?"
objectives:
-   "Explain what to include in publications, and where to publish large, medium, and small datasets."
-   "Explain what DOIs and ORCIDs are."
-   "Get an ORCID."
-   "Describe the FAIR Principles and determine whether a dataset conforms to them."
-   "Obtain DOIs for datasets, reports, and software packages."
keypoints:
-   "Include small datasets in repositories; store large ones on data sharing sites, and include metadata in the repository to locate them."
-   "An ORCID is a unique personal identifier that you can use to identify your work."
-   "A DOI is a unique identifier for a particular dataset, report, or software release."
-   "Data should be findable, accessible, interoperable, and reusable (FAIR)."
-   "Use Zenodo to obtain DOIs."
-   "Publish your software as you would a paper."
---

[s:ghp](#REF) discussed how to publish;
the next questions are what and where.
This lesson therefore looks at what should be included in reports and how best to do that.
We use the generic term "report" to include research papers,
summaries for clients,
and everything else that is shorter than a book and is going to be read by someone else.

Our motivation is summed up in this quotation:

> An article about computational science in a scientific publication is *not* the scholarship itself,
> it is merely *advertising* of the scholarship.
> The actual scholarship is the complete software development environment
> and the complete set of instructions which generated the figures.
>
> -- Jonathan Buckheit and David Donoho, paraphrasing Jon Claerbout, in [Buck1995](#BIB)

While some things can't be published without violating personal or commercial confidentiality,
every researcher's default should be to make their work as widely available as possible.
That means publishing it in an open access venue ([s:inclusive-license](#REF))
so that people who aren't in academia can find it and read it.
Software can be published in [JOSS][joss] or [F1000 Research][f1000-research],
and you can use the [Unpaywall][unpaywall] browser extension
to find what other people have been willing to share.

## What is the most useful way to share my data? {#s:publish-share}

Making data useful to other people (including your future self)
is one of the best investments you can make.
The simple version of how to do this is:

-   Always use [tidy data](#g:tidy-data).
-   Include keywords describing the data in the project's `README.md`
    so that they appear on its home page and can easily be found by search engines.
-   Give every dataset and every report a unique identifier ([s:publish-identifiers](#REF)).
-   Put data in open repositories ([s:publish-data](#REF)).
-   Use well-known formats like CSV and HDF5.
-   Include an explicit license in every project and every dataset.
-   Don't just describe how to get the data: include scripts that do it.
-   Include units and other metadata.

The last point is often the hardest for people to implement,
since many researchers have never seen a well-documented dataset.
We draw inspiration from the data catalog included in [the repository][womens-pockets-data]
for the article "[Women's Pockets Are Inferior][womens-pockets]"
and include a file `./data/README.md` in every project
that looks like this:

<div class="highlight" markdown="1">
{% include publish/data_catalog.md %}
</div>

The catalog above doesn't include column headers or units because the data isn't tidy.
It *does* include the names of the functions used to reformat that data,
and `./results/README.md` then includes the information that users will want.
One section of that file is shown below:

<div class="highlight" markdown="1">
{% include publish/results_catalog.md %}
</div>

Note that this catalog includes both units and whether or not a field can be NA.
Note also that calling a field "NA" is asking for trouble...

## What standards of data sharing should I aspire to? {#s:publish-fair}

The [FAIR Principles][go-fair] describe what research data should look like.
They are still aspirational for most researchers,
but they tell us what to aim for.
The most immediately important elements of the FAIR Principles are outlined below.

### Data should be *findable*.

The first step in using or re-using data is to find it.
You can tell you've done this if:

1.  (Meta)data is assigned a globally unique and persistent identifier ([s:publish-identifiers](#REF)).
2.  Data is described with rich metadata (like the catalog shown above).
3.  Metadata clearly and explicitly includes the identifier of the data it describes.
4.  (Meta)data is registered or indexed in a searchable resource,
    such as the data sharing platforms described in [s:publish-data](#REF).

### Data should be *accessible*.

You can't use data if you don't have access to it.
In practice,
this rule means the data should be openly accessible (the preferred solution)
or that authenticating in order to view or download it should be free.
You can tell you've done this if:

1.  (Meta)data is retrievable by its identifier using a standard communications protocol like HTTP.
2.  Metadata is accessible even when the data is no longer available.

### Data should be *interoperable*.

Data usually needs to be integrated with other data,
which means that tools need to be able to process it.
You can tell you've done this if:

1.  (Meta)data uses a formal, accessible, shared, and broadly applicable language for knowledge representation
2.  (Meta)data uses vocabularies that follow FAIR principles
3.  (Meta)data includes qualified references to other (meta)data

### Data should be *reusable*.

This is the ultimate purpose of the FAIR Principles and much other work.
You can tell you've done this if:

1.  Meta(data) is described with accurate and relevant attributes.
2.  (Meta)data is released with a clear and accessible data usage license.
3.  (Meta)data has detailed [provenance](#s:provenance).
4.  (Meta)data meets domain-relevant community standards.

## What data should I publish and how? {#s:publish-data}

Small datasets (i.e., anything under 500 MB) can be stored in version control
using the conventions described in [s:project](#REF).
If the data is being used in several projects,
it may make sense to create one repository to hold only the data;
the R community refers to these as [data packages](#s:data-package),
and they are often accompanied by small scripts to clean up and query the data.
Be sure to give the dataset an identifier as discussed in [s:publish-identifiers](#REF).

For medium-sized datasets (between 500 MB and 5 GB),
it's better to put the data on platforms like the [Open Science Framework][osf],
[Dryad][dryad],
and [Figshare][figshare].
Each of these will give the datasets identifiers;
those identifiers should be included in reports
along with scripts to download the data.
Big datasets (i.e., anything more than 5 GB)
may not be yours in the first place,
and probably need the attention of a professional archivist.
Any processed or intermediate data that takes a long time to regenerate
should probably be published as well using these same sizing rules;
all of this data should be given identifiers,
and those identifiers should be included in reports.

## How can I identify my work for citation? {#s:publish-identifiers}

A [Digital Object Identifier](#g:doi) (DOI)
is a unique identifier for a particular version of a particular digital artifact
such as a report, a dataset, or a piece of software.
DOIs are written as `doi:prefix/suffix`,
but you will often also see them represented as URLs like `http://dx.doi.org/prefix/suffix`.

We can use [Zenodo][zenodo] to [get DOIs for free][github-zenodo-tutorial]:

1.  Log in to [Zenodo][zenodo] using your GitHub ID.
    (The first time you do this,
    you will have to authorize the application so that Zenodo can read data from your GitHub repositories.)
    Once you have logged in,
    pick a repository and click the "On" button.
2.  Go back to that GitHub repository and go to the "Releases" tab.
    Create a new release,
    give it a version number (discussed in [s:branches-tag](#REF)),
    and then click "Publish release".
3.  Finally, go back to Zenodo
    and look under the "Upload" tab for a new upload corresponding to this release.
    Once it appears,
    fill in the required information and publish it.
    A Zenodo DOI badge will automatically appear on the GitHub project's site,
    and anyone with the DOI will be able to find it.

FIXME: screenshots and a diagram showing how this process works

## How can I identify myself in my publications? {#s:publish-self}

An [ORCID](#g:orcid) is an Open Researcher and Contributor ID.
You can [get an ORCID][orcid] for free,
and you should include it in publications
because people's names and affiliations change over time.

## What software should I publish and how? {#s:publish-software}

Including a link to a GitHub repository in your publications is a good first step,
but it is only the first step.
Software changes over time,
and your scripts almost certainly depend on specific versions of other packages ([s:package](#REF)).
It therefore seems logical to include the exact version numbers of everything used in your analysis
in each publication,
but that's impractical.
Should you include the version of the compiler used to build the R or Python interpreter you used?
What about the operating system?
Is a hardware specification needed in case it turns out that
[the processor you used had a bug][pentium-div-bug]?
Some people now believe that researchers should put everything in a virtual machine and share that,
but a [Docker][docker] image is like a screenshot:
all the bits are there,
but it's a lot of work to get the information out.

Librarians, publishers, and regulatory bodies are still trying to find
useful answers to these questions.
For the moment,
the best advice we can give it to publish the version IDs of the standard software used in the analysis.
As [s:package-install](#REF) described,
you can get these automatically by running:

```shell
$ pip freeze > requirements.txt
```

For everything else,
you should write a script or create a rule in your project's Makefile ([s:automate](#REF)),
since the commands used to get version numbers will vary from tool to tool:

```make
## versions : dump versions of software.
versions :
        @echo '# Python packages'
        @pip freeze
        @echo '# dezply'
        @dezply --version
        @echo '# parajune'
        @parajune --status | head 1
```

The scripts, notebooks, and/or Makefiles used to produce results
tend to evolve at a different rate than data,
so they should get separate DOIs.
Depending on the size or complexity of the software you have written,
and whether you re-use it in multiple projects,
you may publish script by script
or create a zip file or tar file that includes everything.
For example,
the Makefile fragment below creates `~/archive/meow-2019-02-21.tgz`:

```make
ARCHIVE=${HOME}/archive
PROJECT=meow
TODAY=$(shell date "+%Y-%m-%d")
SCRIPTS=./Makefile ./bin/*.py ./bin/*.sh

## archive : create an archive of all the scripts used in this run
archive :
        @mkdir -p ${ARCHIVE}
        @tar zcf ${ARCHIVE}/${PROJECT}-${TODAY}.tgz
```

Finally,
it's imperative that you include the configuration files
and command-line parameters
that you used to generate particular runs.
If all of the program's parameters are in a configuration file ([s:configure](#REF)),
you can archive that.
Otherwise,
have your program print out its configuration parameters
and use `grep` or a script to extract from the logfile ([s:logging](#REF)).
If you can't do that because you're using someone else's software,
write a small shell script that logs the configuration
and then runs the program.

## Summary {#s:publish-summary}

FIXME: create concept map for publishing

## Exercises {#s:publish-exercises}

FIXME: create exercises for publishing

{% include links.md %}
