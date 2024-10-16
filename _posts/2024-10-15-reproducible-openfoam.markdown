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

## Background

Have you ever been here before?
You've done a bunch of work to get a simulation to run, created some figures,
and submitted a paper to a journal.
A month or two later you get the reviews back and you're asked to, e.g.,
make some modifications to make a figure more readable.
There's one small problem, however: You don't remember how that figure was
created,
or you've upgraded your laptop and now have different software installed,
and the script won't run.
In other words, you can't reproduce that figure.

TODO: Relate that more to an OpenFOAM simulation.

I've been there too.
A particularly painful experience is when you run many different simulations,
deleting results after creating figures to save disk space,
and now have to run them all over again.

Now, using Git can be super helpful here.
You can keep your scripts in version control,
but what about your data or results that don't play well with Git because
they're either large (GitHub rejects files larger than 100 MB)
or not text?
You could use Git Large File Storage (LFS),
but that can be a bit overkill and expensive for files that don't
change much.
What about a tool to define and run a pipeline that generates all necessary
artifacts so you can just keep running one command over and over again,
without needing to remember which script does what?

In comes DVC (Data Version Control) to the rescue.
I found out about DVC a few months back and really liked the design.
It has a way to version data (of course) and a neat YAML-based pipeline
definition system.
In fact, I liked it so much, that I built [Calkit](https://calkit.io),
which is sort of like a glue layer between Git, DVC, GitHub, and cloud storage,
to try to make it super simple to work reproducibly.
Think "easy mode" for all those tools, putting everything in one place.

Now I'm going to walk through setting up a research project that will use
OpenFOAM.
We're going to try to answer the question:

>Which RANS model works best for a simple turbulent boundary layer?

## Getting setup

You will need to have Git installed, and you'll need to have a
[GitHub](https://github.com) account.
You'll also need to have Python and Docker installed.

After that, you can install the Calkit Python package with

```sh
pip install calkit-python
```

This will install DVC as well.

## Creating the project

Head over to https://calkit.io and log in with your GitHub account.
Click the button to create a new project.
Let's title ours "RANS boundary layer validation".
We'll keep this private for now,
though in general you shouldn't be scared to work openly.
Creating a project on Calkit also creates the project Git repo on GitHub.

Next, clone the repo to your local machine with the Git CLI, GitHub CLI,
or GitHub desktop app.

## Getting some validation data

We want to validate these RANS models, so we'll need some data.
Up on the Calkit website there is a page for browsing public datasets.
It just so happens that there is already a boundary layer
direct numerical simulation (DNS) dataset on
Calkit downloaded from the
[Johns Hopkins Turbulence Databases (JHTDB)](https://turbulence.pha.jhu.edu/),
so we can simply import that with

```sh
calkit import dataset \
    petebachant/boundary-layer-turbulence-modeling/data/jhtdb-transitional-bl/time-ave-profiles.h5 \
    data/jhtdb-profiles.h5
```

We're going to import it to a different location here.
Under the hood, Calkit used DVC to import the dataset from the Calkit Cloud,
adding metadata to the `datasets` section of `calkit.yaml`.
We can now see that as part of the project datasets on the Calkit web app.

TODO: Add image of dataset on the website.

## Creating a reproducible OpenFOAM environment with Docker

In order to run a Docker container on the local repo files,
I'll create a Calkit Docker environment and corresponding run script with:

TODO: Below should be able to run without building an image

```sh
calkit new docker-env \
    --name openfoam \
    --image-name openfoam-2406-foampy \
    --create-stage build-docker \
    --path Dockerfile \
    --from microfluidica/openfoam:2406 \
    --add-layer mambaforge \
    --add-layer foampy \
    --description "OpenFOAM v2406 with foamPy." \
    --wdir /sim
```

TODO: This should happen in the GUI?

This command will create the necessary Dockerfile,
the environment in our project metadata,
and will add a stage to our DVC pipeline to build the image.

`dvc.yaml` will now look like:

```yaml
stages:
  build-docker:
    cmd: >
      docker build -t openfoam-2406-foampy . &&
      docker inspect --format '{{.Id}}' openfoam-2406-foampy > Dockerfile.digest
    deps:
      - Dockerfile
    outs:
      - Dockerfile.digest:
          cache: false
```

If we run `calkit status`, we see TODO

So, we execute `calkit run`, and then `calkit save -m "Run pipeline"`.

TODO: On the GUI

Metadata about this environment has also been saved to `calkit.yaml`:

```yaml
environments:
  openfoam:
    kind: docker
    image: openfoam-2406-foampy
    path: Dockerfile
    stage: build-docker
    description: OpenFOAM v2406 with foamPy.
    layers:
      - mambaforge
      - foampy
    wdir: /sim  # TODO: Necessary?
```

Let's check that we can run something in the environment.

```sh
calkit run-env blockMesh -help
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
calkit run-env python run.py -h
```

Note that we don't need to specify the environment in which to run the command
since there's only one in the project, but if there are multiple,
Calkit will complain.

We want to run the simulation with a few different turbulence models:

- Laminar (no turbulence model)
- $k$–$\epsilon$
- $k$–$\omega$

To do this, we're going to create a DVC "foreach" stage to run our
script over a list of argument values.
If we set this up properly, DVC will be smart enough to cache the results
and not rerun simulations when they don't need to be rerun.

## Creating a figure to visualize our results

We want to compare the OpenFOAM results to the DNS data,
for which we can plot the mean velocity profiles, for example.
Let's create a new figure TODO

```sh
calkit new figure \
    --title "Mean velocity profiles" \
    --path figures/mean-velocity-profiles.png \
    --create-stage plot-mean-velocity-profiles \
    --cmd "calkit run-env python scripts/plot-mean-velocity-profiles.py" \
    --dep scripts/plot-mean-velocity-profiles.py \
    --dep data/jhtdb-profiles.h5 \
    --dep cases/... \ TODO
    --dep cases/... TODO
```

TODO: I can define a static path?

Now another call to `calkit run` and `calkit save -m "Run pipeline"`
will materialize this figure and push it to the repo.
This figure is now viewable as its own object up on the website,
on which we can make comments.
Since we made it with Plotly,
we can also zoom in, interact with the data, etc.

## Creating a slight variation to the figure with a fresh copy

Now let's show the value of having our project exist in reproducible form,
addressing the problem we laid out in the introduction.
We're going to delete our local copy of the repo,
clone a fresh copy,
and attempt to simply change one of the axis labels slightly.

TODO: Ensure this works if we delete the docker image, i.e., that is gets
rebuilt.

First we edit our plotting script to make the relevant changes.
Then we execute `calkit run`.
Notice how the simulations were not rerun thanks to the DVC cache.
If we run `calkit status` we see there are some differences,
so we run `calkit save -m "Change x axis label"`.
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
