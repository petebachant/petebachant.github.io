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
Even back then, I was pretty adamant about open-sourcing my research
projects, including code and data, so I was able to easily clone the
[repo](https://github.com/UNH-CORE/RVAT-Re-dep)
from GitHub.

In the README, I even had instructions for getting started:

![The README.](/images/repro-fail/readme.png)

Python 3.5 is quite old at this point,
and these days I use
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
channels any longer,
at least not for my MacBook's ARM processor.

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
then we can try to run our script in the environment with:

```sh
calkit runenv python plot.py --all --save
```

The script encountered an error,
but we now have some files saved in our Figures directory,
which is a great start!

If we look at our contour--quiver plot from above, we see it was mostly
reproduced, but the LaTeX labels are not using the same font:

![Contour/quiver plot from first Docker run.](/images/repro-fail/ref-figure-docker.png)

This is probably because our Docker image does not include a LaTeX distribution
like I did when I first ran it.
I attempted to modify the Docker image to install `texlive`,
but this did not produce the same exact figure.
However, I decided this was good enough for now.

I did at least add one figure generation stage to the DVC pipeline to show
how I'd probably approach this as a full Calkit project.
The full pipeline (in `dvc.yaml`) looks like:

```yaml
stages:
  build-docker:
    cmd: calkit build-docker rvat-re-dep -i Dockerfile --platform linux/amd64
    deps:
      - Dockerfile
    outs:
      - Dockerfile-lock.json:
          cache: false
          persist: true
    always_changed: true
  plot-perf-re-dep:
    cmd: calkit runenv -n main python plot.py perf_re_dep --save --no-show
    deps:
      - plot.py
      - pyrvatrd/plotting.py
      - Data/Processed
      - Dockerfile-lock.json
    outs:
      - Figures/perf_re_dep.pdf
    meta:
      calkit:
        type: figure
        title: Turbine performance Reynolds number dependence
        description: >
          Power and drag (or thrust) curves as a function of Reynolds number,
          computed with both the turbine diameter and blade chord length.
```

## But how should this code and data actually be reused?

I actually used this dataset in a later paper validating some CFD simulations,
the repo for which is
[also on GitHub](https://github.com/petebachant/CFT-wake-modeling-paper).
My approach there was to write a single script
`makefigs.py` to make all of the figures for the paper, except for the
ones that needed to be created manually, e.g., ones that came from
CAD drawings.

Peering into the script we can see right away that there's no hope that it's
reproducible:

```python
cfd_sst_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-3d/mesh14"
cfd_sa_dir = "/media/Data2/OpenFOAM/pete-2.3.x/run/unh-rvat-3d/mesh14-sa"
cfd_sst_2d_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-2d/kOmegaSST"
cfd_sa_2d_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-2d/SpalartAllmaras"
exp_dir = "/home/pete/Google Drive/Research/Experiments/RVAT Re dep"
paper_dir = "/home/pete/Google Drive/Research/Papers/CFT wake modeling"
cfd_dirs = {"3-D": {"kOmegaSST": cfd_sst_dir,
                    "SpalartAllmaras": cfd_sa_dir},
            "2-D": {"kOmegaSST": cfd_sst_2d_dir,
                    "SpalartAllmaras": cfd_sa_2d_dir}}


# Append directories to path so we can import their respective packages
for d in [cfd_sst_dir, cfd_sa_dir, cfd_sst_2d_dir, cfd_sa_2d_dir, exp_dir]:
    if not d in sys.path:
        sys.path.append(d)
```

This script depends a lot on the state of the machine on which it was run,
and even references paths on different hard drives.

If we look at the bottom of the script, we can see each figure that would
be generated if it were possible to run this now:

```python
    if "exp_perf" in args.plots or args.all:
        plot_exp_perf(save=save)
    if "meancontquiv" in args.plots or args.all:
        plot_exp_meancontquiv(save=save)
        plot_cfd_meancontquiv("kOmegaSST", save=save)
        plot_cfd_meancontquiv("SpalartAllmaras", save=save)
    if "verification" in args.plots or args.all:
        plot_verification(save=save)
    if "profiles" in args.plots or args.all:
        plot_profiles(save=save)
    if "perf_bar_charts" in args.plots or args.all:
        make_perf_bar_charts(save=save)
    if "recovery" in args.plots or args.all:
        make_recovery_bar_chart(save=save)
    if "kcont" in args.plots or args.all:
        plot_exp_kcont(save=save)
        plot_cfd_kcont("kOmegaSST", save=save)
        plot_cfd_kcont("SpalartAllmaras", save=save)
```

The `plot_exp_perf` function is quite portable.
It simply loads in a CSV and plots it with Matplotlib:

```python
def load_exp_perf_data():
    """Loads section of exp perf data for U_infty=1.0 m/s."""
    return pd.read_csv(os.path.join(exp_dir, "Data", "Processed",
                                    "Perf-1.0.csv"))


def plot_exp_perf(save=False):
    df = load_exp_perf_data()
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7.5, 3))
    ax[0].plot(df.mean_tsr, df.mean_cp, "-o")
    ax[0].set_ylabel(r"$C_P$")
    ax[1].plot(df.mean_tsr, df.mean_cd, "-o")
    ax[1].set_ylabel(r"$C_D$")
    for a in ax:
        a.set_xlabel(r"$\lambda$")
    fig.tight_layout()
    if save:
        fig.savefig("figures/exp_perf" + savetype)
```

However, this could be improved
by adding the experiment repo as a Git submodule so
`exp_dir` could be a relative path.

`plot_exp_meancontquiv` is a bit different.
This function actually uses a Python package in the experiment repo
called `pyrvatrd` to reuse the plotting logic inside:

```python
def plot_exp_meancontquiv(save=False):
    os.chdir(exp_dir)
    pyrvatrd.plotting.plot_meancontquiv(1.0)
    os.chdir(paper_dir)
    if save:
        plt.savefig("figures/meancontquiv_exp" + savetype)
```

Again, this would be better if it referenced a submodule at a relative path.

`plot_cfd_meancontquiv` does something similar,
except each CFD simulation has its own Python package with an identical
structure such that the function could be called:

```python
def plot_cfd_meancontquiv(case="kOmegaSST", save=False):
    """Plots wake mean velocity contours/quivers from 3-D CFD case."""
    os.chdir(cfd_dirs["3-D"][case])
    cfd_packages["3-D"][case].plotting.plot_meancontquiv()
    os.chdir(paper_dir)
    if save:
         plt.savefig("figures/meancontquiv_" + case + savetype)
```

This might be an overzealous use of the "don't repeat yourself" (DRY)
principle,
though the plotting function was technically repeated in both the experiment
and CFD repos, i.e., a change would need to be made in both if desired.

## What about usability?

Beyond not being reproducible,
this data and code was largely non-usable.
So we should put on our product manager hat and think about
what users would want to do with this stuff.
We can use so-called "user stories" to do this.
For example:

1. As a researcher, I want to read mean wake velocity data so I can plot it
   against my simulation results.

These were not possible in the original state of the repo,
so let's go ahead and change that.
We're going to create a basic API.

It was also not possible to use the data outside of the repo,
since the paths were hard-coded assuming we would be running at the top
of the repo as our working directory.

## How I would reuse this code and data now

Over the years I have shifted my opinion on DRY,
and realized it can cause some seriously bad architectures and designs.
If I had to reuse the materials from this experiment these days,
I would start a new project from scratch and start copy/pasting things in
as needed.

1. Created a repo on GitHub.
2. Imported the project on calkit.io.
3. Cloned to my local machine with the Calkit local server running.
1. Clicked "open with VS Code" from the Calkit local machine page.
1. Ran `dvc init`.
1. Ran `calkit config setup-remote`.
1. Committed changes and ran `calkit push`.
1. Manually copied and pasted the processed data CSVs from the experiment into
   my project directory.
1. Added the dataset to `calkit.yaml`, so we know where it came from.
   These last two steps would be nice with a `calkit import dataset` call,
   but that experiment would need to be made into a Calkit project,
   which I haven't done yet.
1. Ran
    ```sh
    calkit new conda-env \
        python \
        pip \
        matplotlib \
        pandas \
        jupyter \
        --pip pxl \
        -n reuse-rvat-re-dep \
        --stage check-conda-env
    ```
1. Ran the pipeline with `calkit run`, which created the environment and a lock
   file.
1. Copied the `pyrvatrd` package into my project directory and added to
   `calkit.yaml` so we can know what it was derived from.
1. Started a notebook called `notebook.ipynb` and copy/pasted a function from
   the experiment repo into it to see if I could replicate the mean velocity
   contour/quiver plot.
1. Did a whole bunch to get that script to run in a new environment.
   See the commits in the repo.
1. Added a pipeline stage to generate the mean contour/quiver plots at all
   velocities.
1. Added figures to `calkit.yaml` for each of these.
1. Ran the pipeline, committed and pushed everything to the cloud.

## Improving the reusability of this experimental data

I created a new project assuming I was going to try to reuse the
RVAT-Re-dep data to validate a simulation.

Make this a RVAT-Re-dep an installable Python package:

```sh
calkit new python-package unh_rvat_re_dep
```

This creates a `pyproject.toml` file and adds the package to the
`software.packages` section in `calkit.yaml`.




## Conclusions and final thoughts

Reproducibility is not the same thing as reusability.
Each serves a different purpose.
Reproducibility is ensuring correctness in the present,
and reusability is ensuring value for the future.
Both are important.

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
