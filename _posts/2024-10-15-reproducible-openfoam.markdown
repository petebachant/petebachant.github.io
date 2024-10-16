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

You will need to have Git installed, and you'll need to have a
[GitHub](https://github.com) account.
You'll also need Python installed.
I will typically use [Miniforge](TODO),
but you can use whatever you'd like.
You'll also need to install Docker.

After that, you can install the Calkit Python package with

```sh
pip install calkit-python
```

This will install DVC as well.

## Creating the project

Head over to https://calkit.io and log in with your GitHub account.
Click the button to create a new project.
Let's title ours "RANS boundary layer validation".
We'll keep this private for now,
though in general you shouldn't be scared to work openly.
Creating a project on Calkit also creates the project Git repo on GitHub.

## Getting the project onto our local machine

There are a few options for getting our project onto our local machine:

1. The Git CLI.
2. GitHub Desktop.
3. The Calkit web app.

For the sake of novelty we're going to go with option 3,
the Calkit web app.

You'll notice up on the Calkit web app project page a section called
"local server."
Since you just installed Calkit,
the local server is most likely not running,
and the web app will tell you as much.
So let's start it up with.

```sh
calkit server
```

If you refresh the page you'll see that the icon has turned green,
indicating you're now connected.
If you click on the local server page,
you'll see some helper buttons,
one of which will allow you to clone the repo.
You can choose where it will go,
but by default it will go in `$HOME/calkit`.

## Getting some validation data
