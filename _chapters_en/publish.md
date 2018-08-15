---
permalink: "/en/publish/"
title: "Publishing"
questions:
-   "How and where should I publish my reports?"
-   "What should I include in my publications?"
objectives:
-   "Explain what to include in publications, and where to publish large, medium, and small datasets."
-   "Describe the FAIR Principles and determine whether a dataset conforms to them."
-   "Explain what DOIs and ORCIDs are."
-   "Get an ORCID."
-   "Obtain DOIs for datasets, reports, and software packages."
keypoints:
-   "Include small datasets in repositories; store large ones on data sharing sites, and include metadata in the repository to locate them."
-   "Data should be findable, accessible, interoperable, and reusable (FAIR)."
-   "An ORCID is a unique personal identifier that you can use to identify your work."
-   "A DOI is a unique identifier for a particular dataset, report, or software release."
-   "Use Zenodo to obtain DOIs."
-   "Publish your software as you would a paper."
---

FIXME: introduction

## What to Publish and Where {#s:publish-what-where}

-   Now that we know *how* to publish, the next questions are *what* and *where*
-   What to publish
    -   Raw data (discussed below)
    -   Intermediate files that take a long time to generate
    -   Every version of software used in a report
    -   The configurations and parameters used for that software
    -   The scripts, notebooks, and/or Makefiles used to produce results
-   Where to publish
    -   Big raw data (more than 5 GB)
        -   May not be yours in the first place, and needs professional archiving
        -   You should include identifiers and/or scripts so that other people can access it
    -   Medium-size raw data (between 500 MB and 5 GB)
        -   Use platforms like the [Open Science Framework][osf], [Dryad][dryad], and [Figshare][figshare]
        -   Again, include identifiers and/or scripts
    -   Small raw data (under 500 MB)
        -   Store in GitHub
    -   Whichever you use, get or create a [DOI](#g:doi) for each version of each dataset
-   Use [Zenodo][zenodo] to get DOIs ([s:structure](#CHAPTER))

## Exercises

FIXME

## FAIR {#s:publish-fair}

-   The [FAIR Principles][go-fair] describe what research data should look like
    -   Still mostly aspirational for most researchers
    -   But it tells us what we need to work on
    -   And yes, I suspect the acronym came first...
-   Findable: because the first step in using or re-using data is to find it
    -   (Meta)data is assigned a globally unique and persistent identifier
    -   Data is described with rich metadata
    -   Metadata clearly and explicitly includes the identifier of the data it describes
    -   (Meta)data is registered or indexed in a searchable resource (FIXME: such as?)
-   Accessible: you can't use data if you don't have access to it (which means a way to authenticate, and having permission)
    -   (Meta)data is retrievable by its identifier using a standardised communications protocol
        -   The protocol is open, free, and universally implementable
        -   The protocol allows for an authentication and authorisation procedure if necessary
    -   Metadata is accessible even when the data is no longer available
-   Interoperable: data usually needs to be integrated with other data, which means that tools need to be able to process it
    -   (Meta)data uses a formal, accessible, shared, and broadly applicable language for knowledge representation
    -   (Meta)data uses vocabularies that follow FAIR principles
    -   (Meta)data includes qualified references to other (meta)data
-   Reusable: because this is the ultimate purpose of all of this
    -   Meta(data) is described with accurate and relevant attributes
    -   (Meta)data is released with a clear and accessible data usage license
    -   (Meta)data has detailed provenance
    -   (Meta)data meets domain-relevant community standards

## Exercises

FIXME

## Publishing Packages {#s:publish-DOI}

FIXME
-   What is an ORCID?
-   What is a DOI?
-   Connect GitHub to [Zenodo][zenodo] to create [citable code][citable-code]
    -   Create a release
    -   Tag it
    -   Create a DOI
-   Publish in [JOSS][joss] or [F1000 Research][f1000-research]

### Exercises

FIXME

## Summary {#s:publish-summary}

FIXME: create concept map

{% include links.md %}
