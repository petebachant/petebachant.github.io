---
comments: true
date: 2024-12-13
layout: post
title: Cloud-based LaTeX collaboration with Calkit and GitHub Codespaces
categories:
  - Open science
  - Reproducibility
  - Collaboration
  - Open source
---

Research projects will very often involve some sort of LaTeX document,
e.g., a conference paper, slide deck, journal article,
or multiple of each.

Here we're going to walk through setting up a collaborative LaTeX editing
environment with Calkit and GitHub Codespaces.

There are other cloud-based LaTeX collaboration tools,
e.g., Overleaf, which is great,
but I feel like tools like Overleaf are
mostly suitable to pure writing projects.
Research projects involve writing, sure,
but they also involve collecting data,
analyzing data, creating figures, etc.,
which is not within the scope of Overleaf.
Calkit on the other hand is intended to be a framework for all of the above,
including the writing part,
and leverages tools that can easily run both in the cloud and locally,
for maximum flexibility.

Full disclosure: There is a paid aspect of the Calkit Cloud
to help pay for the costs of running the system,
since it allows for storage of artifacts like PDFs,
but the software is fully open source and there is a free plan
that provides more than enough storage to do what we'll do here.

## Prerequisites

In order to set this up, you will need a GitHub account.

## Create the project

Head to [calkit.io](https://calkit.io),
sign in with GitHub,
and click the "create project" button.

TODO: Remove plan selection?

Upon submitting, Calkit will create a GitHub repo for us,
setup DVC,
and create a so-called "dev container" configuration from
which we and our collaborators can spin up our GitHub Codespace.

Note that this will create a full Calkit project and DVC pipeline.
You could remove those dependencies if this truly were a pure writing
project,
but they don't add much overhead anyway,
and will give you the flexibility to add things like figure generation
steps to run ahead of the paper compilation,
and setup the appropriate dependencies.

## Configure Codespace secrets

In order to push our PDFs up to the Calkit cloud,
we will need a token.
You can skip this step if you want to keep your compiled PDFs elsewhere,
e.g., commit them directly to Git,
which is okay if there small and/or won't change often.

## Optional: Setup a prebuild for the Codespace configuration

This will help speed things up a bit.

## Add a new publication to the project

On the publications tab,
create a new publication,
select the type as report for now,
and select the `latex/article` template.
This will add a LaTeX article to our repo and a build stage to our
DVC pipeline,
which will use a Docker container to build the document.

Let's create the document in a new folder called `paper`:

![Creating the publication.](TODO)

TODO: Add these as shortcuts on the project homepage?
This could also include adding pipeline stages, etc.

## Edit the document in a dev container

Next, click "edit in GitHub Codespace."
This will open up a new tab with an in-browser VS Code
editor, which will have access to our GitHub repo
and will be able to compile the LaTeX document.

If we execute `calkit run` in the terminal,
we'll see the document will be compiled.

### Break your lines properly

When writing documents that will be versioned with Git,
you want to make sure you break lines properly
by splitting them at punctuation or otherwise breaking into one
logical phrase per line.
This will help when viewing differences between versions
and proposed changes from collaborators.
If you write paragraphs as one long line and let your editor "soft wrap"
them,
it will be a pain.

So, instead of writing something like:

```
This is my very long and nice paragraph. It consists of many sentences, which make up the paragraph.
```

write:

```
This is my very long and nice paragraph.
It consists of many sentences,
which make up the paragraph.
```

The compiled document will look the same.

Add some text to `paper/paper.tex` and press the play button icon
in the upper right corner.
This will automatically call `calkit run` again and refresh the PDF view.

## Commit and push/pull changes

The VS Code interface has a built in graphical tool for working with Git,
which can make things a little easier.
You can do most of what you need to do if you know these concepts:

- Repository (repo): A collection of files tracked with Git.
- Commit: A set of changes saved to the repo.
- Push: Send updates to the cloud.
- Pull: Download updates from the cloud and merge them into our current
  working copy of the repo.
- Stage: Add files to a commit.

Using GitHub pull requests is outside the scope of this article.
For many projects,
it will make sense to have all collaborators simply commit
to the main branch and continue to clean things up as you go.

## Handling concurrent collaboration

Other cloud-based tools like Google Docs and Overleaf
allow multiple people to edit a document at the same time,
continuously saving behind the scenes.
In this workflow, we're using Git,
which also technically allows concurrent editing,
but every change or batch of changes needs to be deliberately committed,
rather than being saved automatically.

My personal opinion is that concurrent collaborative editing is
actually not a good thing.
However, if you want to do it,
you still can,
but you'll need to communicate a little more with your collaborators
so you don't step on each other's toes and end up with merge conflicts.

The Calkit web app has a feature that allows nominally locking files for
editing,
but at the time of writing is doesn't enforce these locks.
You can use this so your collaborators see they shouldn't
work on the file at the same time,
or simply shoot them a message on Slack or something to pass the ball around.

There are other strategies that can work as well.
Ultimately you just want to make sure no two people are working on the same
paragraph(s) at the same time.
You could split up the work by paragraph,
or even use LaTeX `\input` commands to allow each collaborator to work
on their own file, e.g.,
if you've divided up the work by chapter or section.

## Commenting and project management

If you highlight a region of the PDF, you can create a comment
and a corresponding GitHub issue.
If you make a commit that addresses a given issue,
you can include "fixes #5" or "resolves #5" in the commit message,
and GitHub will automatically close it.
I love that feature!

In the `.tex` file, you can highlight some text and create a GitHub
issue from it with the "Create Issue From Selection" command.
Open up the command palette with `ctrl/cmd+shift+p` and
start typing "issue from selection".
The command should show up at the top of the list.
After you create a new issue,
click the GitHub icon in the left pane and look through the recent issues.
You can right click on an issue and select "Go to Linked Code" to do just
that.

TODO: Feature for uploading marked up PDF?

## Conclusions

This setup will allow us to do the other things we'll
need to do in our research project like store datasets,
process them, create figures,
and also build them into our paper.
It can all happen in one place with one command.
