---
comments: true
date: 2024-11-11
layout: post
title: Microsoft Word and Excel have no place in a reproducible research workflow... right?
categories:
- Open science
- Reproducibility
---

![Anakin uses Excel.](/images/repro-office/anakin-excel.jpg)

Everyone knows that when you want to get serious about reproducibility
you need to stop using Microsoft Word and Excel and become a computer hacker,
right?
There is some truth to that, that working with simpler, open source,
less interactive tools is typically better for producing permanent artifacts
and enabling others to reproduce them,
but it's not mandatory.

On the other hand, it's starting to become more and more common,
and will hopefully someday be mandatory
to share all code and data when submitting an article to a journal,
so that others can reproduce your work.
This is a good thing for science overall,
but also good for individual researchers.
Besides the fact that you'll probably get
[more citations](https://doi.org/10.1371/journal.pone.0230416),
which should not necessarily be a goal in and of itself given recent
controversies around citation coercion,
working reproducibly will keep you more organized and focused,
and will allow you to produce higher quality work more quickly.
I also hypothesize that if reviewers can reproduce your work,
your paper will get through the review process more quickly.

![Data availability standards.](/images/repro-office/elsevier-research-data-guidelines.png)

In any case, here I'm going to show that you don't need to become a software
engineer to start working reproducibly.
Inspired by the article
[Ten Simple Rules for Computational Research](https://doi.org/10.1371/journal.pcbi.1003285),
we're going focus on just two simple rules:

1. **Keep all files in version control.**
  Something like Dropbox is not sufficient.
  When you make a change you should have to describe that change,
  and that record should exist in the log forever.
  Adding your initials and a number to the filename is also not good enough!
  Whenever you’ve made a change with any value, _commit_ it.
  When all files are in a version control repository, it's like using
  "track changes" for an entire folder.
1. **Generate permanent artifacts with a pipeline.**
  This will allow us to know if our output artifacts, e.g., figures,
  derived datasets, papers,
  have become out-of-date and no longer reflect their input data or
  processing procedures, after which we can run the pipeline and get them
  up-to-date.
  It also means we only need to focus on building that pipeline and running
  it. We don't need to memorize what scripts to run in what order---just
  run the pipeline.

{% include figure.html
src="/images/repro-office/phd-comics-version-control.webp"
caption="Manual or ad hoc "version control" (don't do this.) From phdcomics.com."
width="90%" %}

We're going to do this with the help of
[Calkit](https://github.com/calkit/calkit),
so if you want to follow along,
make sure it's installed per
[these instructions](https://github.com/calkit/calkit?tab=readme-ov-file#installation)
(you may want to add `--upgrade` to the `pip install` command if you have
an older version installed.)
We'll also need to ensure we have
[generated and stored a token in our local config](https://github.com/calkit/calkit/?tab=readme-ov-file#cloud-integration).

In order to follow rule number 1,
we are going to treat our project's repository, or "repo",
as the place to store everything.
That's right,
any file that has anything to do with our work on this project
goes in the repo.
This will save us time later because there will be no question about
where to look for stuff, because the answer is: in the repo.

This repo will use [Git](https:/git-scm.com) for text files
and [DVC](https://dvc.org) for binary files, e.g., our Excel spreadsheets
and Word documents.
Don't worry though, we're not actually going to interact with Git
and DVC directly.
I know this is a major sticking point for some people,
and I get it---learning Git is a daunting task.
However, all the Git stuff will be done for us behind the scenes.

We can start off by creating a Git (and GitHub)
repo for our project
up on the [Calkit website](https://calkit.io).

![Creating the project](/images/repro-office/create-project.png)

Next, we'll do the only command line thing in this whole process
and spin up a local Calkit server.
This will allow us connect to the web app and allow us to modify the project
on our local machine.
To start the server, open up a terminal or Miniforge command prompt and run:

```sh
calkit local-server
```

![Local server running.](/images/repro-office/local-server.png)

If we navigate to our project page on the Calkit website,
then go to the local machine page, we see that the repo has never been
cloned to our computer, so let's click the clone button

![The repo has not yet been cloned.](/images/repro-office/needs-clone.png)

By default, this will be cloned somewhere
like `C:/Users/your-name/calkit/the-project-name`,
which you can see in the status.
We can also see that our repo is "clean,"
i.e., there are no untracked files or modified files in there,
and that our local copy is synced with both the Git and DVC remotes,
meaning everything is backed up and we have the latest version.
We'll strive to keep it that way.

Now that we have our repository cloned locally let's "collect" our data.
We are going to do this by adding some rows to an Excel spreadsheet
and saving it in our project repo `data.xlsx`.

![Our Excel data.](/images/repro-office/excel-data.png)

Back on the Calkit local machine page,
we see that the `data.xlsx` spreadsheet is showing up as an untracked
file in our repo.
So, let's add it to the repo.

![Untracked data file.](/images/repro-office/untracked-data.png)

![Adding data.](/images/repro-office/add-data.png)

After adding, Calkit is going to automatically push to the remotes
so everything stays backed up,
and again we'll see that our repo is clean and in sync.

Now let's use Excel to create a figure.
If we go in and create a chart inside and save the spreadsheet,
we see up on the local machine page that we have a changed file.
Let's commit that change and give it a message like
"Add chart to spreadsheet".

![Our Excel chart.](/images/repro-office/excel-chart.png)

![Uncommitted changes.](/images/repro-office/uncommitted-changes.png)

Alright, so now our data is in version control and we'll
know if it ever changes.
Now it's time for rule number 2: Generate important artifacts
with a pipeline.
At the moment our pipeline is empty,
so let's create a stage that extracts our chart from Excel into an image
and denotes it as a figure in the repo.
On the web interface we'll see there's a button to create a new stage,
and in there we'll find some stage templates to use.
If we select "Figure from Excel",
there will be a few extra fields to fill out:

1. The name of the stage. We'll use `extract-chart`, but you can call it
   whatever you like.
1. The (local) Excel file path (`data.xlsx`).
2. The desired output file path for our image. We'll use `figures/chart.png`,
   but again, you can choose whatever makes sense to you.
3. The title and description of our figure.

![Creating a new stage.](/images/repro-office/new-stage.png)

After saving the stage the status view will tell us that the pipeline
is out-of-date,
which makes sense.
We added a stage but haven't yet run the pipeline.
So let's do that.

![Pipeline is out of date.](/images/repro-office/pipeline-out-of-date.png)

After the pipeline has been run we can see there are some uncommitted
changes in the repo, so let's commit them with a message that makes sense,
e.g., "Extract figure from data.xlsx".
We should again be in our happy state, with a clean repo synced with the cloud,
and a pipeline that's up-to-date.

To wrap things up, we're going to use this figure in a paper,
written using Microsoft Word.
So, find a journal with a Microsoft Word (`.docx`) submission template,
download that, and save it in the repo.
In this case, I saved the template as a generic name like `paper.docx`,
since in the context of this project, it doesn't really need a special name,
unless of course `paper.docx` would somehow be ambiguous.
We can then follow the same process we followed with
`data.xlsx` to add and commit the untracked file to the repo.

![Untracked paper.docx.](/images/repro-office/untracked-paper.png)

Now let's open up the Word document and insert our PNG image exported
from the pipeline.
Be sure to use the "insert and link"
option, so Word doesn't create an additional copy of the image data inside
the document.
This will allow us to update the figure and not need to reimport into Word.

![Insert and link image.](/images/repro-office/insert-and-link.png)

Again when we refresh we'll see that `paper.docx` has uncommitted changes,
so let's commit them with a message like
"Add figure to paper".

Now let's complete our pipline by adding a stage to convert our
Word document to PDF,
so that can be the main artifact we share with the outside world.
There's a stage template for that on the website,
so follow the stage generation steps we used to extract the figure, but
this time select the "Word document to PDF" template,
filling out the Word document file path, the output PDF path,
and select "publication" as our artifact type.
Fill in the title and description of the publication as well.

![Adding the Word to PDF stage.](/images/repro-office/word-to-pdf-stage.png)

Again the pipeline will show that it's out-of-date,
so let's run and commit again, using a message like
"Export paper to PDF".

But hold on a second you might say.
Why go through the trouble of using version control and a pipeline
when I could do all of this manually?
It's only a few steps. I can remember that!

Here we'll illustrate that value for a simple project like this.
But note: Most projects will become much more complex,
with many figures, different datasets, etc.

Let's go and add a few rows to our dataset,
which will in turn change our chart in Excel.
If we save the file and look at the status,
we can see that this file is different,
and that our pipeline is again out-of-date,
meaning that our primary output (the PDF of the paper)
not longer reflects our input data.

If we wanted to do this manually,
we would need to track the "cache invalidation" in our heads,
noting that we need to re-export our figure and re-export our Word document
to PDF.
This can be tedious for a simple project such as this,
so it's worth it to save the cognitive overhead and just let Calkit manage
this stuff so we can focus on more important things,
like writing a good argument or making our figure beautiful.

Now with one click we can rerun the pipeline,
which is going to update both our figure PNG file and the paper PDF in one
shot.
We can then create a commit message explaining that we added to the dataset.
These messages can be audited later to see when and why something changed,
which can come in handy if all of a sudden things aren't looking right.

We did it.
We created a reproducible workflow using Microsoft Word and Excel,
and we didn't need to learn how Git or DVC work under the hood.
Now we can share our project and others can reproduce the outputs.
All we had to do was follow the two most important rules:

1. All files go in version control.
2. Artifacts should be generated by the pipeline.

As always, feel free to shoot me an
[email](mailto:petebachant@gmail.com)
if you'd like help setting up something similar for your project.
