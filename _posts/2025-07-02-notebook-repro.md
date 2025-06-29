---
comments: true
date: 2025-07-02
layout: post
title: Stop abusing Jupyter Notebooks
categories:
  - Open science
  - Reproducibility
  - Software engineering
  - Jupyter
---

I love Jupyter Notebooks and use them all the time.
However, they have their own reproducibility crisis (TODO: citation),
and their abuse is probably contributing to the reproducibility
crisis in science (TODO: citation).
That is,
people share notebooks they used in their research but they don't
actually run.
They don't produce the outputs their author's say they did
and included in a paper, for example.

So here we're going to talk about how to improve
using some features I've recently built into Calkit,
as I've been progressing along the journey trying to build a framework
in which researchers can work reproducibly.

## 0. Understand what notebooks are for

Before we get into the how, let's talk about the why.

Notebooks are for generating evidence or artifacts.
If you're a software developer,
you can prototype your code in a notebook to provide evidence that
your idea is going to work before putting into a real codebase.
If you're a researcher, you can use a notebook to generate your figures
to include in a paper as evidence to support your conclusions.

Notebooks are not meant to be reusable tools.
They should do one thing: Produce the evidence.
If someone wants to modify a notebook to produce a different type of
evidence, that's great, but at that point it's a different notebook.

Similarly, research projects are not necessarily software projects.
Research projects seek to produce evidence to help answer questions,
and oftentimes tooling that was built for software development will be used.
Software projects seek to build reusable tools.
Research project may include software projects, however.
For example, imagine a researcher wants to build a tool to help others
answer questions or make predictions with the new knowledge they've
discovered.
They will create some software product,
but they will still TODO.

So, notebooks do one thing and should be able to keep doing that one thing
no matter how many times they've been run.

Don't spend your time ensuring the notebook is modular and reusable.
Just make sure it runs and generates the evidence it's supposed to.

Side note: Don't worry about sharing them if they're messy.
As long as they produce the evidence, i.e., they actually run,
they are valid.
"Research code" is there to be studied.
It's not meant to be a work of art.

Yes, you can use notebooks to build web apps,
which is a great use case for marimo in my opinion.
You can also use notebooks to write documentation or even entire books.
Some would also argue you can use notebooks to develop software.
These are interesting use cases, but they are not the most common ones,
and they are not the ones causing reproducibility issues.
Here we're talking about Jupyter Notebooks as used by scientists
and other researchers.
This might include data scientists and data engineers,
though they are typically a little more software oriented,
and their output products are a little bit more like tools than evidence.

## 1. Use version control

If you're going to use a notebook to provide evidence to prove a point,
you should certainly have that notebook backed up.
Storing it in a version control system like Git and pushing it to
a remote on the web like GitHub is a great way to do that.

However, if you don't think about it, you'll probably end up committing
a notebook with outputs.
This can make it hard to see the differences between notebooks,
as you'll like to save many versions as checkpoints along the way,
like tying off as you climb a mountain,
since the outputs are intermingled with the code in a JSON format.

Tools like `nbstripout` and `jupytext` are great here.

## 2. Declare your environment(s)

Never use notebooks in your global system environment,
e.g., Conda's `base` environment.
Declare an environment in which the notebook should run and run it there.
You may think declaring a few dependencies in a README is sufficient,
but the problem with that approach is that it's not tested or verified
each time you run the notebook,
and it's very possible to forget any changes you made to the environment
along the way.

With Calkit, you can create any type of Python environment with a similar
command:

```sh
calkit new {env-type} --name {env-name} {packages...}
```

In this case, `env-type` can be `conda-env`, `uv-venv`, `venv`, `pixi-env`,
depending on which package manager you prefer.
These days I've been falling back to `uv` by default,
since it's so fast (though Pixi is a faster Conda-compatible manager),
so I'll typically do something like:

```sh
calkit new uv-venv --name py1 --python 3.13 ipykernel jupyterlab polars plotly
```

The command above will create a new virtual environment with `uv`
and include the dependencies listed.
By default these will go into a `requirements.txt` file and the environment
will be created under a `.venv` prefix,
but these are selectable with the `--path` and `--prefix` arguments,
respectively.
They can also be changed later by editing the `environments` section of
the project's `calkit.yaml` file.

We can then launch JupyterLab in this environment with:

```sh
calkit xenv -n py1 jupyter lab
```

Calkit will always ensure the environment is up-to-date before executing
any command in it.
To add packages, simply put them in the requirements file and
rerun a command in the environment.
No need to activate and mutate it in place, as that can be another source
of forgotten details.

Calkit will also export a "lock file" for every environment type,
which can be committed to the project repo for later inspection or
rebuilding the exact environment used at a given time.

## 3. Never share anything generated interactively (use a pipeline)

Interactive work is the main benefit of using a notebook.
You can see feedback right away.
However, oftentimes this

Since caching is one of the hardest things in programming (TODO: source),
you probably shouldn't write your own caching logic.

This is the big one.
If you can follow this rule,
you can avoid most reproducibility pitfalls.
The mindset should be simple.
You can mess around in the notebook as much as you want,
but when it comes to producing the stuff that you'll share outside the
project,
make sure it's created with the pipeline.

This all of course assumes you're using Calkit,
which you should be, since it's free and open source,
though I am biased.

## An example

Here's a project that hopefully reflects a realistically
complex scenario.
