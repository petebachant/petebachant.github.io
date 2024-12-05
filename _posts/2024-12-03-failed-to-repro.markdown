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
we can take a look at the newly-created figure (with the published one below):

![Reference figure generated with Python 3.5](/images/repro-fail/ref-figure-docker-py35.png)

![Reference figure.](/images/repro-fail/ref-figure.png)

And we got pretty darn close!
If you look a keen eye you'll notice the font for the tick labels
is slightly different from the figure at the top of the page,
since I believe I had installed the Arial font on my machine back then,
which isn't present by default in this Docker image since it is a
Microsoft font.
We could go down a rabbit hole trying to install the fonts into this image,
but I'm going to call this a win for now.

## But what about reusability?

I actually used this dataset in a later paper validating some CFD simulations,
the repo for which is
[also on GitHub](https://github.com/petebachant/CFT-wake-modeling-paper).
My approach back then was to write a single script
`makefigs.py` to make all of the figures for the paper.
Note how this is totally different from the command used to generate the
figures for the other paper,
which is not great,
and why something like `make` became the default in other contexts.

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
Each of these subproject repos had its own Python package, so
I added all of their locations to the Python path so they could be imported,
and later on, if I wanted to call any of the functions within,
I had to change the working directory to the subproject directory,
since these loaded data from relative paths.
Strangely enough I only added one of the relevant subproject repos
as a submodule to the paper repo.

So these repos were reusable insofar as I could regenerate the figures
from them in a new directory for the paper,
though it took a very complex setup to do so.

If we take a look at one of the functions that plotted results from experiment
and 4 different CFD setups, we can see how each subproject was used
to create something new:

```python
def plot_profiles(save=False):
    """Plot streamwise velocity and TKE profiles for all cases."""
    fig, ax = plt.subplots(1, 2, figsize=(7.5, 3))
    # Load data from 2-D SST case
    os.chdir(cfd_dirs["2-D"]["kOmegaSST"])
    df = pyurof2dsst.processing.load_u_profile()
    ax[0].plot(df.y_R, df.u, "-", label="SST (2-D)")
    df = pyurof2dsst.processing.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "-", label="SST (2-D)")
    # Load data from 2-D SA case
    os.chdir(cfd_dirs["2-D"]["SpalartAllmaras"])
    df = pyurof2dsa.processing.load_u_profile()
    ax[0].plot(df.y_R, df.u, "-.", label="SA (2-D)")
    df = pyurof2dsa.processing.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "-.", label="SA (2-D)")
    # Load data from 3-D SST case
    os.chdir(cfd_dirs["3-D"]["kOmegaSST"])
    df = pyurof3dsst.processing.load_u_profile()
    ax[0].plot(df.y_R, df.u, "--", label="SST (3-D)")
    df = pyurof3dsst.processing.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "--", label="SST (3-D)")
    # Load data from 3-D SA case
    os.chdir(cfd_dirs["3-D"]["SpalartAllmaras"])
    df = pyurof3dsa.processing.load_u_profile()
    ax[0].plot(df.y_R, df.u, ":", label="SA (3-D)")
    df = pyurof3dsa.processing.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, ":", label="SA (3-D)")
    # Load data from experiment
    df = load_exp_data()
    df = df[df.z_H == 0]
    ax[0].plot(df.y_R, df.mean_u, "o", label="Exp.", markerfacecolor="none")
    ax[1].plot(df.y_R, df.k, "o", label="Exp.", markerfacecolor="none")
    # Set legend and labels
    ax[1].legend(loc="best")
    for a in ax: a.set_xlabel("$y/R$")
    ax[0].set_ylabel(r"$U/U_\infty$")
    ax[1].set_ylabel(r"$k/U_\infty^2$")
    plt.tight_layout()
    # Move back into this directory
    os.chdir(paper_dir)
    if save:
        fig.savefig("figures/profiles" + savetype)
```

That code produced this figure:

![Profiles from CFD.](/images/repro-fail/cfd-profiles.png)

And for reference, `load_exp_data` simply called `pandas.read_csv` on one
of the original experiment's processed data files.

I think this leads us to one slightly unrelated principle:
keep everything in the same folder.
Use Git submodules if you have to,
but try not to have dependencies too far away from what you're
trying to achieve.
A related concept is the "monorepo."

Extract anything generally useful into its own package?

Provide a package with a clear API for working with your data,
but realize other languages might want to use it,
so keep it simple with file formats like CSV.

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
