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
and many findings are failing to be replicated
(validated in an end-to-end sense, re-acquiring and reanalyzing raw data)
or even reproduced
(verified by rerunning the same computational processes
on the same input data).
Researchers already borrow plenty of tooling and practices from
the software world,
but I believe those mentioned above have not yet crossed over.

Here I will focus on one set of practices in particular:
those of _Continuous Integration_ and _Continuous Delivery_
([CI/CD](https://en.wikipedia.org/wiki/CI/CD))),
which could manifest as something we might call
_Continuous Reproducibility_ (CR) in the research world.
Making it easier to adopt CR practices is one of the primary goals
of [Calkit](https://calkit.org).

At the core,
the agile, lean, DevOps, and related movements are about breaking down silos
and working in small batches with faster feedback loops.
These are beneficial in scenarios where solutions,
and sometimes even problems, are not fully understood, i.e.,
they are about making decisions and taking action under high uncertainty.
Does that sound like scientific research to you?

These outcomes are achieved with automation.
Code is automatically tested to ensure it can be safely incorporated.
Code is automatically deployed to remove the pain of any manual procedures,
so it can be done more frequently.
Code is accessible to all team members and CI/CD operates on an
independent computing system
so the knowledge on how to test and deploy is not siloed in a subset
of the team, or worse, a single individual.

Many research projects involve some sort of code,
even if they're not seeking to build software products.

You might argue that a PI needs to be siloed away from the grad students
and postdocs because they have other roles.
However, this siloing will produce inefficiency.

The later in the process an error is found,
the more expensive it is to fix.

Even more fundamentally,
these are about reducing complexity.
Instead of putting things in many different boxes
with intricate interfaces between them and a grand plan of orchestration,
put a single box and define the desired outputs.
At least strive to do this as much as possible.
This is related to the concept of premature abstraction.
You are in a constant battle against entropy,
and if you start falling behind your work will slow down
and you're more likely to make mistakes.
Gall's law... TODO

CI/CD has taught the software industry that it is well worth
the upfront investment.

Silos and large batch flows show up in the process of software development
when following a so-called
["waterfall"](https://en.wikipedia.org/wiki/Waterfall_model)
project management model,
where the project moves through discrete stage gates.
Each phase is often owned by a different (siloed) team,
and involves a large batch of work that needs to be handed off for the next
stage.
These phases may be:

1. Market research
2. Requirements definition
3. Design
4. Implementation
5. Testing
6. Integration
7. Delivery

Software engineers learned that under conditions of high uncertainty,
these large batches of work can often produce large amounts of waste,
as full knowledge of the market's problem and ideal solution
cannot be known up front.
Thus, instead of one big waterfall,
the project can be broken down into many small cycles
where teams collaborate cross-functionally.
That is, those with knowledge of the market work alongside designers,
who work alongside engineers to iterate towards the optimal solution
on timescales measured in days instead of months, quarters, or years.

CI/CD turn the later stages (4--7) into one continuous process with
many small steps, where implementation, testing, integration,
and delivery are owned by the same team,
and again, often done multiple times per day instead of once at the end.
This is possible thanks to the use of automated testing and deployment
pipelines.
As developers create valuable changes,
they are integrated into a single source of truth,
a so-called "main branch,"
right away.
Confidence that nothing has broken comes from running a suite of
automated tests.
This single source of truth is then delivered to the users as quickly
as possible,
where the constant stream of small improvements provides much less
disruption to their usage compared to infrequent "big bang" releases.

But how does this relate to scientific research?
Where do silos and large batch flows show up in science?
One might model the modern scientific process as a waterfall,
with stages like:

1. Request for proposal
1. Proposal
1. Study design
1. Study implementation
1. Analysis
1. Writing
1. Peer review (testing)
1. Publication (delivery)
1. Reproduction
1. Replication

Now, turning this entire process into one with frequent feedback
loops and cross-functional collaboration is outside the scope of this article,
though one could imagine there is room for efficiency gains, e.g.,
by eliminating the proposal phase and simply funding capable teams to
work on the research gaps that they discover in a time-boxed manner.
Instead, here we will focus on phases 4--9.

It's important to clarify that
peer review and delivery happen inside a research
group before publishing results to the larger world
(though preprints do deliver externally earlier),
very similar to what happens inside a software product team.
A researcher may make some changes to simulation or data processing code,
which in turn leads them to produce a figure,
and perhaps write some text in a draft of an article.
This draft may be delivered to the principal investigator (PI)
for review.
I am arguing that there are productivity gains to be had by shortening
this feedback loop.
It is here where Continuous Reproducibility practices can help speed things up
with automation.

Graduate students may meet with their advisors weekly to give progress updates.
As part of this ritual they may need to create new slide shows
with the latest results.
This is a significant effort, and these slideshows will often be thrown
away.
A CR workflow would advocate starting the writing process early,
even from the very beginning of the project,
and using that as the single source of truth for the project status,
slowly evolving it into a publishable state.

One important missing principle is a holistic view.
The project should be the important unit.
Yes, there are modules and subcomponents,
but these all exist in a larger picture.
Practically speaking,
this means all files belong together in a single collection.
This includes proposals, notes, drawings, data, code, figures, slideshows,
articles, etc.

I was looking back at my research materials from my master's thesis the other
day, and I noticed how this holistic view was not taken.
Every small task got its own folder,
and these were interspersed with folders related to coursework
and other administrative documents.
I recommend that all files related to research on a given topic belong
in one folder.
Yes, there can be subfolders, but don't try to create silos between them
up front.

These workflows can be distinguished by how long "throwaway" work
lives without being incorporated into the single source of truth.

A non-CR workflow would be...

The "throwaway" work should only exist for minutes instead of days.
Again, to draw the analogy to software development,
some interactive development (e.g., using a debugger)
can be done for minutes to hours,
a valuable change is discovered,
and a "pull request" is submitted.
Working on a potential change for many days, weeks, or even months
is a bad practice.

Let's first start with some principles:

1. The research project itself should be thought of as a single unit.
   It is not helpful to silo the data analysis phase from the writing phase.
   These are inherently coupled, and treating them as if they are not will
   be less efficient.
2. A single command should kick off everything.
   No lists of setup steps.
   No "go into this folder and run ..., then go into this folder and run..."
   You will probably not describe these instructions accurately enough,
   so automate them into a single pipeline.

Continuous Reproducibility similarly will rely on automation.
Every small change to a research project should trigger an automated
CR process, so the single source of truth remains consistent at all times.

The practitioners of research borrow many habits
and tools from the software development world,
which makes sense given that so much of work of researchers relies on computers,
but I believe the DevOps strategies of continuous integration
and continuous delivery (or deployment;
[CI/CD](https://en.wikipedia.org/wiki/CI/CD))
is the next important
concept researchers can borrow from the software development community.
This could be called _Continuous Reproducibility_ (CR).
It has also been described as
[_Continuous Analysis_](https://arxiv.org/abs/2411.02283),
though I think the concept extends beyond analysis and into
generating other artifacts like figures and publications.

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

Coincidentally,
today I was setting up a CI pipeline for
[Calkit](https://github.com/calkit/calkit).
Even though the tests all run fine on my machine,
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

Automated testing then makes developers feel safe that the
changes they're about to incorporate don't break anything.
Similarly,
automating research projects...

The CR pipeline is like a CD pipeline.
It is run every time a change is incorporated so there is a single
source of truth for the project that includes everything.

Research projects are not quite the same as software projects.
For one, most software projects, if successful, don't end.

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

A core mindset shift is from thinking of a bunch of disparate
artifacts created in discrete phases to
the project itself as a whole that evolves continuously.
It may reach milestones along the way,
but the project is the most important unit.

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

So instead of having a "create repro pack" phase,
the entire project repo should be a repro pack from the very start.
This is enabled by CR.

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
1. Generate all artifacts with a single pipeline. The opposite of this would
   be having one pipeline to run the simulation,
   one to post-process, one to generate figures,
   one to compile the publication,
   all of which need to be executed separately by the researcher.
   A pipeline system that can cache results is critical here if there are
   expensive steps, but more on that later.

The change in mindset is a move from focusing on individual files
and artifacts to a focus on the project as a whole.
For example,
thinking that the data processing code is done
and now the writing can start is not a CR mindset.
The review process, internal or external,
will undoubtedly uncover necessary changes.
If an automated CR pipeline is not in place,
the extra work from these iterations will accumulate.
Put the CR pipeline in place from the very beginning!

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

## The biggest mindset shift

Monorepo.
Don't allow complexity to explode by letting your project turn into many
projects.

## Reducing pain through automation

The more painful a process is,
the less likely someone is to do it.
If this process also leads to improved quality,
quality will suffer.
Therefore,
it's important to automated things to reduce pain and uncertainty.

## The interactive/batch dance

Interactivity is the enemy of reproducibility.
Interactivity produces mostly throwaway work.
Interactive work is converted into batch work if it is deemed valuable.

CR says not that we should eliminate interactive work,
but that the value uncovered by interactive work should be incorporated
into a batch process as quickly as possible,
which will manifest as small changes.

## Examples of CR workflows

Microsoft Excel.
If you could do everything in Excel,
that would count as a CR workflow.
Now, there are many reasons you shouldn't do that,
but it fits the criteria:

1. Version controlled
2. Outputs are consistent with inputs and process definitions

## An analogy: The journey and the destination

The destination is the paper.

CR is building a trail and saving GPS coordinates along the route,
since you'll be going back and forth often.

Non-CR, at best,
is creating a map from memory at the destination.
At worst,
it's getting to the destination, taking a photo,
and leaving it at that.

It's actually really important for others to be able to get to where
you got so they can go further.
But if you don't even know how you got there...

The less automated your workflow, the more likely it is to be wrong.

## Tactics for continuous reproducibility

If you've read this far, hopefully you're convinced that your project
should remain reproducible on a daily basis.
So how can we achieve that?

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

### Do run all processes as part of the pipeline

Even if you've gotten things to run in an interactive way,
and you think the results won't change if you run in batch mode,
do it anyway.

### Do use a CI/CD service if possible

For example,
run your pipeline on GitHub Actions.
See [this example](https://github.com/calkit/example-basic/blob/main/.github/workflows/run.yml)
for a Calkit project that runs automatically.

TODO: This should be an example of one that runs on every PR.

## But what if I'm already halfway done?

That's okay.
You can start working reproducibly from now.
At least you can put everything you have right now into version control,
then start adding to the pipeline for everything that needs to be
created after.

## Problems CR avoids

- Do I need to rerun this script/notebook? It's kind of heavy.

## Premature abstraction and the curse of design

Keep your project general at first.
That is, dump all files into a single place.
Don't split into a bunch of different projects,
e.g., one for your proposal, one for the experiment,
one for the analysis code,
one for the journal article,
and one for the thesis.

It's almost always better to go from large to small than the other way
around.
In software development,
this principle is known as premature abstraction,
and it is well known that the wrong abstraction is much more expensive
than no abstraction at all.

A similar concept is that of a "monorepo,"
or a single repository containing multiple sub-projects.
This is much better than excessive fragmentation.
In fact,
Google uses a single monorepo for most of their code.

## 'Trunk-based' development

Experimentation is necessary,
and this doesn't just mean scientific experiments.
Trying out a different way of processing or visualizing data could lead
to a more effective approach.

Instead of deploying different versions of the code...

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

### Prose dependency management

This isn't as bad as prose pipelines, but still should be avoided.

### DIY caching logic

Caching is one of the hardest tasks in software engineering.
Offload that responsibility to a framework.

### Multiple pipelines

Coincidentally,
the ["repro pack" attached to [1]](https://doi.org/10.3886/E111743V2)
appears to have 10 separate pipelines,
with no instructions on how to run them,
if there is any inter-dependence, etc.

It also doesn't contain the paper manuscript compilation.

### Not using a framework

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

## Start your paper (and thesis) on day 1

It's going to be mostly boilerplate,
but that's okay.
As you go through your lit review, you'll be writing the introduction.
Again, instead of phases, make it into one continuous evolutionary process
until it's ready to release.

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

## Open science

Working in a continuously reproducible way will provide the confidence
to share all materials associated with a research project openly.

## How big should a project be?

We've already established that we want to move away from
very small projects, but what's the limit?
Should we draw the line at a single paper?
What if we have a follow-on investigation on the same topic?

## Tooling

Researchers at the frontier of open science and reproducibility
use tools and platforms developed for software development
because there are striking similarities.

However, I do believe research is different enough from software
development to warrant new tooling.

Calkit is designed to help:

- Focus on the project as the most important unit of work.
- Continuously integrate small changes and keep the "build" up-to-date.

## Don't be afraid to repeat yourself

Staying loosely, or non-coupled and reproducible is more important than
not repeating code.

## A real world example

Toy projects are one thing,
but what about a real one?

When I was working on my PhD,
I followed some of these principles,
but not all of them.
Recently,
I converted my entire PhD into a single project,
reproducible with a single command.
Though some pipeline steps are "frozen"...

All releases have been created appropriately...

Subprojects...

Could I have built this up from scratch?

Start thesis from the beginning.

Reproducibility flaws in this project:
- Sandia Red Mesa

## Objections

>But the dataset/code is the only thing of value w.r.t. reusability from my
>project, so why share all the other stuff?

Does sharing all the other stuff prevent users from taking just what
they want/need?
At the very least, the rest of your project will serve as documentation
for how the datasets, etc., can be used,
and if the project reproduces,
that documentation will be _true_.

>Reproducing someone else's project isn't that important.
>As long as the equations
>in the paper are correct,
>I can just reimplement on my own.

If the computations don't reproduce,
and the computations are supposed to be evidence of the equations being
true,
how can we assume that there is any valid evidence for the equations
being true?
Journal referees are definitely not replicating results as part of the
review process,
and I doubt they are reproducing results either.

## Are you practicing continuous reproducibility: A test

1. Can anyone on the team view a single source of truth for the project files
   at any time?
2. Can the project run on anyone's computer?
3. Is there some objective and automated way to check if the project is in consistent state?

PIs may say they're too busy to get involved in the lower level activities,
that they need the grad students and postdocs to provide them with weekly
summary reports.

That may be the case.
However, these reports should be generated automatically.
And to do so, researchers should practice CR.

## Research projects are not (always) software projects, and researchers don't necessarily need to be software engineers

## References

1. Nicholas Bloom, Charles I Jones, John Van Reenen, and Michael Web (2020).
   Are Ideas Getting Harder to Find?
   _American Economic Review_. https://doi.org/10.1257/aer.20180338.
2. Brett K Beaulieu-Jones and Casey S Greene.
   Reproducibility of computational workflows is automated using continuous
   analysis
   https://pmc.ncbi.nlm.nih.gov/articles/PMC6103790/
