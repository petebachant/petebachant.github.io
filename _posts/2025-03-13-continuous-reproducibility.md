---
comments: true
date: 2025-03-13
layout: post
title: >
  Continuous Reproducibility: How DevOps principles could improve
  the speed and quality of scientific discovery
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
(validated in an end-to-end sense by reacquiring and reanalyzing raw data)
or even reproduce
(obtaining the same results by rerunning the same computational processes
on the same input data).
Though the latter is often caused by technical problems
rather than false conclusions,
I believe it is worth trying to solve these technical problems
in order to evaluate the conclusions more clearly.
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

CI means that valuable changes to code are incorporated into a single
source of truth, or "main branch," as quickly as possible,
resulting in a continuous flow of changes to the code rather than
less frequent, larger batches of changes.
CD means that these changes are accessible to the users as quickly as
possible, though the frequencies don't need to match.

CI/CD best practices ensure the code remains working and available
while evolving,
allowing the developers to feel safe about quickly making improvements.
Similarly, CR would ensure the research project remains reproducible---its
output artifacts like datasets, figures, slideshows, and publications,
remain consistent with input data and process
definitions---while allowing researchers to feel safe about making
rapid improvements.

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
Large batches of work were transferred between
different teams in the form of documentation.
Further,
the processes to test and release software were manual,
which meant they could be tedious, expensive, and/or error prone,
which meant there was an incentive to do them less often.

Removing the communication overhead by combining development
and operations teams (hence "DevOps")
so the individuals
could simply talk to each other instead of handing off documentation
and automating processes with CI/CD pipelines
made it possible to do many more iterations per unit time.
It also made it possible to incorporate fewer changes in
each batch, which helped to avoid mistakes.

Another bit of valuable automation relates to collaboration.
I've heard DevOps described as "turning collaborators into contributors."
To do this, we want to minimize the amount of effort required
to start working on a project.
Since CI/CD pipelines typically run on fresh or mostly
stateless virtual machines,
dependency management needs to be automated, e.g.,
with the help of containers and/or virtual environments.
These pipelines then serve as continuously tested documentation,
which can be much more reliable than a list of steps written in a README
by a human and never checked or updated.

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

Instead, we could think of a research project as one continuous
iterative process.
Writing can be done the entire time.
We can start writing the introduction to our first paper and thesis
right from the beginning as we start our lit review.
Data analysis and visualization code can be written and tested
before data is collected.
The methods section of a paper can be written as part of planning
an experiment, and updated while carrying it out.
Essentially, we can think of the project as one unit
instead of set of decoupled
sub-projects.

Similar to how software teams work,
we can build and deliver all project artifacts each iteration
with an automated pipeline,
keeping it continuously reproducible.
Note that in this case "deliver" could mean to our internal team if we
haven't yet submitted to a journal.
Similarly,
software teams may deliver changes that aren't released to all users publicly
until they are deemed ready.

In any case,
the correlation between more iterations and better outcomes
seems to be universal,
so at the very least,
we should look for behaviors that are hurting research
project iteration cycle time.
Here are a few I can think of:

| Problem | Slower, more error-prone solution ❌ | Better solution ✅ |
|---------|--------------|-----------------|
| Ensuring everyone on the team has the latest version of a file when it is updated. | Send an email with the file attached to everyone every time a file changes. | Use a single shared version-controlled repository for all files and treat this as the one source of truth. |
| Updating all necessary figures and publications after changing data processing algorithms. | Run downstream processes manually as needed, determining the sequence on a case-by-case basis. | Use a pipeline system that tracks inputs and outputs and uses caching to skip unnecessary expensive steps, and can run them all with a single command. |
| Ensuring the figures in a manuscript draft are up-to-date after changing a plotting script. | Manually copy/import the figure files from an analytics app into a writing app. | Edit the plotting scripts and manuscript files in the same app (e.g., VS Code) and keep them in the same repository. Update both with a single command. |
| Showing the latest status of the project to all collaborators. | Manually create a new slideshow for each update. | Update a single working copy of the figures, manuscripts, and slides as the project progresses so anyone can view asynchronously. |
| Ensuring all collaborators can contribute to all aspects of the project. | Make certain tasks only possible by certain individuals on the team, and email each other feedback for updating these. | Use a tool that automatically manages computational environments so it's easy for anyone to get set up and run the pipeline. Or better, run the pipeline automatically with a CI/CD service like GitHub Actions. |

What do you think?
Is it worth the effort to make a project continuously reproducible
and check it many times per day?
I think it is, though I'm biased,
since I've been working on tools to make CR easier to do
([Calkit](https://calkit.org);
cf. [this example CI/CD workflow](https://github.com/calkit/example-basic/blob/main/.github/workflows/run.yml)).

One argument against setting up an automated CR framework for your
project is that you do very few "outer loop" iterations.
That is, you are able to effectively work in phases so, e.g.,
siloing the writing away from the data visualization is not slowing you down.
I would argue, however, that analyzing and visualizing data
concurrently while it's being collected is a great way to catch
errors.
If the paper is set up and ready to write during data collection,
important details can make their way in directly,
removing a potential source of error from transcribing lab notebooks.

```mermaid
---
title: Outer loop(s)
---
flowchart LR
    A[collect data] --> B[analyze data]
    B --> C[visualize data]
    C --> D[write paper]
    D --> A
    C --> A
    D --> C
    D --> B
    C --> B
    B --> D
    B --> A
```

```mermaid
---
title: Inner loop
---
flowchart LR
    A[write] --> B[build]
    B --> C[review]
    C --> A
```

Using Calkit or a similar workflow like that of
[showyourwork](https://show-your.work),
outer and inner loop iterations can happen in the same tool.
I assume there is some potential for efficiency gain there.
Imagine the overhead of your current process if you want to perform
a single outer loop iteration and how effectively you can predict
when one will be required.

Another argument against applying CR to research projects
is that software products are supposed to have long lives,
whereas one could argue research project materials typically should have short
lives,
except for a long-lived publication, or in the case that the research
is done to support a more generally useful software product.
This would lead us to believe that there should be few iterations.
Maybe the important cycle time is not the iterations within a given study,
but at a higher level---iterations between studies themselves.

However, one could argue that delivering a fully reproducible
project along with a paper provides a working
template for the next study, effectively reducing that "outer outer loop"
cycle time.
If CR practices mean that it's easy to get set up
and run, and again, the thing actually works,
perhaps the next study can be done more quickly.
Even if it's just one day per study saved,
imagine how that compounds over time.
I've heard quite a few stories of grad students being handed code
from their departed predecessors with no instructions on how to run it,
no version history, no test suite, etc.,
and apparently that's common enough to make a PhD Comic about it:

![PhD comics 1689](/images/cr/phd-comics-1689.png)

If you're convinced on the value of,
or are just curious enough about Continuous Reproducibility and
want help implementing CI/CD/CR practices in your lab,
shoot me an [email](mailto:petebachant@gmail.com) and I will hopefully
have time to help you out (for free!).

## References and recommended resources

1. Nicholas Bloom, Charles I Jones, John Van Reenen, and Michael Web (2020).
   Are Ideas Getting Harder to Find?
   _American Economic Review_.
   [10.1257/aer.20180338](https://doi.org/10.1257/aer.20180338)
2. Brett K Beaulieu-Jones and Casey S Greene (2017).
   Reproducibility of computational workflows is automated using continuous
   analysis. _Nat Biotechnol._
   [10.1038/nbt.3780](https://pmc.ncbi.nlm.nih.gov/articles/PMC6103790/)
3. Toward a Culture of Computational Reproducibility.
   [https://youtube.com/watch?v=XjW3t-qXAiE](https://youtube.com/watch?v=XjW3t-qXAiE)
4. There is a better way to automate and manage your (fluid) simulations.
   [https://www.youtube.com/watch?v=NGQlSScH97s](https://www.youtube.com/watch?v=NGQlSScH97s)
