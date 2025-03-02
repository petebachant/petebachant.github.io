---
comments: true
date: 2025-02-28
layout: post
title: Continuous reproducibility and the interactive/batch dichotomy, or
  why working sloppily is not faster
categories:
  - Open science
  - Reproducibility
---

I have a hypothesis: Working reproducibly is more efficient than not,
despite the fact it might feel like extra work.
Further,
a research project should never not be reproducible.

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

The benefit of CI comes from many small changes incorporated immediately.
Applying this to a research project is also beneficial.

"Incorporated" means committed to a version control system that allows us
to revert changes or return to previous versions.

In any case, practicing CI and CD are key to delivering
higher quality products more quickly,
and this is widely accepted as truth in the software
development world.

Many think their work is reproducible,
though it probably isn't.
I have personally attempted reproducing some results from
code and data archives cited in papers.
Many times what is shared is incomplete.
Sometimes it's just the code without the actually configuration
used to generate the results.
Sometimes it's just the data with an explanation on how to use it.

Now, if these projects were setup to be CR,
the entire thing could be shared.

This shows up in software development as the
"works on my machine" phenomenon.
Is this a problem?
Is it necessarily true that a failure to reproduce means the results
are invalid?
Probably not.
Irreproducible does not mean irreplicable,
but it certainly makes things much harder.

CR via GitHub Actions CI with Calkit...
This gives you an "objective" machine on which to run your pipeline.
If you want, use can use the `--force` to bypass all cached results
and ensure they are created identically.
This could be useful if you haven't properly defined all the dependencies
for a given output.

In a software development project,
it is optimal to create lots of small but valuable changes,
always integrating these into the single source of truth,
or the main branch.

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
Well, it means that the path one took to produce an artifact can no longer
be reliably followed.
Even if you think you've documented your work properly,
if that has not been tested,
it's highly likely that the documentation is missing something,
and your work will not be reproducible.

The solution is to keep running your project every time you make a change.

To make this easier, you should probably build your project in a framework
that can detect change so expensive steps don't need to be rerun
if their inputs or process definitions have not changed.

Calkit uses DVC for this part.
Then there's the other hard part that seems to be overlooked most often:
environment management.
The computation environment is the foundation that must be in place
to run the processes.
One simple way to solve this is to create instructions on how to get your
computer ready to run the project.
This is done in many different ways and there's lots of room for error.
For instance,
there may be a simple list of dependencies in the project's README.
It is then up to the user to install these on their own,
perhaps without even knowing which version may or may not work.

Another step up is to document the environment for some sort of environment
management tool, e.g., Python's `venv`,
and provide instructions for the user to create that environment,
install the dependencies from a file,
then activate the environment before running a given process.
Docker is another form of environment management.

Calkit incorporates environment management to remove that step
requiring the user to setup their own environment.
It also easily allows for multiple environments in a single project.

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

Don't worry about reusability.
So long as your project is reproducible,
you are at least demonstrating to the world how it's done,
and they can rerun and adapt it accordingly.

Excel mental model?
Most projects are too complex to be fully managed in a spreadsheet,
though many will try valiantly.

ResOps like DevOps.
