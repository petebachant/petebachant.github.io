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

There was a bit of a problem, however.
The Anaconda Python distribution link brings us to anaconda.com
rather than continuum.io,
which is now a commercial download, and will obviously not include Python 3.5,
as was recommended in the README.
These days I mostly use the
[Mambaforge](https://conda-forge.org/download/)
distribution.
