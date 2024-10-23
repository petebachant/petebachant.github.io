---
comments: true
date: 2024-10-15
layout: post
slug: reproducible-openfoam
title: Reproducible OpenFOAM simulations with Calkit
categories:
- Engineering
- Software
- Open science
- Reproducibility
---

Have you ever been here before?
You've done a bunch of work to get a simulation to run, created some figures,
and submitted a paper to a journal.
A month or two later you get the reviews back and you're asked by _Reviewer 2_
to make some minor modifications to a figure.
There's one small problem, however: You don't remember how that figure was
created,
or you've upgraded your laptop and now have different software installed,
and the script won't run.
Maybe you were able to clone the correct Git repo with the code,
but you don't
remember where the data is supposed to be stored after you download it
from Google Drive.
In other words, your project is not reproducible.

![Confused computer guy.](/images/repro-openfoam/confused.jpeg)

Here we are going to show how to make an OpenFOAM CFD project reproducible
using [Calkit](https://github.com/calkit/calkit),
a tool I've been working on that ties together and simplifies a
few lower-level tools to help with
reproducibility:
- Git
- GitHub
- DVC (Data Version Control)
- Docker
- Cloud storage

## Getting setup

You will need to have
[Git](https://git-scm.com/)
installed, and you'll need to have a
[GitHub](https://github.com) account.
You'll also need to have Python
([Mambaforge](https://conda-forge.org/miniforge/) recommended)
and [Docker](https://docker.com) installed.
After that, install the Calkit Python package with:

```sh
pip install calkit-python
```

![Installing with pip.](/images/repro-openfoam/pip-install.png)

## Creating and cloning the project

Head over to [calkit.io](https://calkit.io)
and log in with your GitHub account.
Click the button to create a new project.
Let's title ours "RANS boundary layer validation",
since for our example, we're going to create a project that attempts to
answer the question:

>What RANS model works best for a simple boundary layer?

We'll keep this private for now
(though in general it's good to work openly.)
Creating a project on Calkit also creates the project Git repo on GitHub.

![Creating a new Calkit project.](/images/repro-openfoam/create-project.png)

We can then add our question,
so we remember to stay on track 😀

![Calkit project questions list.](/images/repro-openfoam/questions.png)

We're going to need a token to use the Calkit cloud as a DVC remote,
so head over to your
[user settings](https://calkit.io/settings),
generate one for use with the API, and copy it to your clipboard.

Then we can set that token in our local Calkit config with:

```sh
calkit config set token {paste your token here}
```

Next, clone the repo to your local machine with (filling in your username):

```sh
calkit clone https://github.com/{your user name}/rans-boundary-layer-validation.git
```

Note you can modify the URL above to use SSH if that's how you interact with
GitHub.

## Getting some validation data

We want to validate these RANS models, so we'll need some data.
It just so happens that there is already a boundary layer
direct numerical simulation (DNS) dataset on
Calkit downloaded from the
[Johns Hopkins Turbulence Databases (JHTDB)](https://turbulence.pha.jhu.edu/),
so we can simply import that with (after `cd`ing into the project directory):

```sh
calkit import dataset \
    petebachant/boundary-layer-turbulence-modeling/data/jhtdb-transitional-bl/time-ave-profiles.h5 \
    data/jhtdb-profiles.h5
```

We can now see that as part of the project datasets on the Calkit web app.
We can also see the file is present, but ignored by Git,
since it's managed by DVC.

![Calkit project datasets page.](/images/repro-openfoam/datasets-page.png)

## Creating a reproducible OpenFOAM environment with Docker

If you've never heard of or worked with Docker,
it can sound a bit daunting,
but Calkit has some wrapper functionality to make it easy.
Basically, Docker is going to let us create isolated reproducible
environments in which to run software and Calkit will keep track of
which environments belong to this project.

Let's create an OpenFOAM-based Docker environment and build stage with:

```sh
calkit new docker-env \
    --name foam \
    --image openfoam-2406-foampy \
    --stage build-docker \
    --from microfluidica/openfoam:2406 \
    --add-layer mambaforge \
    --add-layer foampy \
    --description "OpenFOAM v2406 with foamPy."
```

This command will create the necessary Dockerfile,
the environment in our project metadata,
and will add a stage to our DVC pipeline to build the image before
running any other commands.

We can visualize the pipeline, i.e.,
all the things that run, as a directed acyclic graph (DAG)
using `dvc dag`.
The Calkit website will also visualize the DAG on the project's workflow
page.

Right now, we can see there's only one step, so let's add more.

If we run `calkit status`, we see TODO

So, we execute `calkit run`, and then `calkit save -m "Run pipeline"`. TODO

Let's check that we can run something in the environment.

```sh
calkit runenv -- blockMesh -help
```

## Adding the simulation runs to the pipeline

Alright, now that we have an environment setup,
we can start declaring what operations we want to run in our pipeline.
I've setup this project to use [foamPy](https://github.com/petebachant/foamPy)
to run a case with a "templatized" `turbulenceProperties` file via a script
`run.py`,
which we're going to run in our Docker environment.
We can see the help output of the script with:

```sh
calkit runenv -- python run.py -h
```

We want to run the simulation with a few different turbulence models:

- Laminar (no turbulence model)
- $k$–$\epsilon$
- $k$–$\omega$

To do this, we're going to create a "foreach" DVC stage to run our
script over a sequence of argument values.
If we set this up properly, DVC will be smart enough to cache the results
and not rerun simulations when they don't need to be rerun.

We can create this with:

```sh
calkit new foreach-stage \
    --cmd "calkit runenv python run.py --turbulence-model {var} -f" \
    --name run-sim \
    --dep system \
    --dep constant/transportProperties \
    --dep run.py \
    --dep Dockerfile-lock.json \
    --out "cases/{var}/postProcessing" \
    "laminar" "k-epsilon" "k-omega"
```

If you look at the `git log`, you'll notice that Calkit is making Git
commits for all of these actions.
This is considered a sane default that should help make things easier,
but it is possible to disable this with `--no-commit`.

We are defining an output for each simulation as the `postProcessing` folder,
which we will cache and push to the cloud for backup,
so others (including our future self),
can pull down the results and work with them without needing to rerun
the simulations.
We are also defining dependencies for the simulations.
What this means is that if anything in the `system` folder, the `run.py`
script, `constant/transportProperties`, or our Dockerfile changes,
DVC will know it needs to rerun the simulations.
Conversely, if those haven't changed and we already have results cached,
there's no need to rerun.

This is nice because we only need to remember one command and keep running it,
and that's simply

```sh
calkit run
```

TODO: Call out below.
Note: `calkit run` is a wrapper around `dvc repro` that parses some special
metadata to define certain special objects, e.g., datasets or publications.

TODO: Show our DAG now.

## Creating a figure to visualize our results

We want to compare the OpenFOAM results to the DNS data,
for which we can plot the mean velocity profiles, for example.
We can create a new figure with its own pipeline stage with:

```sh
calkit new figure \
    figures/mean-velocity-profiles.png \
    --title "Mean velocity profiles" \
    --description "Mean velocity profiles." \
    --stage plot-mean-velocity-profiles \
    --cmd "calkit runenv python scripts/plot-mean-velocity-profiles.py" \
    --dep scripts/plot-mean-velocity-profiles.py \
    --dep data/jhtdb-profiles.h5 \
    --deps-from-stage-outs run-sim
```

The last line there is going to automatically create dependencies based on
the outputs of our `run-sim` stage,
saving us the trouble of typing out all
of our turbulence model names.

Now another call to `calkit run` and `calkit save -m "Run pipeline"`
will materialize this figure and push it to the repo.
This figure is now viewable as its own object up on the website,
on which we can make comments.

## Creating a slight variation to the figure with a fresh copy

Now let's show the value of having our project in a reproducible state,
addressing the problem we laid out in the introduction.
We're going to pretend we were forced to start from scratch,
so we'll clone a fresh copy of the repo
and attempt to simply change one of the axis labels slightly.

So we move back up a directory and clone the repo again with:

```sh
calkit clone https://github.com/{your user name}/rans-boundary-layer-validation.git
```

Moving in there,
you'll notice the `postProcessing` directories exist,
and so does our figure PNG file,
both of which would not exist yet if we had simply used `git clone`.

Next can edit our plotting script to make the relevant changes.
Then we execute `calkit run`.
Notice how the simulations were not rerun thanks to the DVC cache.
If we run `calkit status` we see there are some differences,
so we run `calkit save -m "Change x-axis label for reviewer 2"`.
This creates a Git commit and pushes any relevant cached artifacts to the
cloud.
If we go visit the project on the Calkit website, we see our figure is
up-to-date.

## Conclusions and next steps

We've built a project that runs OpenFOAM simulations reproducibly,
creates some figures, and ensures these are kept in version control
and backed up to the cloud.
Maybe next we'd like to create a publication from those figures,
but that will need to be the subject of a future post.
Guess what? You can also put a LaTeX build stage into the pipeline.

We could add a mesh dependence stage before the TODO.

OpenFOAM could be replaced with any other software that can be run with
Docker, more dependencies could be added, etc.

Do you use a different system to manage pipelines, data, artifacts?
If so, let me know in the comments.

TODO: Make it so users can create a new project starting from this one.
