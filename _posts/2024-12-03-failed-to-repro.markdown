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
projects, including code and data,
so it figured it would be pretty simple.

I was able to easily clone the
[repo](https://github.com/UNH-CORE/RVAT-Re-dep)
from GitHub since it's still up there.
In the README, I even had instructions for getting started and regenerating
the figures:

![The README.](/images/repro-fail/readme.png)

Python 3.5 is quite old at this point,
and these days I mostly use
[Mambaforge](https://conda-forge.org/download/)
instead of Anaconda,
but the ecosystems are largely compatible with each other,
so I figured I could give it a shot with my Mambaforge environment.
The `pip install` commands worked fine:

![Naively installing with pip.](/images/repro-fail/pip-install.png)

So I tried running `python plot.py` to generate the figures, but that actually
doesn't do anything without some additional options
(bad docs, me-from-the-past,)
which was apparent from the help output printed to the terminal.
So I ran `python plot.py --all` to generate all of the figures,
and here was the result:

![The initial plot all call.](/images/repro-fail/plot-all-initial.png)

As we can see,
I failed to reproduce the figures because
the interface to the `scipy.stats.t.interval` function had changed since the
version I was using back then.
This puts us at a crossroads if we're truly going to try to reproduce
these results.
There are two options:

1. Attempt to reproduce the environment in which this ran initially.
1. Adapt the code for newer dependencies.

I made option 1 hard for myself by not exporting the full Conda environment
way back when, i.e.,
"Anaconda using Python 3.5" is not a full description of the environment.
That's a pretty significant oversight.

But let's take another step back and question why we want to do this at all.
What is the point of trying to reproduce these figures?
I can think of two use cases:

1. Reproducing the results can help ensure there are no mistakes,
   or that the outputs (figures) genuinely reflect the inputs (data)
   and procedures (code). There is a chance that I updated the code at some
   point but never reran `plot.py`, so the figures are out-of-date.
   This is quite unlikely though. I remember running this script many times
   after processing the data to get the figures just right.
1. We want to produce a slight variant of one or more figures, adding
   the results from a simulation for the purposed of validation.

We can call these reproducibility and _reusability_, respectively.
These map fairly well to the strategies above as well.
Both are important, but at this point I would prioritize reusability,
where the data can be used to created new knowledge instead of simply
repeating the past.
However, I wanted to see what it would take to achieve both.

## Attempting to reproduce the old environment

Before we start, let's pick a figure from the original paper to focus
on reproducing.
For this I chose one that's relatively complex.
It plots out-of-plane mean velocity in a turbine wake as contours
and in-plane mean velocity as vector arrows,
and includes an outline of the turbine's projected area.
It uses LaTeX for the axis labels, and is set to match the true aspect
ratio of the measurement plane.
These figures were not committed to the Git repo,
but I was able to find them in an executed version of the repo I had archived
to Google Drive in grad school.
Here's an example for reference:

![Reference figure.](/images/repro-fail/ref-figure.png)

As a side note, this figure should probably be using the viridis color map
instead of coolwarm, since in this case mean velocity is not really
a diverging quantity,
but that's a topic for another day.

### Onto the tactical stuff

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

There are some old Anaconda Docker images up on Docker Hub,
so I thought maybe I could use one of those.
The versions don't correspond to Python versions,
however,
so I had to search though the
[release notes](https://docs.anaconda.com/anaconda/release-notes)
to find which Anaconda version I wanted.
Anaconda 2.4.0, released on November 2, 2015,
was the first version to come with Python 3.5,
and that version is available on Docker Hub,
so I attempted to spin up an interactive container:

![Docker run Anaconda.](/images/repro-fail/docker-run.png)

To my surprise, this failed.
Apparently there was a change in Docker image format at some point and these
types are no longer supported.
So I searched for the newest Anaconda version with Python 3.5,
which was Anaconda 4.2.0,
and luckily the image was in the correct format.

At this point I needed to create a new image derived from that one that
installed the additional dependencies with `pip`.
So I created a new Docker environment and added a build stage to the pipeline
with Calkit (a tool I've been developing more recently based on what I wish
I had back then):

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

Simply adding the instructions from the README resulted in
SSL verification and dependency resolution errors.
After some Googling and trial-and-error,
I was able to get things installed in this image with this command:

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

I then added figure generation stages to the DVC pipeline to show
how I'd probably approach this as a full Calkit project, so that
each output could be cached separately.
The pipeline (in `dvc.yaml`) then looked like:

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
  plot-mean-cont-quiv:
    cmd: calkit runenv -n main python plot.py all_meancontquiv --save --no-show
    deps:
      - plot.py
      - pyrvatrd/plotting.py
      - pyrvatrd/processing.py
      - Data/Processed
      - Dockerfile-lock.json
    outs:
      - Figures/meancontquiv_04.pdf
      - Figures/meancontquiv_06.pdf
      - Figures/meancontquiv_08.pdf
      - Figures/meancontquiv_10.pdf
      - Figures/meancontquiv_12.pdf
  # More stages here...
```

After a call to `calkit run`,
we can take a look at the reference figure:

![Reference figure generated with Python 3.5](/images/repro-fail/ref-figure-docker-py35.png)

And we got very close!
If you look very closely you'll notice the font for the tick labels
is slightly different from the figure at the top of the page,
since I had installed some font on my machine back then that
isn't present in this Docker image.
We could go down a rabbit hole trying to install the fonts into this image,
but I'm going to call this a win for now.

## What about reusability?

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

But again, let's take a step back and ask the question:
what is the real value of this project?

1. It provides a dataset against which numerical models can be validated in
   order to help improve them for simulating these types of turbines.
1. Some of the plotting procedures may be of interest, especially if the
   prospective numerical modeler wanted to generate similar figures from
   their simulation results.
1. The main question of the work was to address at what scale a physical
   model test needed to be to fairly approximate full-scale performance.

What then are the products corresponding to this value?

Most of the value in the dataset is in CSV files containing statistics of
each of the tow tank runs during the experiment.
With only those, many different plots can be made.

The plotting procedures are fairly tightly coupled to the structure of the
dataset, so they are not usable in their current form.

The third point of value can simply be done as a hand calculation,
which is nice.

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
4. Clicked "open with VS Code" from the Calkit local machine page.
5. Ran `dvc init`.
6. Ran `calkit config setup-remote`.
7. Committed changes and ran `calkit push`.
8. Manually copied and pasted the processed data CSVs from the experiment into
   my project directory.
9. Added the dataset to `calkit.yaml`, so we know where it came from.
   These last two steps would be nice with a `calkit import dataset` call,
   but that experiment would need to be made into a Calkit project,
   which I haven't done yet.
10. Ran
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
11. Ran the pipeline with `calkit run`, which created the environment and a lock
    file.
12. Copied the `pyrvatrd` package into my project directory and added to
    `calkit.yaml` so we can know what it was derived from.
13. Started a notebook called `notebook.ipynb` and copy/pasted a function from
    the experiment repo into it to see if I could replicate the mean velocity
    contour/quiver plot.
14. Did a whole bunch to get that script to run in a new environment.
    See the commits in the repo.
15. Added a pipeline stage to generate the mean contour/quiver plots at all
    velocities.
16. Added figures to `calkit.yaml` for each of these.
17. Ran the pipeline, committed and pushed everything to the cloud.

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

Technology marches onwards.
We probably can't expect unlimited computational reproducibility
on any hardware.
Just like I can't simply run a punch card program on my laptop,
some code will just not last forever.
Technologies like Docker can help us a lot here,
but we need to be realistic.

On the other hand,
reproducibility is not the same thing as reusability.
Each serves a different purpose.
Reproducibility is ensuring correctness in the present,
and reusability is ensuring value for the future.
Both are important.

If we want the products of research to be usable far into the future
we need to focus on keeping them as simple as possible,
and we might need to do some maintenance to them over time.

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
