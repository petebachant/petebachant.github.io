---
comments: true
date: 2025-09-01
layout: post
title: "Why almost no science is reproducible, and should we even care?"
categories:
  - Open science
  - Reproducibility
  - Software engineering
---

Why your research is probably not reproducible, and does that even matter?

Your research is probably not reproducible: Why is that, and does it even matter?

Your research is probably not reproducible,
and you probably don't care enough to change that.
That's not a judgement of you,
but of the system in which you're working.

I left my job about a year ago to try to help with the reproducibility
crisis.
This article is a summary of what I've learned so far and my current outlook.

When I started on this journey I assumed this problem was well known and
just about every researcher was eager for a solution.
I learned it wasn't so simple.

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
