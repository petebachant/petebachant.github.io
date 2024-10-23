---
comments: true
date: 2024-10-23
layout: post
slug: reproducible-openfoam
title: Reproducible OpenFOAM simulations with Calkit
categories:
- Engineering
- Software
- Open science
- Reproducibility
- OpenFOAM
- CFD
---

Have you ever been here before?
You've done a bunch of work to get a simulation to run, created some figures,
and submitted a paper to a journal.
A month or two later you get the reviews back and you're asked by _Reviewer 2_
to make some minor modifications to a figure.
There's one small problem, however:
You don't remember how that figure was created,
or you've upgraded your laptop and now have different software installed,
and the script won't run.
Maybe you were able to clone the correct Git repo with the code,
but you don't remember where the data is supposed to be stored.
In other words, your project is not reproducible.

![Confused computer guy.](/images/repro-openfoam/confused.jpeg)

Here we are going to show how to make a research project
that uses OpenFOAM reproducible
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

## Creating and cloning the project repo

Head over to [calkit.io](https://calkit.io)
and log in with your GitHub account.
Click the button to create a new project.
Let's title ours "RANS boundary layer validation",
since for our example, we're going to create a project that attempts to
answer the question:

>What RANS model works best for a simple boundary layer?

We'll keep this private for now
(though in general it's good to work openly.)
Note that creating a project on Calkit also creates the project
Git repo on GitHub.

![Creating a new Calkit project.](/images/repro-openfoam/create-project.png)

We can then add our question,
so we remember to stay on track 😀

![Calkit project questions list.](/images/repro-openfoam/questions.png)

We're going to need a token to interact with the Calkit API,
so head over to your
[user settings](https://calkit.io/settings),
generate one for use with the API, and copy it to your clipboard.

![Creating a new token.](/images/repro-openfoam/new-token.png)

Then we can set that token in our local Calkit config with:

```sh
calkit config set token YOUR_TOKEN_HERE
```

Next, clone the repo to your local machine with (filling in your username):

```sh
calkit clone https://github.com/YOUR_USERNAME/rans-boundary-layer-validation.git
```

Note you can modify the URL above to use SSH if that's how you interact with
GitHub.

![Cloning the repo.](/images/repro-openfoam/clone.png)

`calkit clone` is a simple wrapper around `git clone` that sets up the
necessary configuration to use the Calkit Cloud as a DVC remote,
the place where we're going to push our data,
while our code goes to GitHub.

## Getting some validation data

We want to validate these RANS models, so we'll need some data for comparison.
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

If we run `calkit status` we can see that there is one commit that has been
made but not pushed to `origin/main` (on GitHub), so we can
make sure everything is backed up there with `calkit push`.

![Status after importing dataset](/images/repro-openfoam/status-after-import-dataset.png)

`calkit status` and `calkit push` behave very similarly to `git status`
and `git push`. In fact, those commands are run alongside some additional
DVC commands, the importance of which we will see shortly.

We can now see our imported dataset as part of the project datasets on the
Calkit website.
We can also see the file is present, but ignored by Git,
since it's managed by DVC.
Because the dataset was imported, it does not take up any of this project's
storage space, but will be present when the repo is cloned.

![Calkit project datasets page.](/images/repro-openfoam/datasets-page.png)

## Creating a reproducible OpenFOAM environment with Docker

If you've never heard of or worked with Docker,
it can sound a bit daunting,
but Calkit has some tooling to make it a little simpler.
Basically, Docker is going to let us create isolated reproducible
environments in which to run software and will keep track of
which environments belong to this project in the `calkit.yaml` file.

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

If we run `calkit status` again,
we see that there's another commit to be pushed to GitHub,
and our pipeline is showing some changed dependencies and outputs.

![Status after creating Docker environment.](/images/repro-openfoam/status-after-create-docker-env.png)

This is a signal that it is out-of-date,
and should be executed with `calkit run`.
When we do that we see some output from Docker as an image is
built, and `calkit status` then shows we have a new `dvc.lock` file
staged and an untracked `Dockerfile-lock.json` file.

![Status after first Calkit run.](/images/repro-openfoam/status-after-run-docker-build.png)

We'll need to add that `Dockerfile-lock.json` file to our repo and then
commit and push. We can do this with the `calkit save` command:

```sh
calkit save dvc.lock Dockerfile-lock.json -m "Run pipeline to build Docker image"
```

which does the `add`, `commit`, `push` steps all in one,
deciding which files to store in DVC versus Git, and pushing to the respective
locations to save time and mental overhead.
However, if desired, you can of course run those individually for full control.

![Saving after building the Docker image.](/images/repro-openfoam/save-after-docker-build.png)

Finally, let's check that we can run something in the environment, e.g.,
print the help output of `blockMesh`:

```sh
calkit runenv -- blockMesh -help
```

This is great. We didn't need to install OpenFOAM, and neither will our
collaborators.
We're now ready to start setting up the cases.

## Adding the simulation runs to the pipeline

We can run things interactively and make sure things work,
but it's not a good idea to rely on interactive or ad hoc processes
to produce something permanent.
Any time you get to a point where you do want to save something permanent,
that should be created by the pipeline,
so let's add some simulation runs to ours.

We want to run the simulation to validate a few different turbulence models:

- Laminar (no turbulence model)
- $k$–$\epsilon$
- $k$–$\omega$

I've setup this project to use [foamPy](https://github.com/petebachant/foamPy)
to create and run variants of a case with a "templatized"
`turbulenceProperties` file via a script `run.py`,
which we're going to run in our Docker environment.

To simulate the same case for multiple turbulence models,
we're going to create a "foreach" DVC stage to run our
script over a sequence of argument values.
If we set this up properly, DVC will be smart enough to cache the results
and not rerun simulations when they don't need to be rerun.
We can create this stage with:

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

Another call to `calkit status` shows our pipeline needs to be run,
which makes sense, so let's give it another `calkit run`.
You'll note at the very start our Docker image build stage is not rerun
thanks to DVC tracking the inputs and outputs.

The output of `calkit status` now shows something we haven't seen yet:
we have some new data produced as part of those simulation runs.
We can do another `calkit save` to ensure everything is committed and
pushed:

```sh
calkit save -am "Run simulations"
```

In this case, the outputs of the simulations were pushed up to the DVC remote
in the Calkit Cloud.

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
    --description "Mean velocity profiles from DNS and RANS models." \
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

Another call to `calkit status` shows we need to run the pipeline again.

Now another call to `calkit run` and
`calkit save -m "Run pipeline to create figure"`
will create this figure and push it to the repo.
This figure is now viewable as its own object up on the website.

![Figure on website.](/images/repro-openfoam/figure-on-website.png)

## Solving the problem

Now let's show the value of having our project in a reproducible state,
addressing the problem we laid out in the introduction.
We're going to pretend we were forced to start from scratch,
so we'll clone a fresh copy of the repo
and attempt to simply change one of the axis labels slightly.

So we move back up a directory, delete the repo and clone it again with:

```sh
cd .. \
&& rm -rf rans-boundary-layer-validation \
&& calkit clone https://github.com/{your user name}/rans-boundary-layer-validation.git
```

Moving in there,
you'll notice our imported dataset,
the `postProcessing` directories,
and our figure PNG file were all downloaded,
which would not have happened with a simple `git clone`,
since those files are kept out of Git.

Running `calkit status` and `calkit run` again shows that what we've
cloned is fully up-to-date.

Next can edit our plotting script to make the relevant changes.
Then we execute `calkit run`.
Notice how the simulations were not rerun thanks to the DVC cache.
If we run `calkit status` we see there are some differences,
so we run `calkit save -am "Change x-axis label for reviewer 2"`
to get those saved and backed up.
If we go visit the project on the Calkit website, we see our figure is
up-to-date and has the requested changes in the legend.
Reviewer 2 will be so happy.

![Updated figure on website.](/images/repro-openfoam/figure-on-website-updated.png)

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
