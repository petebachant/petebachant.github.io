---
comments: true
date: 2024-11-02
layout: post
title: Office suites are the enemy of reproducibility, right?
categories:
- Open science
- Reproducibility
---

![Anakin uses Excel.](/images/repro-office/anakin-excel.jpg)

Everyone knows that when you want to get serious about reproducibility
you need to stop using Microsoft Word and Excel and
become a computer hacker, right?
There is some truth to that,
that working with simpler, less interactive tools is typically better
for producing permanent artifacts,
but it's not mandatory.

<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:share:7248736572437659648" height="536" width="504" frameborder="0" allowfullscreen="" title="Embedded post"></iframe>

[This post](https://www.linkedin.com/posts/greg-wilson-a26510b6_the-next-time-you-see-a-post-saying-spreadsheets-activity-7248736573263863809-3siO?utm_source=share&utm_medium=member_desktop)
is related.
Do we know if spreadsheets are more error prone than Jupyter Notebooks,
for example?
We're not going to worry about that here.
We're going to pretend we don't even know what a Jupyter Notebook is.
We use spreadsheets because that's the tool we know and have access to.
Further, errors are fine, so long as the version that produced the publication
is available, and it is truly the one that produced the publication.

We're going to take a few relevant rules from the article
[Ten Simple Rules for Computational Research](https://doi.org/10.1371/journal.pcbi.1003285):

1. For every result, keep track of how it was produced.
1. Archive the exact versions of all external programs used.
1. Version control all custom scripts.
1. Always store the raw data behind plots.
1. Provide public access to scripts, runs, and results.

Besides our office suite
(here we'll use LibreOffice, but Microsoft Office could work just as well),
we're going to need
[Git](https://git-scm.com),
Python ([Mambaforge](https://conda-forge.org/miniforge/) recommended),
and Calkit installed (`pip install calkit-python` from the command line).
There is a point to be made about minimizing the amount of commercial
closed-source software
used in research, since everything that needs to be purchased
is another barrier to reproducibility, but we're not going to worry
about that here.

The first thing we're going to do is create a Git repo for our project.
We'll do this up on the Calkit website,
which will create a repo for us on GitHub,
and help us to _use Git without using Git_.

This is so we can follow the principle:

>Version control all custom scripts.

TODO: Import dataset from
https://figshare.com/articles/dataset/Tropical_cyclone_impacts_in_coastal_marine_ecosystems/27316113?file=50036859

Or maybe
https://figshare.com/ndownloader/files/50034510

Now, spreadsheets are like custom scripts, data, and a computational
environment all bundled into one,
which has its benefits and drawbacks.
Keeping our spreadsheet in version control simply means we're
going to create a checkpoint, or "commit,"
every time we make a relevant change.
Instead of renaming the file every time,
we're going to save a message describing the changes each time
the file is modified,
so we can go back in time if we need to.

Next, let's address:

>Archive the exact versions of all external programs used.

This is a tough one.
Are you allowed to archive Microsoft Office?

We're at least going to define the version we're
using in our project's metadata.
To do this, we'll create a new environment description for our
computer.

TODO: This needs to be possible from the GUI.

First we will lock this file for editing so none of our collaborators
tries to work on it.
I think Word may have some sort of merge tool,
but let's avoid it if we can.
The necessity to truly work concurrently is very rare for these sorts of
projects, in my experience.

First, let's "collect" our data.
We are going to add some rows to a spreadsheet.
I am going to use LibreOffice here, but Microsoft Office should
work nearly identically.

Every time we make a change, we upload a new version?
That's pretty burdensome.
Maybe use the local server and GUI.

The only command line thing we're going to do is spin up a local Calkit
server to connect to the web app and allow us to modify the project
on our local machine.
Someday this will likely run as a background service,
but for now, it needs to be started manually.
So, open up a terminal, and assuming you've
installed [Git](https://git-scm.com)
run `pip install --upgrade calkit-python`
at some point, run

```sh
calkit server
```

Side note: If you are a GUI-only kind of person,
let me know if this is too annoying to be worth the trouble!

Now, the most important rule:

>For every result, keep track of how it was produced.

It is possible to do this manually,
but it is a waste of precious brainpower.
Essentially we want to view our project as a whole
and have some way of knowing if there is something about it
that is out-of-date or invalid.

The value to doing this lies in not needing to keep track of
whether or not something needs to be redone because
something about the pipeline has changed.
For example, if the filtering is updated,
there will be a cascading change as the figure and paper
are now invalid.
Being able to simply run the pipeline saves brainpower
for more important things!

We're going to keep these files in Git instead of DVC,
since they're relatively small.
Git is not great for this, since the files are binary
(actually they are zip archives of XML documents,
but we won't go down that road here),
but it's workable.

We're just going to focus on two goals:
1. Save every version in version control.
2. Make sure we can't forget to update downstream artifacts if something
   goes out-of-date.

TODO: Compute a metric by averaging our spreadsheet?
Make sure this value is correct in the text?

TODO: Figure and table in our document?

TODO: Show a diff/merge process?

So you've heard working reproducibly is important and feel left out because
you use Excel and Word to do your work?
Don't feel bad.

Last but not least,
we're going to bundle up and archive our materials so they can
be cited in our paper,
so we can follow the rule

>Provide public access to scripts, runs, and results.

TODO: Allow making project public, creating an archive.

This may already be mandatory for the journals you're
interested in publishing,
and hopefully it will be mandatory for all at some point.
I'd go even further to suggest most reviewers
should attempt to reproduce a result as part of the review process.
Might as well get ahead of the curve here.
