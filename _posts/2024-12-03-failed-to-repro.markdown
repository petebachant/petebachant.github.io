---
comments: true
date: 2024-12-03
layout: post
title: I failed to reproduce my own results from a decade ago
categories:
- Open science
- Reproducibility
---

I recently received an email from my PhD advisor introducing me to a grad
student who was interested in using some experimental data I had collected a
decade ago to validate his simulations.
Even back then, I was pretty adamant about open sourcing everything about a
project, including code and data, so I was able to easily clone the
[repo](https://github.com/UNH-CORE/RVAT-Re-dep)
from GitHub.

In the README, I even had instructions for getting started:

![The README.](/images/repro-fail/readme.png)

Python 3.5 is quite old at this point,
and I use
[Mambaforge](https://conda-forge.org/download/)
instead of Anaconda,
but the ecosystems are compatible with each other,
so I figured I could give it a shot with my Mambaforge environment.
The `pip install` commands worked fine:

![Naively installing with pip.](/images/repro-fail/pip-install.png)

So I tried running `python plot.py` to generate the figures, but that actually
doesn't do anything without some additional options,
which was apparent from the help output printed to the terminal.
So I ran `python plot.py --all` to generate all of the figures,
and here was the result:

![The initial plot all call.](/images/repro-fail/plot-all-initial.png)

As we can see,
the interface to the `scipy.stats.t.interval` function had changed since the
version I was using back then.
This puts us at a crossroads.
We need to decide between:

1. Adapting the code for newer dependencies.
2. Attempting to reproduce the environment in which this ran initially.

I made option 2 hard for myself by not exporting the Conda environment
way back when.
That's a pretty significant oversight.

At this point
it's worth doing a little _product management_ and thinking about
what is actual point of doing all this.
I can think of two use cases:

1. Reproducing the results can help ensure there are no mistakes,
   or that the outputs (figures) genuinely reflect the inputs (data)
   and procedures (code). There is a chance that I updated the code at some
   point but never reran `plot.py`, so the figures are out-of-date.
   This is quite unlikely though. As a side note, this is a problem
   my project [Calkit](https://github.com/calkit/calkit) helps solve.
2. We want to produce a slight variant of one or more figures, adding
   the results from a simulation for comparison.

I would deem use case 2 more important than use case 1
since it involves carrying things forward rather than simply trying to
repeat the past.
But how does this inform which strategy to use?
Should we adapt the code or reproduce the old environment?
Is the new prospective user going to want to use the old environment to
create their figure variant?
Should they simply start from scratch and copy/paste whatever they need
from my code to write their own figure generation procedure?

If the old environment were easy to use for just this procedure,
that would probably be fine,
but if it continues to be iterated upon with more variants created,
at some point it will probably need to be modernized or even rewritten.

I decided to try both strategies on two different branches to see which
one was easier.

One of the figure types in question is fairly complex.
It plots out-of-plane mean velocity in a turbine wake as contours
and in-plane mean velocity as vector arrows,
and includes the projected area of the turbine.
It uses LaTeX for the axis labels, and is set to match the true aspect
ratio of the measurement plane.
These figures were not committed to the Git repo,
but I was able to find them in an executed version of the repo I had archived
to Google Drive.
Here's an example for reference:

![Reference figure.](/images/repro-fail/ref-figure.png)

As a side note, this figure should probably be using the viridis color map
instead of coolwarm, since in this case mean velocity is not really
a diverging quantity,
but that's a topic for another day.

Another one of the figures plotted quantities with error bars against
two different Reynolds numbers,
each with its own x-axis:

![Re dep figure.](/images/repro-fail/re-dep-figure.png)

I remember this being a pain to figure out,
and I've had questions from others on how to create similar figures
for their own data.
Does that warrant an abstraction?

## Attempting to reproduce the old environment

I left myself some non-machine-usable instructions for reproducing the old
environment: Install a version of Anaconda that uses Python 3.5
and `pip install` two additional packages.
Given that I already have `conda` installed,
I figured I could generate a new environment with Python 3.5
and take it from there.

![Attempting to create a Python 3.5 environment.](/images/repro-fail/mamba-create-py35.png)

No luck. Python 3.5 is not available in the `conda-forge` or `main`
channels any longer.

There are some old Anaconda Docker images up on Dockerhub.
Maybe I can use one of those.
The versions don't correspond to Python versions,
however,
so I had to search for the
[release notes](https://docs.anaconda.com/anaconda/release-notes)
to find which Anaconda version I wanted.
Anaconda 2.4.0, released on November 2, 2015,
was the first version to come with Python 3.5,
and that version is available on Dockerhub,
so I attempted to spin up an interactive container:

![Docker run Anaconda.](/images/repro-fail/docker-run.png)

To my surprise, this failed.
Apparently there was a change in image format at some point and these
images are no longer supported.

So let's see if we can run the newest Anaconda version with Python 3.5.
That would be Anaconda 4.2.0.
That image was in the correct format!

Attempting to install our two additional dependencies with `pip`
proved to be problematic, however,
with SSL verification errors,
and an inability to find the correct distribution.
Upgrading `pip` was not helpful,
since it installed a version incompatible with Python 3.5.

Looking up the latest version of `pip` compatible with Python 3.5
shows lots of
[recommendations](https://www.reddit.com/r/Python/comments/s0j7ao/which_pip_version_is_max_supported_to_be_useable/)
to upgrade to 3.6,
so maybe we'll just need to do that.
At this point, we're blending the two strategies here---attempting to find
an environment that works rather than reproducing the one that did back then.

`mamba create -n rvat-re-dep python=3.6` failed, so we can hunt for the
newest Anaconda verison with Python 3.6.
At this point we're at Anaconda 5.2.0, so let's
try to run that Docker container and do our `pip install`s in it.

Installing `progressbar33` went okay,
but `pip install pxl` caused an error with a missing graphics library
that Matplotlib depended on:

![Failed pxl install with Python 3.6.](/images/repro-fail/fail-pxl-install-py36-docker.png)

I then set the default Matplotlib backend with

```sh
export MPLBACKEND=Agg
```

and `pxl` was able to be installed.

At this point it's clear I am going to need to create my own Docker image
if I want to keep going down
this path,
which I'm not even sure I do at this point.

So I created a new Docker environment with its own build stage with Calkit:

```sh
calkit new docker-env \
    --name main \
    --image rvat-re-dep \
    --from continuumio/anaconda3:5.2.0 \
    --description "A custom Python 3.6 environment" \
    --stage build-docker
```

In this case, the `Dockerfile` doesn't yet have everything we need,
but it's a start.

We add these lines and we should be good to go:

```Dockerfile
ENV MPLBACKEND=Agg

RUN pip install --no-cache-dir progressbar33 pxl
```

Running our pipeline again with `calkit run` will automatically rebuild the
image after that,
then we can try

## Conclusions and final thoughts

Overall, I'd give myself a B- for reproducibility and reusability
here.
The data and code were made openly available and
cited in the relevant paper.
However, as a product, this repo is not really easy to reuse.
The CSVs of processed data are the core of the value,
and maybe the plotting code provides some value for copy/pasting,
but again, these require copying and pasting,
which doesn't necessarily leave breadcrumbs for further reuse.

Should we treat these bundles of data and code as products that require
maintenance?
Or should we simply hand them off to the world and move on?
Do we have some obligation to treat these as products and ensure they
deliver value to the users,
or is enough to simply provide all of the materials?

Perhaps this project as a whole can be treated as a starting point
for the user, and they can morph it to their own ends?
