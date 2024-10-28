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

Here we're going to develop a reproducible workflow without using the
command line at all.

I will typically avoid office suites like Microsoft Office like the plague.
I don't find them to be particularly helpful at producing anything that
should live for a long time,
and there are better tools for quick notes, calculations,
and slideshows.

After writing my masters thesis in Word,
keeping track of reference and equation numbers manually because I couldn't
get Word to format them properly,
I've held a grudge against office suites.

Many spreadsheets contain errors, but code probably does too [Greg Wilson].
Errors are fine, so long as the version that produced the publication
is available, and it is truly the one that produced the publication.
That's the problem we're going to solve here.

TODO: Paid software and reproducibility.
You need a computer, and those cost money too.
This is nuanced.

Another time I was collaborating on a document with half a dozen people,
and we were emailing around the document,
using the tried-and-true version control system of appending
initials and revision numbers every time,
when two people made edits at the same time,
and they needed to be merged manually.

Real time cloud editing a la Google Docs is has made this much better,
but it remains troublesome, to say the least,
to use an office suite for real scientific work.

Unfortunately, office suites are a go-to tool for many,
and I want to resist being elitist and simply insisting people
switch to, e.g., LaTeX and Git because I said so.
I actually tried this once a long time ago, and it did not go well.
Most people are not early adopters...

So, can we use an office suite and still work reproducibly?
Here we will try.

The persona we will be here does not use the command line, ever,
so we won't either.
They store, analyze, and visualize their data in spreadsheets,
and write papers in a WYSIWYG word processor.

To be clear: I want this workflow to be okay!
I don't think we should force all researchers to become hacker
software engineers to create knowledge.

We are going to use Calkit here, of course.

The main principle we're going to follow is:

>Save every change

So let's create a new Calkit project.

This is going to take up a lot of storage space,
but we can always clean this up later.

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
be cited in our paper.
