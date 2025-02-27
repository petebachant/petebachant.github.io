---
comments: true
date: 2025-02-28
layout: post
title: Continuous reproducibility and the interactive/batch dichotomy
categories:
  - Open science
  - Reproducibility
---

I have a hypothesis: Working reproducibly is more efficient than not,
despite the fact it might feel like extra work.

What does this mean to work reproducibly though?
It means at any point in time, the outputs of a given project
accurately reflect the inputs and process definitions therein.

I would go further to posit that if a project can remain
continuously reproducible,
it can be done more quickly and with higher quality.

This idea comes from software development,
namely the concepts of continuous integration (CI)
and continuous deployment (CD).
CI means that valuable changes are incorporated into the
single source of truth as soon as they
are discovered,
and CD means that the external world has access to these changes as
quickly as possible.
An enabling practice for CI/CD is test automation.
What test automation does is ensure that the behaviors of the
software (outputs) match a set of defined inputs.

In any case, practicing CI and CD are key to delivering
higher quality products more quickly,
and this is widely accepted as truth in the software
development world.

In a research project is certainly can be a good idea to use
automated tests for the software to check its accuracy,
but reproducibility is slightly different.

The way CI works is that any proposed change goes through some testing,
and...

So, our research project should have a single source of truth
where its state is tracked with a version control system.
This is the state of the inputs and processes.

```mermaid
inputs --> processes --> outputs
```

What is it like to not work reproducibly?

What this means is that we need to produce outputs as part of a
batch process.
However, developing the process is almost always more efficient
to do with an interactive workflow with fast feedback.
We then need some way of taking what we discover in our interactive work
and converting it into a batch process, i.e.,
a pipeline.

What are some tactics for managing the back-and-forth?

The first is to never take any product produced with a interactive
workflow as the final product.

The frequency with which you flip back and forth between the workflow types
is important.
It should be as frequent as possible.
Discover a valuable change and integrate it back into the pipeline
right away.
Commit it to the version control system.

You should probably never be showing anyone anything developed with
an interactive workflow.
Those "products" are temporary and only there for you to get feedback
on your batch process definitions.
