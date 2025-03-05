---
comments: true
date: 2025-02-28
layout: post
title: >
  "_Continuous Reproducibility_: How adopting DevOps principles can help
  improve the speed and quality of scientific discovery"
categories:
  - Open science
  - Reproducibility
  - Software engineering
---

In the 21st century,
the principles of
[lean startup](https://en.wikipedia.org/wiki/Lean_startup),
[agile software development](https://en.wikipedia.org/wiki/Agile_software_development),
and [DevOps](https://en.wikipedia.org/wiki/DevOps)
have significantly reduced waste, improved quality,
enhanced innovation,
and increased the speed of development of software products and related
technology.
At the same time, the
[pace of scientific innovation appears to be slowing](https://doi.org/10.1257/aer.20180338),
and many findings are failing to be replicated (validated in a full end-to-end sense, re-acquiring and reanalyzing raw data)
or even reproduced (verified by rerunning the same computational processes
on the same inputs).

The practitioners of research borrow many habits
and tools from the software development world,
which makes sense given that so much of work of researchers relies on computers,
but I believe the DevOps strategies of continuous integration
and continuous delivery (or deployment;
[CI/CD](https://en.wikipedia.org/wiki/CI/CD))
is the next important
concept researchers can borrow from the software development community.
This could be called _Continuous Reproducibility_ (CR).

Firstly,
what is CI/CD and how does it relate to working habits and project
management?
CI means that valuable changes are integrated or incorporated into the
single source of truth, i.e., the main branch, as soon as they
are created,
and CD means that the external world has access to these changes as
soon as possible.
An enabling practice for CI/CD is test automation.
What test automation does is ensure that the behaviors of the
software (outputs) match a set of defined inputs.

Automated testing then makes developers feel safe that the
changes they're about to incorporate don't break anything.
Similarly,
automating research projects...

Working this way encourages small batch sizes
and discourages the so-called
["waterfall"](https://en.wikipedia.org/wiki/Waterfall_model)
project management style,
where projects pass through "stage gates," e.g.,
planning, design, execution, testing, release,
in a linear fashion with little to no feedback loops,
often handled by completely different teams handing off artifacts
to each other without truly collaborating.
The waterfall approach is often inefficient because planning is
difficult or nearly impossible when the requirements
are uncertain and therefore cannot be fully documented up front.
Fundamentally,
these movements are about breaking down silos
and moving from large batch to small batch sizes.

Silos exist in research between funding organizations and PIs,
PIs and grad students and postdocs,
and authors and referees.
There are sometimes silos between collaborators,
where for example,
only one team member knows how to run the code,
or has their computer setup to do so.
SWEs avoid this problem by setting up automated pipelines
and running these on 3rd party machines,
usually starting from no state.

This is analogous to climbing a ladder one small step at a time
instead of taking one big jump.

In research,
to shift from large batch to small batch flows,
CR is an enabling practice that ensures the single source of truth,
the full collection of project files
(documents, datasets, code, figures, publications)
despite evolving rapidly and in small increments,
remains reproducible throughout the entire project lifecycle.

One tactic practiced by the open science community is to publish
a ["reproducibility pack" or "repro pack"](https://lorenabarba.com/blog/how-repro-packs-can-save-your-future-self/)
along with each scientific article.
However, in my experience,
these are often curated after the project is mostly finished,
and therefore were not actually used throughout the process.
They often only include a subset of the files,
e.g., only the datasets, or only the code,
but not the files used to generate the figures or manuscript.
Further, they are usually missing some information that only the researcher
knows since they are working with the files every day on a computer
whose state (operating system, software installed, etc.)
may have evolved over years.
[I am guilty of this too](https://petebachant.me/failed-to-repro/).

I believe there is a lot of value left on the table by taking this
phased approach.
For one, it is more complex with higher cognitive overhead.
When working this way,
that insider information lives in the researcher's head,
meaning every time they make a change to some file,
they need to keep track of the downstream consequences
and run the appropriate processes,
perhaps doing something like manually copying and pasting artifacts into
a different location.
Secondly, it is error prone.
Missing a step in a manual "pipeline" could result in out-of-date
or even incorrect results making their way into the final publication.

The scientific review process today is similar to the handoffs
between software development and quality assurance (QA) teams.
However, journal article referees are usually not rerunning analyses.

The two most important tactics to achieving CR are:

1. Keep all files in version control, in a single repository.
1. Automate dependency management.
2. Generate all artifacts with a single pipeline. The opposite of this would
   be having one pipeline to run the simulation,
   one to post-process, one to generate figures,
   one to compile the publication,
   all of which need to be executed separately by the researcher.
   A pipeline system that can cache results is critical here if there are
   expensive steps, but more on that later.

The change in mindset is a move from focusing on individual files
and artifacts to a focus on the project as a whole.

Software engineers will work on one small part of the code
and run an automated test suite to ensure the entire project still works.

This is the sort of mindset a research project should strive towards.

We don't move through phases and stop allowing for change.

For example,
data filtering may have a mistake,
and this has multiple downstream implications.
It's very possible that this mistake is discovered after submission
of a journal article.
In a CR workflow,
the filtering algorithm can be updated
and the pipeline can be run all in a single command,
ensuring all figures in the paper are up-to-date.

What if there's an important aggregate number in the paper?
Ensure that number is inserted as part of the pipeline.
Or at the very least,
include an explicit
[manual step](https://docs.calkit.org/pipeline/manual-steps/)
in the pipeline that will tell the user they
need to check that number
any time a dependency has changed.

## Examples of CR workflows

## Tactics for continuous reproducibility

What does this mean to work reproducibly though?
It means at any point in time, the outputs of a given project
accurately reflect the inputs and process definitions therein.

I would go further to posit that if a project can remain
continuously reproducible,
it can be done more quickly and with higher quality.

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

Some processes are too heavy to be practical to rerun.
For example,
it is usually not feasible to rerun a large scale simulation on a
high performance computing (HPC) cluster to simply check its
reproducibility.
In this case, some automated documentation of the version of the code,
configuration files,
and the computation environment(s) can be sufficient.
The key word here is automated.
Simply saying
"we ran SimulationApp v1.2 on the University of Whatever's cluster"
in the paper is too ambiguous.
Luckily,
a version control system is a convenient way to take a snapshot of all files.
However, it is possible to "cheat."

This is analogous to a software application with a large database
of users?
We don't need to be able to continuously recreate all of that data,
but we need to ensure that data could be recreated with any
version of the code.

## Anti-patterns to avoid

Even if when using a VCS,
it's possible to fall into a large batch mindset.

Working for a long period of time with dirty repo,
or even saving artifacts generated with a dirty repo.
Commit first, then run, if you intend to save the outputs.
Or at least commit changes to the code and outputs all at the same time.

Never share results generated with uncommitted code.
Or further,
never share uncommitted results.

### Not using version control

### Manual or ad hoc version control

### One project, many repos

This is analogous to the "distributed monolith" software architecture,
where tightly coupled components are spread across multiple codebases
and/or infrastructure groups.
In research, this could take the form of one repo for the data collection,
one repo for the data processing software,
one repo for the paper.
These are all inherently coupled in service of producing the paper.
Just keep them together in the same repo.
If by change some sub-component, e.g., the software,
becomes useful on its own,
deal with that afterwards, not up front.

### Large batch version control practices

Many small commits are generally preferable to fewer large commits.

### Prose pipelines

If a pipeline is written in English and can't be run all with a single
command,
it's not really a pipeline.
There will almost certainly be information missing.
This includes setting up dependencies as well.

### Multiple pipelines

Coincidentally,
the ["repro pack" attached to [1]](https://doi.org/10.3886/E111743V2)
appears to have 10 separate pipelines,
with no instructions on how to run them,
if there is any inter-dependence, etc.

It also doesn't contain the paper manuscript compilation.

## The opposite of continuous delivery

A common pattern in many analytical endeavors is to periodically
share slides with curated results.

The shift to CR would mean generating these slides as part of a pipeline,
so they continually stay up-to-date,
and the single source of truth and its history can be accessed
by all collaborators.

As a side note,
similar arguments could be used to support
eliminating research proposals.
Instead, simply fund innovative and capable scientists
and let them figure out what's important to discover.

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

## On collaboration

Handing off a draft is not real collaboration.

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

## Reusability

Don't worry about reusability.
So long as your project is reproducible,
you are at least demonstrating to the world how it's done,
and they can rerun and adapt it accordingly.
If someone makes a copy of your project and changes something slightly,
it will be very clear what has changed and what needs to be regenerated.

Excel mental model?
Most projects are too complex to be fully managed in a spreadsheet,
though many will try valiantly.
Every time you make a change, the spreadsheet values all update.
This means that their values are reproducible.
If you like what you see, you save the file.
If you have enabled track changes, or you use Google Sheets
named version feature,
you're then putting it in version control.
Now, this would be okay if you could generate everything in a single
spreadsheet,
and by everything I mean all figures, publications, etc.
Obviously spreadsheets don't do that,
so you'd need to use some other software for those things.
So when we expand from using a single file per project to multiple
files and processes per project, we need to use a more sophisticated tool.
In this case,
our project now becomes a folder of files,
and we shift our mindset to managing this folder instead of one file.

This project folder should then contain everything.
Yes, everything.
And we're going to need a tool to "track changes" to the folder,
instead of a single file.
We're also going to need some way of updating outputs
if inputs or process definitions change.

```mermaid
input data cell --> spreadsheet formula --> output data cells
```

ResOps like DevOps.

Anything worth doing is usually difficult,
and difficult things get easier if you do them in small steps.
Finishing a small step should mean the project stays reproducible.

Cite Barba's "repro packs" and how this idea is different because
your entire project is a repro pack from the start,
rather than something you put together at the end.

Waterfall versus agile argument?
Instead of having stage gates like plan, collect data,
analyze, write, start writing from the beginning.
View the entire project holistically.

Painful situations you can avoid by applying CR:

1. Your advisor points back at an older slide deck and requests that you
   include a certain figure in the paper you're preparing for submission,
   but you don't remember how it was generated.
   In this case you can copy/paste it out of the slides,
   but it's quite possible there are errors in that figure.
   If your project uses CR principles,
   the figure should be present in its most up-to-date form,
   and if not,
   you can travel back in time and check out the version used to generate
   the slides.
   Or better yet, travel back in time to view the entire state of the
   project at the time you emailed the slides.
   This is very possible.
2. You want to make a small change to a figure generated from a large
   simulation, but you generated the figure interactively instead of as
   part of a pipeline,
   and the results have long been deleted from your scratch space on the
   cluster.
   If you follow CR principles,
   that figure would never have been shared externally unless it could be
   generated by the pipeline.

## References

1. Nicholas Bloom, Charles I Jones, John Van Reenen, and Michael Web (2020).
   Are Ideas Getting Harder to Find?
   _American Economic Review_. https://doi.org/10.1257/aer.20180338.
