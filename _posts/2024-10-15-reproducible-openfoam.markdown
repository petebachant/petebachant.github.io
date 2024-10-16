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
You'll also need:
- Python/Conda. I like to install [Miniforge](TODO), but there are a few
  options.
- Docker.

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

## Getting an important reference

We want to mesh the domain similarly to the one used for the DNS dataset in the
JHTDB.
First, we want to import the README from the JHTDB dataset as a reference
so we can see what the domain looks like.
As luck would have it, this reference already exists in another project,
so I can just run

```sh
calkit import reference \
    petebachant/boundary-layer-turbulence-modeling/references.bib:JHTDBDescription
```

and I will have the reference in a local `references.bib` file (BibTeX format)
as well as a PDF in the `references` folder.

## Starting our OpenFOAM case

We know we're going to want to run multiple different versions of a similar
case so we can test different turbulence models.
We should also probably do a quick mesh dependence study.
For this, I'm going to setup the case in a "templatized" way,
and create new cases to run as needed from a script.

I'm going to copy over some files from a case I had already created.
You'll notice the `blockMeshDict` is actually named `blockMeshDict.template`,
and it uses Python's string formatting syntax to parameterize certain values.
We're also going to templatize the `constant/turbulenceProperties` file,
so we can easily create new cases with different turbulence settings.

You'll also notice this is all managed through a `run.py` script,
but we haven't installed any of the necessary dependencies to run it.
In order to make these simulations reproducible, we're going to use
Docker.

## Creating a reproducible OpenFOAM environment with Docker

In order to run a Docker container on the local repo files,
I'll create a Calkit Docker environment and corresponding run script with:

```sh
calkit new docker-env \
    --name openfoam-2406-foampy \
    --create-stage build-docker \
    --path Dockerfile \
    --base microfluidica/openfoam:2406 \
    --add-module mambaforge \
    --add-module foampy \
    --workdir /sim \
    --create-run-script run-docker.sh
```

TODO: This should happen in the GUI?

This command will create the necessary Dockerfile,
the environment in our project metadata,
and will add a stage to our DVC pipeline to build the image.

If we run `calkit status`, we see TODO

So, we execute `calkit run`, and then `calkit save -m "Run pipeline"`.

TODO: On the GUI

## Creating a Conda environment for our Python scripts

We're going to plot some of the data with various Python packages,
so we need to ensure we have an environment in which to run those.

```sh
calkit new conda-env \
    --name blsim-python \
    --create-stage create-conda-env \
    --env-name blsim \
    --add-package python=3.12 \
    --add-package pandas \
    --add-package jupyter \
    --add-package notebook \
    --add-package matplotlib \
    --add-pip-package plotly
```

This will also create a DVC stage to ensure we create our Conda environment
if necessary when running the pipeline.

## Creating figures

We want to compare the OpenFOAM results to the DNS data,
for which we can plot the mean velocity profiles, for example.
Let's create a new figure TODO

```sh
calkit new figure \
    --title "Mean velocity profiles" \
    --path figures/mean-velocity-profiles.json \
    --create-stage plot-mean-velocity-profiles \
    --create-script \
    --cmd python scripts/plot-mean-velocity-profiles.py \
    --dep sim/... \ TODO
    --dep sim/... TODO
```

TODO: I can define a static path?

Now another call to `calkit run` and `calkit save -m "Run pipeline"`
will materialize this figure and push it to the repo.
This figure is now viewable as its own object up on the website,
on which we can make comments.
Since we made it with Plotly,
we can also zoom in, interact with the data, etc.

## What about manual steps?

Automation is great, and we should try to script everything if possible,
but what about things that we only know how to do manually.
In my case, I'm not all that great with scripting in ParaView,
but I know how to manually create a snapshot of the mesh,
so I'm going to do it that way, but I want it to be part of the pipeline so
it can be tracked, and I'll be forced to regenerate the image if the
mesh changes.

```sh
calkit new figure \
    --path figures/mesh-snapshot.png \
    --title "Mesh snapshot" \
    --stage save-mesh-snapshot \
    --create-stage \
    --manual-step "Save mesh image to figures/mesh-snapshot.png" \
    --cmd "paraview sim/cases/k-epsilon-ny-40/case.foam" \
    --dep sim/cases/k-epsilon-ny-40/constant/polyMesh
```

This command shows me a message telling me what to do, and will rerun
if the mesh changes.
Now let's execute `calkit run` again.
Note ParaView will need to be installed for this to run properly.

TODO: These dependencies should be listed in our repo somehow.
They could actually be manual steps.

But wait, what if we don't have ParaView installed?
We can add another manual step for installing ParaView.
Now, technically, we should point to a specific version,
or maybe even run it as a Docker container,
but we're aiming for reasonable reproducibility,
not necessarily perfection.
In this case, we will add the stage manually to the `dvc.yaml` file:

```yaml
stages:
  ensure-paraview-installed:
    cmd: >
      calkit check-call
      --message "Confirm ParaView is installed"
      --cmd "paraview --version > paraview-version.txt"
    outs:
      - paraview-version.txt:
          cache: false
    always_changed: true
...
```

Basically what this allows us to do is ensure any annoying manual setup steps
can be tracked, and rerun if need be.
We'll also record the version in the repo after installation with the
`--post-cmd` option.
This should help reduce some cognitive load, i.e.,
you only need to remember to run `calkit run` to get back to where you were.
We could do this with Docker too, but I'll leave that up to you.

TODO: Maybe this won't actually be rerun. Should this be a procedure?

## Tying it all together

So we have something of a report,
we are going to create a Jupyter notebook TODO

```sh
calkit new publication \
    --kind notebook \
    --path notebook.ipynb \
    --create-stage build-notebook \
    --title "Validating RANS models against DNS of a turbulent boundary layer"
```

TODO: Ensure nbstripout is installed for the repo with `nbstripout --status`?

## Our finished product

If we visit the Calkit website,
we can now view our new reproducible OpenFOAM project.
We can see the pipeline, questions we were hoping to answer,
relevant references and datasets,
figures we created, and the notebook that visualizes our results.

## Archiving and obtaining a DOI

Finally, we're going to archive all of the materials here and obtain a
digital object identifier (DOI) for this snapshot,
so others can cite it and refer back to this exact set of files.
