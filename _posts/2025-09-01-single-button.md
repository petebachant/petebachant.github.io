---
comments: true
date: 2025-09-28
layout: post
title: "Single button reproducibility: The what, the why, and the how"
categories:
  - Open science
  - Reproducibility
  - Software engineering
---

One of the initial visions for computational reproducibility dates back to
the early 90s, where
[Claerbout and Karrenbach](https://doi.org/10.1190/1.1822162)
shared their goal that researchers would be able to
reproduce their results "a year or more later with a single button.""

These days, the open science movement has made code and data sharing more
prevalent,
which is a great achievement,
but often what is shared---sometimes called a
["repro pack"](https://lorenabarba.com/blog/how-repro-packs-can-save-your-future-self/)---is
not really single button reproducible.
In fact, in most case repro packs are
[not actually reproducible at all](https://doi.org/10.1093/bib/bbad375),
hence why it's referred to as a crisis.
As a side note,
I am not talking about replicability here,
which refers to collecting new raw data
and checking the original study's conclusions.
Reproducibility refers to rerunning the analysis, visualization, etc.,
on the original data,
checking that it's possible to regenerate the evidence (figures, tables, etc.)
that back up the
original conclusions.

Log on to Figshare or Zenodo and download a random repro pack and
you'll probably see long lists of manual steps explaining how to
create and update environments, install dependencies,
and then maybe a numbered
collection of scripts and/or notebooks.
Sometimes, you'll see a collection of files with no instructions at all.
In many cases, you'll need to manually modify the code to run on your
system,
either because you've been instructed to download some data and put it
somewhere of your choosing, or the original author used absolute paths
that need to be adapted for a new instance of the project.

To be clear,
this level of transparency and willingness to share messy research code
is laudable,
and failure to reproduce does not necessarily indicate
incorrect conclusions,
but the lack of automation in workflows presents a huge opportunity
to benefit both the community and those who are currently publishing
irreproducible work.
Here I'll explain the what, why, and how to get there.

## What is single button reproducibility?

Basically, if you can go from raw data to research article with a single
command (or button, but the command line is probably more realistic),
your project is single button reproducible.
This one command should include dependency management,
e.g., installing Python or R packages.
However, we can make exceptions for system-level
foundational dependencies like Python distributions,
R, Julia, Docker, etc., even MATLAB.
The distinction here is that these are generally useful across many projects
and do not vary like package versions might.
So, a programming language like Python is a foundational dependency but a
library like Pandas is not.

## The relationship to software products

You may think your scripts will never have any use outside your
project---so what?
Almost all software products started out as some prototype that
solved a very specific problem,
hence the phrase "land and expand."
Make your project at least run, worry about productization later.

## Benefits to society

It's not hard to imagine why it would be nice for every single study
to ship with a single button repro pack.

## Benefits to the individual

Sadly, individuals are not going to be making decisions like whether
or not to automate their research workflows based on the benefits to
society alone.
They'll need to get something out of it.
Luckily, there is much to be gained for those who automate.

Cal Newport's "Deep Work"...

## But what about the cost?

## So how do we get there?

By now maybe you agree that single button reproducibility is a good
thing.
However, given the cost, perhaps it's in the "nice to have" category.
The papers need to get out the door,
and you don't think the cost/benefit analysis justifies it right now.

1. Subsidize the cost:
    1. Of training
    2. Of the software engineering work
2. Build tools and infrastructure to bring the cost down

Option 1.1 is effectively the strategy of
[The Carpentries](https://carpentries.org/)
and it's one I like.
Computational literacy may not fit into most college curricula,
but I believe it can improve the productivity of basically any knowledge
worker.

Option 1.2 is a bit newer,
with research software engineering (RSE) becoming a more common job title
in academia (my current one).
Essentially the strategy is to pay for the expertise so scientists
don't need to do so much on their own.
I like this one as well,
given that's currently how I make a living,
and it's especially good when RSEs can help produce scientific
software products that help reduce the computational expertise
necessary for other scientists to do their work.

I also believe that there is unnecessary complexity in some typical
computational practices in research,
which is worth building tooling infrastructure around to allow researchers
to work at a higher level of abstraction.
Is it really reasonable to expect scientists to become part time SWEs so
their R and Python scripts can be reproducible?
Or do we expect them all to hire experts in somewhat high demand for
relatively simple computational workflows?
This is where option 2 comes in,
and I think we need to continue down that path.

## Simplified tooling and infrastructure

Of course I will need to talk about Calkit now.

Concepts:

1. The project is the most important entity and should contain all related
   files.
2. Any derived artifact, e.g., a figure, should not be shared outside the
   project unless it was produced by its pipeline.

Follow these two rules, and you'll be more efficient...

### Challenge 1: Version control

### Challenge 2: Tooling fragmentation

### Challenge 3: Dependency management

### Challenge 4: Bridging the interactive--batch chasm

When someone creates, for example, a figure that they like.
They will naturally assume they're done, i.e.,
they won't have to do it again, or they won't
need to iterate on it.
So they won't think they need to automate its creation.

What we need is a way to essentially create a replayable and editable
history of what they did.

## Where Calkit is heading

## Reproducibility: What is it?

First off, what is reproducibility?
The Turing Way handbook has a good section on this.
Basically, it means that with the same data and tools,
anyone can get the same results.

This is not to be confused with replicability,
which involves collecting new data.

If we create a simple model of the research process as a
directed acyclic graph (DAG),
it might look like this:

```mermaid
flowchart LR
    A[Collect data] --> B[Process data]
    B --> C[Visualize data]
    C --> D[Compile paper]

    style A fill:#90EE90
    style B fill:#87CEEB
    style C fill:#87CEEB
    style D fill:#87CEEB
```

In this model, reproducibility involves the latter three stages,
which replicability includes them all.

## How bad is the 'crisis'?

## The gold standard

In the original

Single button

Where do we draw the line?
Some have said 15 minutes of labor max.
Personally, I think we should shoot for the moon here.

"Foundational" dependencies are an exception.
Things like package managers, Docker, etc.
Individual package installs must be automated though.

From this standard, a study that takes an hour of human labor to reproduce
would technically not be considered reproducible.
It kind of is, but in my opinion we should be shooting for the gold standard.
We'll discuss a bit more about why that's important later on.

## A rule of thumb

If you want to share something, e.g., a figure, dataset, or ML model,
produce it as part of a version-controlled
single button pipeline so there's never any question
how it came to be.

## Relation to open science

To be reproducible, it must be open.
However, it's possible to be open but not reproducible.
In fact, that's very common.

## Are our methods unsound?

>I don't see any methods at all.

Accurate description of methods is an integral part of any scientific study.
However, the computational tools available to researchers
these days are so complex that traditional ways of describing methods---prose
and mathematical formulas---are no longer sufficient.

## The state of the art in open reproducible science

Lists in a README

A conflation of repro/reuse

If one did truly want to make their work single-button reproducible,
what would it take?

## Why reproducibility is rare

Cost/benefit

Cost can be getting scooped

Costs of manual workflows are not obvious

Hidden or forgotten global state

Interactivity causes this, but interactivity is key

Fragmentation

For software development, it is now taken for granted that automating
testing and deployment is always worth the cost,
but is that true for research work?

## The costs and gains to be had

Scientists provide value by thinking up innovative ideas
and turning them into knowledge.
They do this with the scientific method.
Any unnecessary work done along the way is waste.

Let's try to estimate that waste.

What are some examples of wasteful activities:

- Determining which figures need to be regenerated after a change in data
  processing logic.
- Manually uploading new figures to Overleaf or re-importing into Microsoft
  Word.
- Manually copying data to and from an HPC cluster.

TODO: Make some back of the envelope estimates and show that if
reproducibility were free,
science would advance X% faster.

## The role of interactivity

Interactivity is necessary for discovering the computations that work.

However, interactive workflows need to be converted into batch workflows
once they are deemed valuable.
That is the costly part that often doesn't make immediate sense to do.

We lose the breadcrumbs.

Global system changes that now get us working.
We could document them, but that's also costly.

Let's to back to the rule of thumb with an example.
Say you're playing around and stumble upon a way of visualizing the data
the elucidates an answer to an important question.
Before sending it off to your team on Slack,
put the script or notebook or whatever into a pipeline, run it,
and share the version created there.

So how to we bridge the divide?

## Why we should improve

Eliminating mistakes: Let's forget about that because in peer review it's
hardly ever checked.
However, it's a given.

We are going to focus on benefits to the individual,
not society.

Efficiency gains

Iteration cycle time

Can we do a simulation to show where the tipping point is with simpy?

Reusability

A nice reproducible research project serves as a platform for doing more
science, not as a platform for developing software.

I often see repro packs written in such a way that they attempt to
deliver half-baked tools instead of the research project itself.
This may be out of humility.
Why would anyone want code that simply produces the results in my paper
but nothing more?

The thing is,
in trying to make your code more reusable you broke its ability to achieve
its original purpose!

## The goal: Reduce the cost and increase the benefits



## My current hypothesis for a solution: Full stack science

Silos and handoffs are bad.

Maybe don't need this section

Bring down the cost and improve the benefit

Education is a cost
Can we reduce the amount of training required by building better
computational tooling and infrastructure?

If you look at the landscape, there are so many tools out there to use,
but it's very rare to tie them all together.

This is the direction we've been heading with Calkit,
and we're going to keep driving down the cost of automation.

Is literate programming the answer?
I'm skeptical that it will be intuitive to people to declare a big
computing job to be run on an HPC inside of a document,
but maybe.
