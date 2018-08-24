---
permalink: "/en/publish/"
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

-   Now that we know *how* to publish ([s:ghp](#CHAPTER)), the next questions are *what* and *where*
-   Use the generic term "report" to include research papers, summaries for clients,
    and everything else that is shorter than a book and is going to be read by someone else
    -   "A report is a PDF you would print on your own printer."

## What to Publish and Where {#s:publish-what-where}

-   Small raw data (under 500 MB): store in GitHub
-   Medium-size raw data (between 500 MB and 5 GB)
    -   Use platforms like the [Open Science Framework][osf], [Dryad][dryad], and [Figshare][figshare]
    -   Include dataset identifiers and/or download scripts with the report
-   Big raw data (more than 5 GB)
    -   May not be yours in the first place, and needs professional archiving
    -   Again, include identifiers or download scripts
-   Whichever you use, get or create a [DOI](#g:doi) for each version of each dataset ([s:publish-identifiers](#SECTION))
-   Also publish intermediate files that take a long time to generate
    -   Same sizing rules as above
    -   If they're likely to be used by other people or in other reports, get a DOI
-   Publish the version IDs of the standard software used in the analysis
    -   `pip freeze > requirements.txt` for Python packages ([s:packages-install](#SECTION))
    -   Helps to write a script to get versions for everything else
    -   Or put commands in a Makefile

```
## versions : dump versions of everything used in this run
versions :
        @echo '# Python packages'
        @pip freeze
        @echo '# dezply'
        @dezply --version
        @echo '# parajune'
        @parajune --status | head 1
```

-   The scripts, notebooks, and/or Makefiles used to produce results
    -   These tend to evolve at a different rate than data, so get separate DOIs
    -   May publish script by script, or create a Zipfile or tar file that includes everything
    -   The Makefile fragment below creates `~/archive/meow-2018-08-21.tgz`

```
ARCHIVE=${HOME}/archive
PROJECT=meow
TODAY=$(shell date "+%Y-%m-%d")
SCRIPTS=./Makefile ./bin/*.py ./bin/*.sh

## archive : create an archive of all the scripts used in this run
archive :
        @mkdir -p ${ARCHIVE}
        @tar zcf ${ARCHIVE}/${PROJECT}-${TODAY}.tgz
```

-   The configurations and parameters used for that software
    -   If all parameters are in a configuration file, use that ([s:configuration](#CHAPTER))
    -   Or log all configuration parameters and use `grep` or a script to extract from the logfile ([s:logging](#CHAPTER))

### Common Problems

FIXME: common problems for what to publish and where

### Exercises

FIXME: create exercises for what to publish and where

## ORCIDs and DOIs {#s:publish-identifiers}

-   An [ORCID](#g:orcid) is an Open Researcher and Contributor ID
    -   Because names and affiliations change
-   Can [get an ORCID][orcid] for free and include in publications
    -   Greg Wilson's is 0000-0001-8659-8979
-   A [DOI](#g:doi) is a Digital Object Identifier
    -   Uniquely identifies a particular version of a particular digital artefact
    -   Can be a report, a dataset, or a version of software
    -   Format is `doi:prefix/suffix`, but will often see URLs like `http://dx.doi.org/prefix/suffix`
-   Use [Zenodo][zenodo] to [get DOIs for free][github-zenodo-tutorial]
-   Log in to [Zenodo][zenodo] using GitHub ID
    -   Authorize application (so Zenodo can read data from your GitHub repositories)
    -   Pick a repository and click the "On" button
-   Go back to GitHub repository
    -   Go to the "Releases" tab
    -   Create a new release and give it a version number ([s:workflow-tag](#SECTION))
    -   Click "Publish release"
-   Go back to Zenodo
    -   Look under the "Upload" tab for a new upload corresponding to this release
    -   Fill in information and publish
    -   Zenodo DOI badge will automatically appear on the GitHub project's site
-   Cite datasets and software versions in reports
    -   Include DOIs in bibliography entries
-   Publish software in [JOSS][joss] or [F1000 Research][f1000-research]
-   Publish *everything* in open access venues ([s:inclusive-license](#SECTION))
    -   Use [Unpaywall][unpaywall] browser extension to check and find things

### Common Problems

FIXME: common problems for ORCIDs and DOIs

### Exercises

FIXME: create exercises for ORCIDs and DOIs

## FAIR {#s:publish-fair}

-   The [FAIR Principles][go-fair] describe what research data should look like
    -   Still mostly aspirational for most researchers
    -   But it tells us what we need to work on
    -   And yes, the acronym probably came first...
-   Findable: because the first step in using or re-using data is to find it
    1.  (Meta)data is assigned a globally unique and persistent identifier
    2.  Data is described with rich metadata
    3.  Metadata clearly and explicitly includes the identifier of the data it describes
    4.  (Meta)data is registered or indexed in a searchable resource (FIXME: such as?)
-   Accessible: you can't use data if you don't have access to it (which means a way to authenticate, and having permission)
    1.  (Meta)data is retrievable by its identifier using a standardised communications protocol
        -   The protocol is open, free, and universally implementable
        -   The protocol allows for an authentication and authorisation procedure if necessary
    2.  Metadata is accessible even when the data is no longer available
-   Interoperable: data usually needs to be integrated with other data, which means that tools need to be able to process it
    1.  (Meta)data uses a formal, accessible, shared, and broadly applicable language for knowledge representation
    2.  (Meta)data uses vocabularies that follow FAIR principles
    3.  (Meta)data includes qualified references to other (meta)data
-   Reusable: because this is the ultimate purpose of all of this
    1.  Meta(data) is described with accurate and relevant attributes
    2.  (Meta)data is released with a clear and accessible data usage license
    3.  (Meta)data has detailed provenance
    4.  (Meta)data meets domain-relevant community standards
-   In practice:
    -   Always use [tidy data](#g:tidy-data)
    -   Include keywords in the project's `README.md` so that they appear on its home page
    -   Give everything DOIs
    -   Put data in open repositories
    -   Use well-known formats like CSV and HDF5
    -   Include an explicit license in every project and every dataset
    -   Include scripts or documentation on how to get or regenerate data
    -   Include units (please)

### Common Problems

FIXME: common problems for FAIR Principles

### Exercises

FIXME: create exercises for FAIR Principles

## Summary {#s:publish-summary}

FIXME: create concept map for publishing

{% include links.md %}
