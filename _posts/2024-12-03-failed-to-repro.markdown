---
comments: true
date: 2024-12-03
layout: post
title: I failed to reproduce my own results from a decade ago
categories:
  - Open science
  - Reproducibility
---

I recently received an email from my former PhD advisor
introducing me to a grad
student who was interested in using some experimental data I had collected a
decade ago to validate his simulations.
The repo from the experiment was still up on
[GitHub](https://github.com/UNH-CORE/RVAT-Re-dep),
so I figured that would be easy,
but I was wrong.

In the README, I had instructions for getting started and regenerating
the figures:

![The README.](/images/repro-fail/readme.png)

So I gave it a try.
These days I have
[Mambaforge](https://conda-forge.org/download/)
installed on my machine instead of Anaconda,
but the ecosystems are largely compatible with each other,
so I figured I could give it try.
The `pip install` commands worked fine,
so I tried running `python plot.py` to generate the figures,
but that actually
doesn't do anything without some additional options
(bad documentation, me-from-the-past,)
which was at least apparent from the help output printed to the terminal.
I then ran the correct command,
`python plot.py --all` to generate all of the figures,
and here was the result:

![The initial plot all call.](/images/repro-fail/plot-all-initial.png)

As we can see,
I failed to reproduce the figures because
the interface to the `scipy.stats.t.interval` function had changed since the
version I was using back then.

The naive approach failed, which isn't necessarily surprising after
a full decade of software changes.
This puts us at a crossroads if we're truly going to try to reproduce
these results.
There are two options:

1. Attempt to reproduce the environment in which this ran initially.
1. Adapt the code for newer dependencies.

But let's take a step back and question why we want to do this at all.
What is the point of trying to reproduce these figures?
I can think of two reasons:

1. Reproducing the results can help ensure there are no mistakes,
   or that the outputs (figures) genuinely reflect the inputs (data)
   and procedures (code). There is a chance that I updated the code at some
   point but never reran `plot.py`, so the figures are out-of-date.
   This is quite unlikely though. I remember running this script many times
   after processing the data to get the figures just right.
1. We want to produce a slight variant of one or more figures, adding
   the results from a simulation for the purposes of validation.

We can call these reproducibility and _reusability_, respectively.
These map fairly well to the strategies above too.
That is,
reproducing the original environment is a reproducibility task,
and adapting the code is a reusability one.
Both are important, but at this point I would prioritize reusability,
where the project materials can be used to created new knowledge instead of
simply repeating the past.
However, I wanted to see what it would take to achieve both.

## Attempting to reproduce the old environment

Before we start, let's pick a figure from the original paper to focus
on reproducing.
For this I chose one that's relatively complex.
It shows out-of-plane mean velocity in a turbine wake as contours
and in-plane mean velocity as vector arrows,
and includes an outline of the turbine's projected area.
It uses LaTeX for the axis labels, and is set to match the true aspect
ratio of the measurement plane.
Here's what it looked like published:

![Reference figure.](/images/repro-fail/ref-figure.png)

I left myself some incomplete instructions for reproducing the old
environment: Install a version of Anaconda that uses Python 3.5
and `pip install` two additional packages.
Again, bad documentation, me-from-the-past!
Given that I already have `conda` installed,
I figured I could generate a new environment with Python 3.5
and take it from there.

![Attempting to create a Python 3.5 environment.](/images/repro-fail/mamba-create-py35.png)

No luck. Python 3.5 is not available in the `conda-forge` or `main`
channels any longer,
at least not for my MacBook's ARM processor.

The next possible avenue was Docker.
There are some old Anaconda Docker images up on Docker Hub,
so I thought maybe I could use one of those.
The versions don't correspond to Python versions,
however,
so I had to search though the
[Anaconda release notes](https://docs.anaconda.com/anaconda/release-notes)
to find which version I wanted.
Anaconda 2.4.0, released on November 2, 2015,
was the first version to come with Python 3.5,
and that version is available on Docker Hub,
so I tried to spin up an interactive container:

![Docker run Anaconda.](/images/repro-fail/docker-run.png)

To my surprise, this failed.
Apparently there was a change in Docker image format at some point and these
types are no longer supported.
So I searched for the newest Anaconda version with Python 3.5,
which was Anaconda 4.2.0,
and luckily the image was in the correct format.

At this point I needed to create a new image derived from that one that
installed the additional dependencies with `pip`.
So I created a new Docker environment for the project
and added a build stage to a
fresh DVC pipeline with
[Calkit](https://github.com/calkit/calkit)
(a tool I've been working on inspired by situations like these):

```sh
calkit new docker-env \
    --name main \
    --image rvat-re-dep \
    --from continuumio/anaconda3:4.2.0 \
    --description "A custom Python 3.5 environment" \
    --stage build-docker
```

In this case, the automatically-generated `Dockerfile` didn't yet have
everything we need, but it's a start.

Simply adding the `pip install` instructions from the README resulted in
SSL verification and dependency resolution errors.
After some Googling and trial-and-error,
I was able to get things installed in the image by adding this command:

```dockerfile
RUN pip install \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    --no-cache-dir \
    progressbar33 \
    seaborn==0.7.0 \
    pxl==0.0.9 \
    --no-deps
```

Note that I had to pin the `seaborn` version since `pxl` would install a
newer version, which would install a newer version of `pandas`,
which would fail, hence the `--no-deps` option.

I also had to set the default Matplotlib backend with:

```dockerfile
env MPLBACKEND=Agg
```

since PyQt4 was apparently missing and Matplotlib was trying to import it
by default.

After calling `calkit run`, which ran the pipeline to build the Docker image,
I ran the plotting script in that environment with:

```sh
calkit runenv -n main -- python plot.py all_meancontquiv --save
```

We can then take a look at the newly-created figure
(with the published version shown again below it):

![Reference figure generated with Python 3.5](/images/repro-fail/ref-figure-docker-py35.png)

![Reference figure.](/images/repro-fail/ref-figure.png)

And we got pretty darn close!
If you look closely you'll notice the font for the tick labels
is slightly different from the published version,
since I believe I had installed the Arial font on my machine back then,
which isn't present by default in this Docker image since it is a
Microsoft font.
We could go further and try to install the fonts into this image,
but I'm going to call this a win for now.
It took some hunting and finagling, but we reproduced the figure.

## But what about reusability?

If we look back at this project's README above we can see I said absolutely
nothing about how to reuse these materials.
I didn't describe the data or code or how to use them.
Now, to be fair to myself,
at the time the main purpose of open-sourcing these materials
was to open-source the materials.
Even that is still rare for research projects,
and I do think it's the right thing to do.
However, if we want to ensure our work has the most impact possible,
we should spend some time thinking about how
users can derive value from any of the materials,
not just the paper we wrote.

I actually used this dataset in a later paper validating some CFD simulations,
the repo for which is
[also on GitHub](https://github.com/petebachant/CFT-wake-modeling-paper).
Looking in there,
the value that the dataset's repo provided was:

1. CSV files containing statistical data.
1. A Python package that made it possible to:
    1. [recreate the Matplotlib figures](https://github.com/petebachant/CFT-wake-modeling-paper/blob/master/scripts/makefigs.py#L69)
       so we didn't need to copy/paste them,
    1. instantiate a `WakeMap` Python class that computed various gradients to
       aid in
       [computing wake recovery quantities](https://github.com/petebachant/CFT-wake-modeling-paper/blob/master/scripts/makefigs.py#L262)
       to compare against simulation,
    1. inspect the code that generated complex figures so it could be
       [adapted for plotting the CFD results](https://github.com/petebachant/UNH-RVAT-3D-OpenFOAM/blob/4496430e05f9aed170fceed714363fed2095d1d7/pyurof3dsst/plotting.py#L82).

Now, items 2.1 and 2.2 were actually not that easy to do,
since the Python package was not installable.
I actually had to add the folders to `sys.path` to import the packages,
and they used relative paths,
so I had to change directories in order to load the correct data.
This is somewhat of an easy fix though.

First, we can make the Python package installable by
[adding a `pyproject.toml` file](https://github.com/UNH-CORE/RVAT-Re-dep/commit/426e35c407fd52f3e639462c22c41fc779849be9).
Then we can
[switch to using absolute paths](https://github.com/UNH-CORE/RVAT-Re-dep/commit/e22523d6f6d7f5f09a103c27dabeed3d6b0278d7#diff-a07a3aaaea2bef878af1e0059f5743fc3380fab5ff8ba9e9b07713641bcf3690)
so the data loading and plotting functions
can be called from outside.

Lastly, we should add some documentation explaining how to reuse
the materials.
I ended up adding two sections to the
[README](https://github.com/UNH-CORE/RVAT-Re-dep?tab=readme-ov-file#unh-rvat-reynolds-number-dependence-experiment):
one for reproducing the results and one for reusing the results.
I also created an example project reusing this dataset by including it as
a Git submodule, which you can also view
[up on GitHub](https://github.com/petebachant/reuse-rvat-re-dep).
Doing this is a good way to put yourself in the users' shoes
and can reveal stumbling blocks.
It also gives users a template to copy if they would find that helpful.

## Conclusions

Simply providing the code and data without documentation is better than
nothing,
and many papers don't even go that far.
However,
we should actually go further.
Every project should describe the steps both to reproduce and reuse the
outputs.

### On reproducibility

It's hard.
Technology marches onwards.
We probably can't expect unlimited computational reproducibility
on any hardware.
Just like I can't simply run a punch card program on my laptop,
some code will just not last forever.
Technologies like Docker can help us a lot here,
but we need to be realistic.

Reproducibility is most valuable at the present time of the work
being done.
It can help them ensure researchers don't make mistakes.
It can help speed up peer review.
It can help ensure all team members can effectively work on the same
project.

Sometimes it might not even be that valuable later on,
since value comes in reusability.

## On reusability

Researchers should do some product management work to ensure they are
delivering value to the world.

I feel like I've said a word too many times and now I forget the meaning.

The wrong abstraction is worse than no abstraction.

On the other hand,
reproducibility is not the same thing as reusability.
Each serves a different purpose.
Reproducibility is ensuring correctness in the present,
and reusability is ensuring value for the future.
Both are important.

If we want the products of research to be usable far into the future
we need to focus on keeping them as simple as possible,
and we might need to do some maintenance to them over time.

One of the most important reproducibility principles that arises
is to keep everything in one place:
Source code, data, environment definitions (including fonts).
Docker and DVC help here.
What we're trying to achieve is portability.
Try not to depend on too much that is not accurately described in the
repo itself.

If I were to do something like that CFD paper over again, I would use
a monorepo for the entire project with Git submodules for work done previously,
and I would keep every single file in version control,
with the larger raw results using DVC,
and build the entire project around a single pipeline
rather than a bunch of custom manually-executed sub-pipelines.

We need to think like product managers a bit and try to imagine
simple ways to derive value from what we produce.
It's nice if we can provide a simple recommendation or hand calculation,
but in many cases some sort of complex computational workflow is shown in
a paper, where readers are left to their own devices regarding how to
actually use the workflow.

So at a bare minimum, you should still be sharing everything.
It should be reproducible.
If you want to have the most impact, be thoughtful about the products
of your research and how they can deliver the most value.

Overall, I'd give myself a B- for reproducibility and reusability
here.
The data and code were made openly available and
cited in the relevant paper.
However, as a product, this repo is not really easy to reuse.
The CSVs of processed data are the core of the value,
and maybe the plotting code provides some value for copy/pasting,
but again, these require copying and pasting,
which doesn't necessarily leave breadcrumbs for further reuse.

The changes we made here did not make our project completely self
contained.
For instance,
we are still depending on Dockerhub to not delete that Anaconda image
we're using as our base to build ours.
We should probably push the image somewhere.
Even if we did that, however,
Docker could stop supporting that image format,
leaving us unable to reproduce this again.
We're depending on the Python Package Index (PyPI) to retain those versions
of `progressbar33` and `pxl` for us to download.
We're depending on the Debian archives to stay up.
Is true reproducibility a real goal here?

So what are the takeaways here?
Reproducibility has an expiration date?
Reusable products need to be carefully thought about to minimize
their dependencies?

Should we treat these bundles of data and code as products that require
maintenance?
Or should we simply hand them off to the world and move on?
Do we have some obligation to treat these as products and ensure they
deliver value to the users,
or is enough to simply provide all of the materials?

Perhaps this project as a whole can be treated as a starting point
for the user, and they can morph it to their own ends?

Though I will acknowledge that in some cases the only value you
can possibly derive from some work is a simple hand calculation,
that is increasingly rare as research becomes more complex.
In many cases, the real value we can provide is through
delivering datasets and software.

Avoid complexity!

Do you have some results for which you'd like to check the reproducibility?
I might be willing to give it a shot as well.
Shoot me an email!
