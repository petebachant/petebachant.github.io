---
comments: true
date: 2025-02-28
layout: post
title: >
  Continuous Reproducibility: How DevOps ideas can help
  improve the speed and quality of scientific discovery
categories:
  - Open science
  - Reproducibility
  - Software engineering
---

In the 21st century, the
[Agile](https://en.wikipedia.org/wiki/Agile_software_development)
and [DevOps](https://en.wikipedia.org/wiki/DevOps) movements
helped to significantly reduce waste, improve quality,
enhance innovation,
and increase the speed of development of software products and related
technology by breaking down silos,
improving collaboration,
and moving towards working in smaller batches with faster feedback loops.
At the same time, the
[pace of scientific innovation appears to be slowing](https://doi.org/10.1257/aer.20180338),
with many findings failing to replicate
(validated in an end-to-end sense, re-acquiring and reanalyzing raw data)
or even to be reproduced
(verified by rerunning the same computational processes
on the same input data).
Though the products of science only sometimes include software,
I believe there is more science can learn from the software field
in these areas.

Here I will focus on one set of practices in particular:
those of _Continuous Integration_ and _Continuous Delivery_
([CI/CD](https://en.wikipedia.org/wiki/CI/CD)).
There has been some discussion about adapting these
under the name
[_Continuous Analysis_](https://arxiv.org/abs/2411.02283),
though I think the concept extends beyond analysis and into
generating other artifacts like figures and publications,
which oftentimes serve as the primary interfaces to the knowledge
science creates.
Therefore, here we will use the term
_Continuous Reproducibility_ (CR).

## Defining CI/CD

What is CI/CD and why has it become the norm for software teams?
CI means that valuable changes are integrated or incorporated into the
codebase's single source of truth, i.e., the main branch, as soon as they
are created,
and CD means that the external world has access to these changes as
quickly as possible.

Silos are broken down as development
is combined with operations (hence "DevOps").
That is, the same team writing the code handles testing/QA and deployment,
whereas in the past this might have been handled by multiple teams.
This way of working encourages frequent small changes (small batches)
to the codebase instead of larger, less frequent
updates, sometimes taking months or even years.

## The end of the waterfall

This more agile way of working evolved in response to the failures of the
[waterfall project management](https://en.wikipedia.org/wiki/Waterfall_model)
model,
which splits a project up into multiple phases or "stage gates,"
often owned by different people and moved through by handing off
large amounts of documentation.
For example, design, implementation, testing, and deployment all might
be siloed in different teams.

The source of inefficiency in this way of working comes from
the documentation burden, which hinders
communication/collaboration, and the high cost
of returning to previous stages after moving forward.
For example,
if a performance or user experience (UX) deficiency shows up in testing,
we may need to go back and redesign and reimplement parts of the software.
If each iteration requires similar amounts of documentation to be handed
off, the process may be slow enough to allow competitors to gain an advantage.
Working in smaller chunks and testing each one
allows us to discover issues earlier where
they are cheaper to fix.

We can see some waterfall aspects in research as well.
Data collection might be treated as a distinct phase
from data analysis,
which might be siloed from writing.
This would be fine if we never needed to return to earlier stages,
but anyone who has ever been part of the review process for a journal
article
should know that it's very likely you'll to need to revisit data analysis
and visualization to fulfill requested changes to the article.

## The role of automation

CI/CD is impractical without automation,
and thus automation was and is a key enabler.
As part of CI,
a suite of automated tests will run,
often on an independent computer,
to ensure changes will not break the codebase in ways that are hard to predict.
If the tests pass and the team agrees on the value of the changes,
they are merged.
Then, an automated CD pipeline will run
(also usually on an independent computer) to build
any necessary artifacts and send them where they need to go
(a web server, package download service, etc.).
Whatever is released out into the world is then totally consistent
with the single source of truth that is the main branch.

If these processes were not automated,
they would be more painful to carry out and would naturally be done less
frequently,
which reduces speed and quality.
The sense of confidence and reduced anxiety that comes from having
things automated makes it much easier to explore different ideas without
the fear of destroying previous progress.

## 'Repro packs'

One practice popularized by the open science community is to publish
a ["reproducibility pack" or "repro pack"](https://lorenabarba.com/blog/how-repro-packs-can-save-your-future-self/)
along with each scientific article.
These are great, and I applaud anyone who publishes one,
especially if they weren't required to do so.

However, I want to emphasize that curating a repro pack
should not be a stage that happens at the end of the project.
Continuous reproducibility would have us using a repro pack for the entire
project lifecycle, literally as the place to perform and keep all the work,
and it would follow a few important rules we will discuss later.

## General rules

So what would it mean for a research project to be "Continuously Reproducible?"
We can extract a few core principles from the CI/CD processes defined above:

1. There is a single source of truth for all input materials (data)
   and process definitions (code, configuration files).
   Practically this means a shared version control repository or repo.
   Different team members can easily sync with this main repo.
   No important files live on only one person's computer.
   Git is the obvious tool of choice here, but for very simple projects
   (e.g., ones that only involve a single file)
   Microsoft Office and Google Workspace's built-in cloud storage and
   version control may be sufficient.
2. These processes can be run on different computers, i.e., they are not
   dependent on some "hidden state" of one developer's machine.
3. Whatever is delivered to the outside world is always
   consistent with the input
   materials and process definitions.
   Through the use of version control, we can always go back in time to the
   input materials and process definitions that produced any given artifact
   and produce it again.
4. Getting the project into a consistent state after making a change requires
   very little effort from the team members.
   Practically speaking, this would mean executing a single command
   rather than a series of manual steps.
   It may require a good deal of work from a computer, but not a human.

## How to do CR: The specifics

Let's explore these more deeply and see how they can be followed or not.

This section is going to be slightly biased towards
[Calkit](https://github.com/calkit/calkit),
a project framework and toolset I've been working on to help
enable CR,
but it is by no means the only way to follow the principles,
and I will try to provide other options.

But what if you're already halfway through the project?
That's okay.
You can start working reproducibly from now.
At least you can put everything you have right now into version control,
then start adding to the pipeline for everything that needs to be
created after.

### Create a single version-controlled repo for the entire project

To say that a research project has a "single source of truth"
for all materials
we probably need to define what constitutes a project.
How do we draw the boundaries?

This might be the most important concept to help prevent complexity
from spiraling out of control.
First realize that working in small batches does not mean working
on small projects.
My recommendation is to start with a single logical project for each
general research topic.
If you're in the middle of a master's or PhD program everything
research-related belongs in that one
project so long as the topic hasn't radically changed.

Any file necessary to produce anything that will be released to the external
world belongs in here.
This includes proposals, notes, drawings, data, code, figures, slideshows,
articles, etc.

The important point here is that we don't want to splinter our work
off into a bunch of tiny projects,
e.g., one for a lit review,
one for your proposal, one for the experiment,
one for the analysis code,
one for the journal article,
and one for the thesis,
because they all will share content,
and if we prematurely split them up,
it will make some of the other CR rules harder to follow.

If a sub-project later emerges as something that can be valuable
on its own,
we can always split it off later,
e.g., into Git submodule.
Always better to err on the side of too big and break it up later
than start too small.

That is not to say you shouldn't organize the project with subfolders---you
absolutely should do that.

If you're using Git you'll want to use a secondary system to version
larger data files.
The Calkit framework uses
[DVC](https://dvc.org)
for this,
but there are other tools like
[Git LFS](https://git-lfs.com/) or
[DataLad](https://www.datalad.org/).
I recommend not building your own,
which I have been guilty of in the past.

### Minimize system-wide dependencies and automate their management

Instead of a list in the README that says "install A, install B, install C...,"
use virtual environments and/or containers.

If you absolutely require things to be installed system-wide,
try to keep them to a minimum and try to automate their installation with
a script or something similar.

In general system-wide dependencies should be avoided,
since typically multiple versions cannot be installed.
So for example, instead of telling users to install Matplotlib,
define a Conda environment and have them install Conda.
Similarly, instead of telling users to install some version OpenFOAM,
have them use a Docker container.

If you define all of your environments with Calkit,
you will not even need to instruct your users on how to create them.

### Allow reproducing everything with a single command

This follows a similar principle as above:
Avoid giving lists of steps to follow in the README,
which is like a non-automated pipeline written in prose.
Instead, automated it.

For example, you might have something like
"to run the simulations...",
"to create the plots...",
"to build the paper...".
The problem with this is that users (including you) will not know which to do
and when,
or it may require lots of insider knowledge and cognitive overhead
to figure this out.
This is a manifestation of the waterfall mindset,
assuming that once we've done one step we'll never need to return to it.
Falling for that can bite you.
Instead, make it simple and use a single pipeline or command.

Coincidentally,
the [repro pack cited in [1]](https://doi.org/10.3886/E111743V2)
appears to have 10 separate pipelines,
with no instructions on how to run them,
if there is any inter-dependence, etc.
It also doesn't contain the paper manuscript compilation.

If you're using Calkit,
you can put all steps into a DVC pipeline and execute them all with
`calkit run`,
which will also ensure all environments match their specifications.

Alternatives include
[Make](https://www.gnu.org/software/make/),
[Snakemake](https://snakemake.readthedocs.io/en/stable/),
[showyourwork](https://show-your.work/en/latest/)
(a project framework similar to Calkit but
focused on building LaTeX PDF articles with Snakemake),
or even a simple shell script.
If the project is super lightweight, e.g.,
a pure writing project with no figure generation,
the "pipeline" could be to save a Word document as a PDF.
Keep it as simple as possible.

Following this rule will help limit the number of tools you use as well.
For example, instead of opening MATLAB to run data analysis scripts
and uploading figures manually to Overleaf,
use a more general tool like
VS Code that can edit/run both MATLAB and LaTeX files.

You should be running your pipeline after every change.
However,
some processes are too heavy to be practical to rerun every single time.
For example,
it is usually not feasible to rerun a large scale simulation on a
high performance computing (HPC) cluster to simply check its
reproducibility.

In these cases, we should cache results and come up with some way to determine
when they've been invalidated.
However, avoid writing your own caching logic, since:

>There are only two hard things in Computer Science: cache invalidation and naming things.
>
>-- Phil Karlton

If you're using Calkit,
the DVC pipeline allows cache invalidation based on the content of files.
You provide a list of input files,
and if none of those have changed since the last run,
the outputs are still valid.
You can set the input files to be all of your simulation scripts and configs,
run the pipeline,
cache the outputs,
and you can keep calling `calkit run` over and over and the heavy process
will not rerun unless you edit the scripts or configs.
Your collaborators can sync from the cache and work on later pipeline
stages without missing a beat.

### Use a CI/CD service, or at least an independent computer

For example,
run your pipeline on GitHub Actions, which is free for public projects.
See [this example](https://github.com/calkit/example-basic/blob/main/.github/workflows/run.yml)
for a Calkit project that runs automatically on every push to GitHub.

This can be very helpful as a CI/CD service will typically give you access
to a fresh virtual machine (VM) for every run,
which means you need to automate the full setup and pipeline running
process.
This simulates what it would take for one of your collaborators to get
started
and helps catch dependencies or steps you've omitted or forgotten.

Coincidentally,
I was recently setting up a CI pipeline for Calkit,
and even though the tests all ran fine on my machine,
it took me
[15 iterations](https://github.com/calkit/calkit/pull/273)
to get them running up on the GitHub Actions CI/CD service.
Along the way, I discovered that the contributor's guide
was missing
[one system-level dependency](https://github.com/calkit/calkit/commit/ae3b3bf8d969bdf1714470967da4d650bbdd2bd3).

This is very important for collaboration because there were some details
about my own laptop that I had forgotten about (hidden state),
which allow the tests to run fine on my machine,
but would fail on others.
If you're working completely alone,
maybe this doesn't matter,
but you probably want it to be easy for someone to build upon your
work so it has the maximum impact, right?
If someone can't get your project to run,
how are they supposed to build upon it?
Further,
what if you have a team working on the project?
You're going to want it to be easy for anyone on the team to contribute.
In this case, CR will help you avoid the annoying
"works on my machine" investigations.

I've heard DevOps described as "turning collaborators into contributors"
and this step makes sure the barrier to entry is as low as possible,
or at least properly described.

## The role of interactive workflows

If a given artifact you're producing requires an interactive workflow,
e.g., to open up a GUI, point and click on some things, and export,
that is a violation of CR,
since we would not be able to reproduce our entire project with a single
command.
However, interactive workflows are very important for developing batch
workflows.
Some GUI applications allow recording "macros" from interactions
that can in turn be executed in a pipeline.
In these cases,
the interactive workflow helps us develop the batch one.

This happens while developing software too.
Oftentimes one will make some small changes to some code
and setup some way to get feedback on its effect.
If automated tests are configured,
it can be faster to just run one test that one is sure will be impacted
by the code changes.
Alternatively,
a debugger can be used to step through the processes in the code and
inspect the values of variables to better check things are correct.

It's important to setup a "fixture" to get fast feedback while developing
batch processes.
However,
even if we end up running a long interactive process and it succeeds,
we should still commit the changes and run the pipeline to produce
the "official" artifact.
That is,
do not settle for any artifacts created interactively.
In other words,
the output of interactive processes should be batch process definitions.
Only batch processes should create artifacts.

The speed of testing changes is ideally instantaneous.
If it takes minutes or even hours to get feedback on if your change
works,
you probably should break it down into smaller testable chunks.
In this case,
automated unit tests can be very useful.

The frequency with which you flip back and forth between the workflow types
is important.
It should be as frequent as possible.
Discover a valuable change and integrate it back into the pipeline
right away.
Commit it to the version control system.
This is analogous to climbing a ladder one small step at a time
instead of taking one big jump.

## More small rules to follow

1. Never share an artifact you couldn't easily regenerate.
   If there are uncommitted changes in the repo, it's considered "dirty."
   Never share something created from a dirty repo.
   Commit, run the pipeline, then share.
2. Don't email editable artifacts. You will lose your single source of truth
   quickly this way.
   Instead, share artifacts that can be marked up, like PDFs,
   and incorporate those comments into the main branch.
3. Start your paper (or thesis) on day 1.
   It's going to be mostly boilerplate,
   but that's okay.
   As you go through your lit review, you'll be writing the introduction.
   As you plan your experiment and write your data processing code
   you can write the methods section.
   Again, instead of phases, make it into one continuous evolutionary process
   until it's ready to release.
4. Create project update slideshows with the same pipeline used to create
   everything else. Automate this so you're not manually copy/pasting
   things into slides each week for project updates.
5. Prefer many small changes over fewer large changes.
   Even if using version control and a pipeline system,
   it's possible to fall into a large batch mindset.

## Reusability

One common misconception one might have about sharing project files
is that they need to have some sort of broad usefulness besides
producing the figures, paper, etc.

This is not true.
In fact,
if you try to make your files more generally useful and they
no longer can do the specific tasks to generate your artifacts,
they might be even less useful.

Delivering someone a working project is valuable.
It's self-documenting,
which is much better than delivering a subset of the project with
incorrect or incomplete documentation.
This will be easier for you too.
Just archive the project as is.
No need to convert it into some format to maximize reusability.

Don't worry about reusability.
So long as your project is reproducible,
you are at least demonstrating to the world how it's done,
and they can rerun and adapt it accordingly.
If someone makes a copy of your project and changes something slightly,
it will be very clear what has changed and what needs to be regenerated.

I don't think it's important to, for example,
create a separate project with just your datasets.
Deliver the world a working project.
They will be able to see how the data is used there and reuse it in their
own case.

Realistically,
the next generation of grad students after you will be the ones reusing
your work.
If your project runs because you've kept it continuously reproducible
they are going to have a huge jump start,
even if the details of their investigation will be different.

![PhD comics 1689](/images/cr/phd-comics-1689.png)

Now imagine their materials are spread all over the place---one project
for the code,
another for the visualization,
and another for writing the thesis.
You are not going to go through the trouble to reproduce their work
and will need to reinvent the wheel.

Downstream users can continue the process,
making small changes,
rerunning,
committing,
making more small changes,
rerunning,
committing,
and they will follow the path of agility.

## Signs that you could benefit from these ideas

1. You dread the prospect of getting a new computer,
   because getting everything setup to work would take days.
2. You dread the prospect of changing a data processing script,
   because you aren't sure what else would need to be updated to keep things
   consistent.
   For example, there could be figures that need to be updated,
   or aggregate numbers listed in a paper that were entered manually.
3. You dread the prospect of updating figures because you'll need to
   manually copy files into a different project or tool to update the relevant
   publication.
4. You're the only person on your team who knows how to run the scripts in
   your project, i.e., you're working in a silo.
5. You feel like you're working on the edge of a cliff,
   like one small change would send an entire house of cards toppling down.

## Summary and conclusions

Based on the learnings from the Agile and DevOps movements,
I believe scientists can boost their productivity and quality
of their work
by applying Continuous Reproducibility principles to their projects.
This essentially means automating dependency management and
artifact generation to simplify reproducibility down to a single command.

Is it worth the extra effort?
You may think it's not, but it almost certainly is.
The gains will continue adding up over time,
so it's better to start now.
If you use a framework it may take a few hours to get setup,
and this will likely save you many hours throughout the life of the project.

The litmus test for CR is that... TODO

Working in a continuously reproducible way will provide the confidence
to share all materials associated with a research project openly.

If you want help implementing CR practices in your lab,
or want to talk about the difficulties involved,
shoot me an [email](mailto:petebachant@gmail.com) and I will probably
be willing to help you out (for free!)

## References

1. Nicholas Bloom, Charles I Jones, John Van Reenen, and Michael Web (2020).
   Are Ideas Getting Harder to Find?
   _American Economic Review_. https://doi.org/10.1257/aer.20180338.
2. Brett K Beaulieu-Jones and Casey S Greene.
   Reproducibility of computational workflows is automated using continuous
   analysis
   https://pmc.ncbi.nlm.nih.gov/articles/PMC6103790/
3. Wilson G, Aruliah DA, Brown CT, Chue Hong NP, Davis M, et al. (2014)
   Best Practices for Scientific Computing.
   PLOS Biology 12(1): e1001745.
   https://doi.org/10.1371/journal.pbio.1001745
