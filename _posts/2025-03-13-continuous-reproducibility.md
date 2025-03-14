---
comments: true
date: 2025-03-13
layout: post
title: >
  Continuous Reproducibility: Could DevOps principles significantly improve
  the quality and speed of scientific discovery?
categories:
  - Open science
  - Reproducibility
  - Software engineering
---

In the 21st century, the
[Agile](https://en.wikipedia.org/wiki/Agile_software_development)
and [DevOps](https://en.wikipedia.org/wiki/DevOps) movements
revolutionized software development,
reducing waste, improving quality,
enhancing innovation,
and increasing the speed at which software products and related
technology could be brought into the world.
At the same time, the
[pace of scientific innovation appears to be slowing](https://doi.org/10.1257/aer.20180338) [1],
with many findings failing to replicate
(validated in an end-to-end sense by re-acquiring and reanalyzing raw data)
or even reproduce
(obtaining the same results by rerunning the same computational processes
on the same input data).
Though the latter is often caused by technical problems
rather than false conclusions,
I believe it is worth trying to solve these technical problems
so that we'll be able to evaluate the conclusions more clearly.
Towards this end I think there are some ideas we could borrow from the
software world to help.

Here I will focus on one set of practices in particular:
those of _Continuous Integration_ and _Continuous Delivery_
([CI/CD](https://en.wikipedia.org/wiki/CI/CD)).
There has been some discussion about adapting these
under the name
[_Continuous Analysis_](https://arxiv.org/abs/2411.02283),
though I think the concept extends beyond analysis and into
generating other artifacts like figures and publications.
Therefore, here I will use the term
_Continuous Reproducibility_ (CR).

In its less mature era,
software was built using the traditional
[waterfall](https://en.wikipedia.org/wiki/Waterfall_model)
project management methodology.
This approach broke projects into distinct phases or "stage gates," e.g.,
market research, requirements gathering,
design, implementation, testing, deployment,
which were intended to be done in a linear sequence,
with each taking weeks or months to finish.
The problem with this approach is that it only works for projects
with low uncertainty, i.e.,
those where the true requirements can easily be defined up front
and no new knowledge is uncovered between phases.
These situations are of course
rare in both product development and science.

These days, all of the phases are happening
continuously and in parallel.
The best teams are deploying new changes
[many times per day](https://www.atlassian.com/devops/frameworks/devops-metrics),
because generally, the more iterations, the more successful the product.

But it's only possible to do many iterations if cycle times can be shortened.
In the old waterfall style,
full cycle times were on the order of months or even years.
Large batches of work were thrown over the wall between
different teams in the form of documentation.
Further,
the processes to test and release software were manual,
which meant they could be tedious and expensive,
which meant there was an incentive to do them less often.

Removing the communication overhead by combining teams
so they could simply talk to each other instead of handing off documentation
and automating processes with CI/CD pipelines
made it possible to do many more iterations per unit time.
It also made it possible to incorporate fewer changes in
each batch, which helped to avoid mistakes.

Another bit of automation relates to collaboration.
I've heard DevOps described as "turning collaborators into contributors."
To do this, we want to minimize the amount of setup required
to start working on a project.
Since CI/CD pipelines typically run on fresh or stateless virtual machines,
dependency management had to be automated,
which made it easy for developers to setup their machine to start
working on the project.

So how does this relate to research projects, and are there potential
efficiency gains if these practices were to be adopted?

In some cases we might find ourselves thinking in a waterfall mindset,
where we want to do our work in distinct phases,
e.g., planning, data collection, data analysis, figure generation,
writing, peer review.
But is this really best modeled as
a linear waterfall process where nothing is learned between
phases?
Do we never, for example, return to data analysis after starting the writing
or peer review process?

Alternatively, we can think of a research project as one continuous
iterative process.
Writing can be done the entire time.
We can start writing the introduction to our first paper and thesis
right from the beginning as we start our lit review.
Data analysis and visualization code can be written and tested
before data is collected.
The methods section of a paper can be written as part of planning
an experiment.
Basically, think of the project as one unit instead of bunch of decoupled
sub-projects.

Similar to how software teams work,
we can build and deliver all project artifacts with each iteration
with an automated pipeline.
Note that in this case "deliver" could mean to our internal team if we
haven't yet submitted to a journal.
Similarly,
software teams may deliver changes that aren't released to all users publicly
until they are deemed ready.
By using automation we can ensure our project remains
continuously reproducible.

In any case,
the relationship between more iterations and a better outcome
seems to be universal,
so at the very least,
we should look for behaviors that are hurting research
project iteration cycle time.
Here are a few I can think of:

| Problem | Bad solution ❌ | Better solution ✅ |
|---------|--------------|-----------------|
| Ensuring everyone on the team has the latest version of a file when it is updated. | Send an email with the file attached to everyone every time a file changes. | Use a single version-controlled repository for all files and treat this as the one source of truth. |
| Updating all necessary figures and publications after changing data processing algorithms. | Run downstream processes manually as needed. | Use a pipeline system that tracks inputs and outputs and uses caching to skip unnecessary expensive steps, and can run them all with a single command. |
| Ensuring the figures in a manuscript draft are up-to-date after changing a plotting script. | Manually copy/import the figure files from an analytics app into a writing app. | Edit the plotting scripts and manuscript files in the same app (e.g., VS Code) and keep them in the same repository. Update both with a single command. |
| Compiling a document to show the latest status of the project. | Manually create a new slideshow for each update. | Update a single working copy of the manuscript and slides as the project progresses. |
| Ensuring all collaborators are using the same software and library versions. | Send out an email when these change, telling the team what to install. | Use a tool that automatically manages computational environments. |

What do you think?
Is it worth the effort to make a project continuously reproducible?
I think it is, though I'm biased,
since I've been working on things to make it easier to apply
([Calkit](https://calkit.org)).
It would be interesting to test, perhaps with some research.

On argument against applying CR to research projects
is that software products are supposed to have long lives,
whereas research project materials typically should have short lives,
except for a long-lived publication.
Maybe the important cycle time is not the iterations within a given study,
but at a higher level---iterations between studies themselves.

However, one could argue that delivering a fully reproducible
project along with a paper provides a working
template for the next study.
If CR practices mean that it's easy to get setup
and run, and again, the thing actually works,
perhaps the next study can be done much more quickly.
I've heard quite a few stories of grad students being handed code
from their predecessors with no instructions on how to run it,
no version history, no test suite, etc.,
and apparently that's common enough to make a PhD Comic about it:

![PhD comics 1689](/images/cr/phd-comics-1689.png)

In my experience,
having a working example,
even if it doesn't do exactly what you want it to do,
is a great way to jump start a new project.
In fact,
that's how I built the
[Calkit Cloud](https://github.com/calkit/calkit-cloud),
and I learned the React front end framework by reading through
the template I started with
rather than by starting with the documentation and starting from scratch.

If you want help implementing CI/CD/CR practices in your lab,
or want to talk more about the details and difficulties involved,
shoot me an [email](mailto:petebachant@gmail.com) and I will probably
have time to help you out (for free!)

## References

1. Nicholas Bloom, Charles I Jones, John Van Reenen, and Michael Web (2020).
   Are Ideas Getting Harder to Find?
   _American Economic Review_.
   [https://doi.org/10.1257/aer.20180338](https://doi.org/10.1257/aer.20180338).
2. Brett K Beaulieu-Jones and Casey S Greene.
   Reproducibility of computational workflows is automated using continuous
   analysis.
   [https://pmc.ncbi.nlm.nih.gov/articles/PMC6103790/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6103790/)
3. Toward a Culture of Computational Reproducibility.
   [https://youtube.com/watch?v=XjW3t-qXAiE](https://youtube.com/watch?v=XjW3t-qXAiE)
