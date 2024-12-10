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

## Create the Calkit project

In order to set this up, you will first need a GitHub account.
Then head to [calkit.io](https://calkit.io),
sign in with GitHub,
and click the "create project" button.

Upon submitting, Calkit will create a GitHub repo for us,
setup DVC,
and create a so-called "dev container" configuration from
which we can spin up our GitHub Codespace.

## Configure Codespace secrets

In order to push our PDF artifacts up to the Calkit cloud,
we will need a token.
You can skip this step if you want to keep your compiled PDFs elsewhere,
e.g., commit them directly to Git,
which is okay if there small and/or won't change often.

TODO: Quick action on Calkit homepage to manage Codespace secrets
that goes to
https://github.com/{owner}/{repo}/settings/secrets/codespaces

Create a secret called `CALKIT_DVC_TOKEN`
and paste in the value.

Quick action should generate the DVC token, then allow them to copy
and click a link to add to

"Create a DVC token and add to GitHub Codespace secrets"

## Optional: Setup a prebuild for the Codespace configuration

This will help speed things up a bit.

## Add a new publication to the project

TODO: Enable below

Click the quick action to "create a new publication."
In the dialog,
select the `latex/article` template.
This will add a LaTeX article to our repo and a build stage to our
DVC pipeline,
which will use a Docker container to build the document.
Let's create the document in a new folder called `paper`:

![Creating the publication.](TODO)

TODO: Add these as shortcuts on the project homepage?
This could also include adding pipeline stages, etc.

## Edit the document in a GitHub Codespaces dev container

Next, click "edit in GitHub Codespace."
This will open up a new tab with an in-browser VS Code
editor, which will have access to our GitHub repo
and will be able to compile the LaTeX document.

If we execute `calkit run` in the terminal,
we'll see the document will be compiled to `paper/paper.pdf`
We can add some text to the document
and rebuild it with the play button icon in the upper right corner of
the editor.
In the TeX section of the toolbar on the left there are
some quick commands for building the document and viewing the PDF.
Saving the `paper.tex` file should kick of an automatic rebuild
and refresh the PDF view if it's open.

### Tip: Break your lines properly

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
which can make things a little easier compare to learning the Git CLI,
if you're unfamiliar.
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

### Pushing the PDF to the Calkit Cloud

The default behavior of DVC is to not save
pipeline outputs to the repo, but instead commit them to DVC.
The Calkit Cloud serves as a DVC remote for us to push these artifacts
to back them up.
Running `calkit push` will send our PDF to the cloud
and make it viewable on the project's publications page.
Note that `calkit push` will also send the Git changes to GitHub,
which completely backs up the project.

## Handling concurrent collaboration

Other cloud-based tools like Google Docs and Overleaf
allow multiple people to edit a document at the same time,
continuously saving behind the scenes.
My personal opinion is that concurrent collaborative editing is
usually not a good thing.
However, if you want to do it with this setup,
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

You could also have a collaborator mark up a PDF and submit a single GitHub
issue with the PDF attached.

These issues will also show up in the "To-do" section of the Calkit project
homepage.

## Conclusions

Here we showed how to collaborate on a Calkit project's LaTeX document
in the cloud using a GitHub Codespace.
This setup will allow us to do the other things we'll
need to do in our research project like store datasets,
process them, create figures,
and also build them into our paper.
It can all happen in one place with one command.
We are also able to work equally well locally as we can in the cloud,
providing maximum flexibility.
