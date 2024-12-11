---
comments: true
date: 2024-12-11
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
Collaborating on one of these can be a pain.

There are cloud-based LaTeX collaboration tools that promise to make this
easier,
the most popular of which is probably
[Overleaf](https://overleaf.com).
Overleaf is pretty neat,
but the free version is quite limited in terms of versioning and collaboration,
and more importantly
I feel like it's only really suited to pure writing projects.
Research projects involve writing, sure,
but they also involve a potentially iterative workflow including
collecting and analyzing data, running simulations, creating figures, etc.,
which are not within the scope of Overleaf.

[Calkit](https://github.com/calkit/calkit)
on the other hand is intended to be a framework for all of the above,
including writing,
and leverages tools that can easily run both in the cloud and locally,
for maximum flexibility.
Here, however, we're going to focus doing everything in a web browser.
We'll walk through setting up a collaborative LaTeX editing
environment with Calkit and GitHub Codespaces.

Disclosure: There is a paid aspect of the Calkit Cloud,
which I manage,
to help pay for the costs of running the system,
and to prevent users for pushing up obscene amounts of data.
However, the software is open source and there is a free plan
that provides more than enough storage to do what we'll do here.

## Create the project

In order to follow along, you will first need a GitHub account.
Then head to [calkit.io](https://calkit.io),
sign in with GitHub,
and click the "create project" button.
Upon submitting, Calkit will create a GitHub repo for us,
setup DVC,
and create a so-called "dev container" configuration from
which we can spin up our GitHub Codespace.

![Creating a new project.](/images/latex-collab/new-project.png)

## Configure Codespace secrets

In order to push our PDF artifacts up to the Calkit Cloud's DVC remote,
we will need a token.
You can skip this step if you want to keep your compiled PDFs elsewhere,
e.g., commit them directly to Git,
which is okay if there small and/or won't change often.

On the Calkit project homepage you'll see a link to manage user tokens.
Head over there and create one, selecting "DVC" as the purpose.
Save this in a password manager if you have one,
then head back to the project homepage and click the quick action link
to manage GitHub Codespaces secrets for the project.
Create a secret called `CALKIT_DVC_TOKEN`
and paste in the token.

![Adding the secret.](/images/latex-collab/codespaces-secrets-2.png)

## Add a new publication to the project

Next, click the quick action to "create a new publication from template."
In the dialog,
select the `latex/article` template,
and fill in the rest of the required information.
This will add a LaTeX article to our repo and a build stage to our
DVC pipeline,
which will automatically create
a TeX Live Docker container to build the document.
Let's create the document in a new folder called `paper`:

![Creating the publication.](/images/latex-collab/new-pub-2.png)

## Create the Codespace

Next, click "Open in GitHub Codespaces."
Once created, we'll see an in-browser VS Code
editor, which will have access to our project repository
and will be able to compile the LaTeX document.
Consider this your very own virtual machine in the cloud for working
on this project.
You can update settings, add extensions, install packages, etc.
You have total control over it.
Note that GitHub does
[charge for this service](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces),
but the free plan limits are reasonably generous.
It's also quite easy to run the same dev container config locally in
[VS Code](https://code.visualstudio.com/).

This might take few minutes to start up the first time,
so go grab a coffee or take the dog for a walk.

![Creating the Codespace.](/images/latex-collab/building-codespace.png)

## Edit the document

After the Codespace is built and ready,
we can open up `paper/paper.tex` and start editing.

![Editing the source.](/images/latex-collab/paper.tex.png)

If you look in the upper right hand corner of the editor panel,
you'll see a play button icon thanks to the
[LaTeX Workshop](https://github.com/James-Yu/LaTeX-Workshop)
extension.
Clicking that play button will rebuild the document.
Just to the right of that button is one that will open the PDF in
split window,
which will refresh on each build.

![The editor with buttons.](/images/latex-collab/editor-split.png)

Note that the play button will run the entire pipeline,
not just the paper build stage,
so we can add more stages later, e.g., for creating figures,
or even another LaTeX document,
and everything will be kept up-to-date.
Check out the
[DVC stage documentation](https://dvc.org/doc/user-guide/pipelines/defining-pipelines#stages)
for more details on how to
build and manage your pipeline,
including how to define dependencies and outputs for the stages.

If we execute `calkit run` in the terminal,
we'll see the document will be compiled to `paper/paper.pdf`
We can add some text to the document
and rebuild it with the play button icon in the upper right corner of
the editor.

## Break lines in a Git-friendly way

This particular advice is not unique to cloud-based LaTeX editing,
but it's worth mentioning anyway.
When writing documents that will be versioned with Git,
make sure to break lines properly
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

The VS Code interface has a built-in graphical tool for working with Git,
which can make things a little easier compare to learning the Git CLI,
if you're unfamiliar.
You can do most of what you need to do if you know these concepts:

- Repository (repo): A collection of files tracked with Git.
- Commit: A set of changes saved to the repo.
- Push: Send updates to the cloud.
- Pull: Download updates from the cloud and merge them into our current
  working copy of the repo.
- Stage: Add files to a commit.

If we make some changes to `paper.tex`,
we can see a blue notification dot next to the source control icon in the
left sidebar.
In this view we can see there are two files that have been changed,
`paper.tex`, which is understandable,
and `dvc.lock`,
which is a file DVC creates to keep track of the pipeline,
and shows up in the "Staged Changes" list.
We want to save the changes both this file and `paper.tex` in one commit,
so let's stage the changes to `paper.tex`,
write a commit message, and click commit.

![Staging the changes.](/images/latex-collab/stage.png)

We'll then see a button to sync the changes with the cloud,
which we can go ahead and press.

### Pushing the PDF to the Calkit Cloud

The default behavior of DVC is to not save
pipeline outputs to the repo, but instead commit them to DVC,
because Git is not particularly well suited to large files.
The Calkit Cloud serves as a DVC remote for us to push these artifacts
to back them up.
If we go down to the terminal and run `calkit push`,
we'll push our DVC artifacts (just the PDF at this point)
up to the cloud as well,
which will make our PDF visible in the publications section of
the Calkit project homepage.
Note that `calkit push` will also send the Git changes to GitHub,
which completely backs up the project.

![Calkit push.](/images/latex-collab/push.png)

## Handling concurrent collaboration

What we've seen so far is an individual's workflow.

Other cloud-based tools like Google Docs and Overleaf
allow multiple people to edit a document at the same time,
continuously saving behind the scenes.
My personal opinion is that concurrent collaborative editing is
usually not a good thing.
However, if you want to do it with this setup,
you still can,
but you'll need to communicate a little more with your collaborators
so you don't step on each other's toes and end up with merge conflicts.
Alternatively, if you really like the Google Docs experience,
you can setup the Codespace for
[live collaboration](https://docs.github.com/en/codespaces/developing-in-a-codespace/working-collaboratively-in-a-codespace).

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

Using GitHub pull requests is outside the scope of this article.
For many projects,
it will make sense to have all collaborators simply commit
to the main branch and continue to clean things up as you go.

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

The LaTeX `todonotes` extension can also work nicely,

Show GitHub.dev link?

## Conclusions

Here we showed how to collaborate on a Calkit project's LaTeX document
in the cloud using a GitHub Codespace.
This setup will allow us to do the other things we'll
need to do in our research project like store datasets,
process them, create figures,
and also build them into our paper.
It can all happen in one place with one command
(see [this example](https://calkit.io/calkit/example-basic).)
We are also able to work equally well locally as we can in the cloud,
providing maximum flexibility.
Most importantly,
anyone on our team will be able to reproduce the results.
