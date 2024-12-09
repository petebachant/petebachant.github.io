---
comments: true
date: 2024-12-13
layout: post
title: A cloud-based workflow for collaborating on LaTeX documents
categories:
  - Open science
  - Reproducibility
  - Collaboration
  - Open source
---

I've noticed a bit of dissatisfaction with Overleaf lately.
In my opinion it's a great tool for what it's meant for: Collaborating on
LaTeX documents where the document is the main thing changing.

What that means is that the project needs to be one where it's
mostly writing,
not data analysis, figure generation, etc.,
since Overleaf isn't made for those other things.
Since my projects almost always involved more than just writing a document,
Overleaf was not the right tool for the job,
so I didn't use it much.

I'm going to give a slightly different philosophical stance on
collaborating on documents or any other files for that matter.
I don't actually think concurrent editing is good actually.
For the same piece of content, team members should work in series,
or the work should be split up into relatively uncoupled
pieces before updating in parallel.

We are going to show a practical example here that makes use of
Calkit, an open source
tool I've been working on to help with reproducibility in
research projects.

Full disclosure: There is a paid aspect of the Calkit Cloud
to help pay for the costs of running the system,
since it allows for storage of artifacts,
but the software is fully open source and there is a free plan
that provides more than enough storage to do what we'll do here.

Calkit defines a framework for managing the entire project,
not just the writing part,
but we'll just focus on writing and document creation here.
Calkit ties together and leverages Git, GitHub, DVC, Docker, and more
to allow everything to live in a single folder,
and easily be run on different machines.

Here, the Calkit web app is going to setup our GitHub repo
for LaTeX editing and compilation.
This could all be done manually outside,
but the goal here is to make it as simple as possible with as few steps
as possible.

Starting from the beginning,
we'll assume we already have an Overleaf project and we want
to migrate it over.

Another benefit of what we'll create here is the ability to work offline
using nearly identical tooling.
We're going to use a GitHub Codespace for cloud editing,
which defines a so-called "dev container" that can be connected to remotely
or run locally with VS Code.

Another elephant in the room is Git.
Git is scary for the uninitiated, but here we'll show that with
VS Code's graphical tools, it's quite easy.

## Prerequisites

In order to set this up, you will need a GitHub account

## Creating the project

Head to [calkit.io](https://calkit.io),
sign in with GitHub,

TODO: Remove plan selection

then create a new project.
This will create a GitHub repo for us,
setup DVC,
and create a dev container in which we and our collaborators can work.

On the publications tab,
create a new publication,
select the type as report for now,
and select the `latex/article` template.
This will add a LaTeX template to our repo and a build stage to our
DVC pipeline.

TODO: Allow importing from Overleaf?

Next, click "edit in GitHub Codespace."
This will open up a new tab with an in-browser VS Code
editor, which will have access to our GitHub repo
and will be able to compile the LaTeX document.

## Handling concurrent collaboration

The Calkit web app has a feature that allows locking files for editing.
You can use this so your collaborators see they shouldn't
work on the file at the same time.

## Reviewing proposed changes using PRs?

## Adding comments to address

If you highlight a region of the PDF, you can create a comment
and a corresponding GitHub issue.
If you make a commit that addresses a given issue,
you can include "fixes #5" or "resolves #5" in the commit message,
and GitHub will automatically close it.
I love that feature!

## Importing from Overleaf

```sh
calkit import publication \
    https://overleaf.com/my-thing \
    --kind journal-article
    --stage latex-build
```

```sh
calkit new publication \
   --title "PhD thesis" \
   --import https://overleaf.com/something \
   --stage build-thesis \
   --stage-type latex \
   --environment texlive \
   ./thesis
```

## Conclusions

This setup will allow us to do the other things we'll
need to do in our research project like store datasets,
process them, create figures,
and also build them into our paper.
It can all happen in one place with one command.
