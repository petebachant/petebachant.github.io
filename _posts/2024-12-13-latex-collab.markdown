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
Collaborating on one of these can be painful.
There are cloud-based LaTeX collaboration tools that help,
the most popular of which is probably
[Overleaf](https://overleaf.com).
Overleaf is pretty neat,
but the free version is quite limited in terms of versioning, collaboration,
and offline editing.
Most importantly
I feel like it's only really suited to pure writing projects.
Research projects involve writing, sure,
but they also involve (often iteratively)
collecting and analyzing data, running simulations, creating figures, etc.,
which are not within the scope of Overleaf's functionality.

[Calkit](https://github.com/calkit/calkit)
on the other hand is a framework for all of the above,
including writing,
and is built upon tools that can easily run both in the cloud and locally,
on- or offline,
for maximum flexibility.
Here we're going to focus doing everything in a web browser.
We'll set up a collaborative LaTeX editing
environment with Calkit and
[GitHub Codespaces](https://github.com/features/codespaces),
a cloud-based virtual machine service.

Disclosure: There is a paid aspect of the Calkit Cloud,
which I manage,
to help pay for the costs of running the system,
and to prevent users for pushing up obscene amounts of data.
However, the software is open source and there is a free plan
that provides more than enough storage to do what we'll do here.

## Create the project

In order to follow along, you'll need a GitHub account,
so if you don't have one,
[sign up for free](https://github.com/signup).
Then head to [calkit.io](https://calkit.io),
sign in with GitHub,
and click the "create project" button.
Upon submitting, Calkit will create a new GitHub repository for us,
setup [DVC](https://dvc.org) (Data Version Control) inside it,
and create a so-called "dev container" configuration from
which we can spin up our GitHub Codespace and start working.

![Creating a new project.](/images/latex-collab/new-project.png)

## Configure Codespace secrets

In order to push artifacts like PDFs up to the Calkit Cloud's DVC remote,
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
Here we'll create the document in a new folder called `paper`:

![Creating the publication.](/images/latex-collab/new-pub-2.png)

Keep in mind that you'll be able add different LaTeX style and config
files later on if the generic article template doesn't suit your needs.
Also, if you have ideas for templates you think should be included,
drop a note in a
[new GitHub issue](https://github.com/calkit/calkit/issues/new).

## Create the Codespace

Next, from the project homepage on calkit.io,
click "Open in GitHub Codespaces."
Once created, we'll see an in-browser
[Visual Studio Code (VS Code)](https://code.visualstudio.com/)
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
in VS Code.

It might take few minutes to start up the first time
as the Codespace is created,
so go grab a coffee or take the dog for a walk.

![Creating the Codespace.](/images/latex-collab/building-codespace.png)

## Edit the document

After the Codespace is built and ready,
we can open up `paper/paper.tex` and start writing.

![Editing the source.](/images/latex-collab/paper.tex.png)

If you look in the upper right hand corner of the editor panel,
you'll see a play button icon added by the
[LaTeX Workshop](https://github.com/James-Yu/LaTeX-Workshop)
extension.
Clicking that will rebuild the document.
Just to the right of that button is one that will open the PDF in
split window,
which will refresh on each build.

![The editor with buttons.](/images/latex-collab/editor-split.png)

Note that the play button will run the entire pipeline,
not just the paper build stage,
so we can add more stages later, e.g., for creating figures,
or even another LaTeX document,
and everything will be kept up-to-date.
This is effectively the same thing as calling `calkit run`
from the terminal.
Check out the
[DVC stage documentation](https://dvc.org/doc/user-guide/pipelines/defining-pipelines#stages)
for more details on how to
build and manage your pipeline,
including how to define dependencies and outputs for the stages.

## Break lines in a Git-friendly way

This advice is not unique to cloud-based LaTeX editing,
but it's worth mentioning anyway.
When writing documents that will be versioned with Git,
make sure to break lines properly
by splitting them at punctuation or otherwise breaking into one
logical phrase per line.
This will help when viewing differences between versions
and proposed changes from collaborators.
If you write paragraphs as one long line and let them "soft wrap,"
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

## Commit and push/pull changes

For better or for worse,
working with Git/GitHub is different from other systems
like Google Docs, Overleaf, or Dropbox.
Rather than syncing our files automatically,
we need to deliberately "commit" changes to create a snapshot
and then sync or "push" them to the cloud.
This can be a stumbling block when first getting started with version control,
but it's valuable because it makes you stop and think about how to
describe a given set of changes.
More importantly, every snapshot will be available forever,
so if you create lots of them, you'll never lose work.
In a weird mood and ruined a paragraph that read well yesterday?
Easy fix---just revert the changes.

The VS Code interface has a built-in graphical tool for working with Git,
which can make things a little easier compare to learning the Git
command-line interface (CLI,)
if you're unfamiliar.
If we make some changes to `paper.tex`,
we can see a blue notification dot next to the source control icon in the
left sidebar.
In this view we can see there are two files that have been changed,
`paper.tex`, which is understandable,
and `dvc.lock`,
which is a file DVC creates to keep track of the pipeline,
and shows up in the "Staged Changes" list,
which is the list of files that would be added to a snapshot if we were
to create a commit right now.
We want to save the changes both this file and `paper.tex` in one commit,
so let's stage the changes to `paper.tex`,
write a commit message, and click commit.
It is conventional to use the imperative mood for commit messages,
so instead of something like "Added new text",
one might use "Add new text",
though it's totally up to you and your collaborators to define
that for your project.

![Staging the changes.](/images/latex-collab/stage.png)

After committing we'll see a button to sync the changes with the cloud,
which we can go ahead and press.
This will first pull and then push our commits up to GitHub,
which our collaborators will then be able to pull into their own workspaces.

### Push the PDF to the Calkit Cloud

The default behavior of DVC is to not save
pipeline outputs like our compiled PDF to Git,
but instead commit them to DVC,
since Git is not particularly good at handling large and/or binary files.
The Calkit Cloud serves as a "DVC remote" for us to push these artifacts
to back them up and make them available to our team.

If we go down to the terminal and run `calkit push`,
we'll push our DVC artifacts (just the PDF at this point)
up to the cloud as well,
which will make our PDF visible in the publications section of
the Calkit project homepage.
Note that `calkit push` will also send the Git changes to GitHub,
which completely backs up the project.

![Calkit push.](/images/latex-collab/push.png)

Later on,
if you end up adding things like large data files for analysis,
or even photos and videos from an experiment,
these can also be versioned in DVC and
backed up in the Calkit Cloud.

## Collaborate concurrently

What we've seen so far is an individual's workflow.
What if we have multiple people working on the document at the same time?
Other cloud-based tools like Google Docs and Overleaf
allow multiple people to edit a file simultaneously,
continuously saving behind the scenes.
My personal opinion is that concurrent collaborative editing is
usually not a good thing.
However, if you want to do it with this setup,
you still can,
but you'll need to communicate a little more with your collaborators
so you don't step on each other's toes and end up with merge conflicts,
which require manual fixes.
There's actually an experimental file locking feature on the Calkit Cloud
for notifying your team that the document should not be edited,
though at the time of writing the locks are only displayed,
not enforced.
You could also simply send your team a message on Slack letting them know
you're working on the doc, or a given section, and avoid conflicts that way.
Alternatively, if you really like the Google Docs experience,
you can setup the Codespace for
[live collaboration](https://docs.github.com/en/codespaces/developing-in-a-codespace/working-collaboratively-in-a-codespace).

There are other strategies that can work as well.
Git is actually quite good at automatically merging changes together.
Ultimately you just want to make sure no two people are working on the same
line(s) at the same time.
You could split up the work by paragraph,
or even use LaTeX `\input` commands in the main `.tex` file
to allow each collaborator to work
on their own file, e.g.,
if you've divided up the work by chapter or section.

Git can also create different branches of the repo in order to merge them
together at a later time, optionally via GitHub pull requests,
which can allow the team to review proposed changes before they're
incorporated.
However, for many projects,
it will be easier to have all collaborators simply commit
to the main branch and continue to clean things up as you go.
If commits are kept small with descriptive messages,
this will be even easier.

To boil this down to one piece of advice,
be sure to run `git pull` often, either from the UI or from the terminal.

## Manage the project with GitHub issues

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

For complex cases with lots of tasks and team members,
GitHub projects is a nice tool,
allowing you to put your tasks into a Kanban board or table,
prioritize them, rate their effort level, and more.

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
