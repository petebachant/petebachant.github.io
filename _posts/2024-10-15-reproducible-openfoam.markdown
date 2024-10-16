---
comments: true
date: 2024-10-15
layout: post
slug: reproducible-openfoam
title: Reproducible OpenFOAM simulations with Calkit
categories:
- Engineering
- Software
- Open science
- Reproducibility
---

## Background

Have you ever been here before?
You've done a bunch of work to get a simulation to run, created some figures,
and submitted a paper to a journal.
A month or two later you get the reviews back and you're asked to, e.g.,
make some modifications to make a figure more readable.
There's one small problem, however: You don't remember how that figure was
created,
or you've upgraded your laptop and now have different software installed,
and the script won't run.
In other words, you can't reproduce that figure.

TODO: Relate that more to an OpenFOAM simulation.

I've been there too.
A particularly painful experience is when you run many different simulations,
deleting results after creating figures to save disk space,
and now have to run them all over again.

Now, using Git can be super helpful here.
You can keep your scripts in version control,
but what about your data or results that don't play well with Git because
they're either large (GitHub rejects files larger than 100 MB)
or not text?
You could use Git Large File Storage (LFS),
but that can be a bit overkill and expensive for files that don't
change much.
What about a tool to define and run a pipeline that generates all necessary
artifacts so you can just keep running one command over and over again,
without needing to remember which script does what?

In comes DVC (Data Version Control) to the rescue.
I found out about DVC a few months back and really liked the design.
It has a way to version data (of course) and a neat YAML-based pipeline
definition system.
In fact, I liked it so much, that I built [Calkit](https://calkit.io),
which is sort of like a glue layer between Git, DVC, GitHub, and cloud storage,
to try to make it super simple to work reproducibly.
Think "easy mode" for all those tools, putting everything in one place.

Now I'm going to walk through setting up a research project that will use
OpenFOAM.
We're going to try to answer the question:

>Which RANS model works best for a simple turbulent boundary layer?

## Getting setup
