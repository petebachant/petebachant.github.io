---
comments: true
date: 2024-11-11
layout: post
title: It's not possible to work reproducibly in Microsoft Word and Excel, right?
categories:
- Open science
- Reproducibility
---

![Anakin uses Excel.](/images/repro-office/anakin-excel.jpg)

Everyone knows that when you want to get serious about reproducibility
you need to stop using Microsoft Word and Excel and become a computer hacker,
right?
There is some truth to that, that working with simpler,
less interactive tools is typically better for producing permanent artifacts,
e.g., figures, papers, and being somewhat certain about how they were produced,
but it's not mandatory.

It's also not usually mandatory to work in a reproducible way, i.e.,
sharing all code and data so others can arrive at the same exact results.
These days, many journals are requiring a "data availability statement"
(see the example from Elsevier below,)
which allows authors to explain why code and data might not be available,
but hopefully someday it will be fully mandatory to share everything,
so here we're going to help you get a head start on that.

![Data availability standards.](/images/repro-office/elsevier-research-data-guidelines.png)

Inspired by the article
[Ten Simple Rules for Computational Research](https://doi.org/10.1371/journal.pcbi.1003285),
we're going to keep things simple and focus on two rules:

1. **Keep all files in version control.**
  Something like Dropbox is not sufficient.
  When you make a change you should have to describe that change,
  and that record should exist in the log forever.
  Adding your initials and a number to the filename is also not good enough!
  Whenever you’ve made a change with any value, _commit_ it.
1. **Generate permanent artifacts with a pipeline.**
  This will allow us to know if our output artifacts, e.g., figures,
  derived datasets, papers,
  have become out-of-date and no longer reflect their input data or
  processing procedures, after which we can run the pipeline and get them
  up-to-date.

{% include figure.html
src="/images/repro-office/phd-comics-version-control.webp"
caption="Manual or ad hoc "version control" (don't do this.) From phdcomics.com."
width="90%" %}

We're going to follow the two rules with the help of Calkit,
the installation instructions for which can be found
[here](https://github.com/calkit/calkit?tab=readme-ov-file#installation).

The first thing we're going to do is create a Git repo for our project.
We'll do this up on the Calkit website,
which will create a repo for us on GitHub,
and help us to _use Git without using Git_.

We are going to treat our project repo as the place to put everything.
Yep, everything that has anything to do with our work on this project
goes in the repo.
This will save us time later because there will be no question about
where to look for stuff, because the answer is: in the repo.

Instead of using something like Dropbox,
we will use a repository so every time we save a file,
we leave a trail of breadcrumbs regarding how we got there,
why we did what we did, etc.
It's like "track changes" for an entire folder.

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

![Elsevier research data guidelines](/images/repro-office/elsevier-research-data-guidelines.png)

From https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-guidelines.

At some point, you probably won't be able to publish unless you include
all of your code and data, so you might as well get ahead of the curve.

Maybe it will speed up the publication process.
Has anyone studied that?

Working reproducibility will also make you more efficient and organized,
so it's not just some noble service to society.
