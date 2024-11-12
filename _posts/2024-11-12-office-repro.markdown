---
comments: true
date: 2024-11-12
layout: post
title: Microsoft Word and Excel have no place in a reproducible research workflow... right?
categories:
- Open science
- Reproducibility
---

{% include figure.html
src="/images/repro-office/anakin-excel.jpg"
caption="Anakin uses Excel."
%}

Everyone knows that when you want to get serious about reproducibility
you need to stop using Microsoft Word and Excel and become a computer hacker,
right?
There is some truth to that, that working with simpler, open source,
less interactive tools is typically better for producing permanent artifacts
and enabling others to reproduce them,
but it's not mandatory.

On the other hand, it's starting to become more and more common,
and will hopefully someday be mandatory
to share all code and data when submitting a manuscript to a journal,
so that others can reproduce your work.
This is a good thing for science overall,
but also good for individual researchers,
even though it may seem like more work.

Besides the fact that you'll probably get
[more citations](https://doi.org/10.1371/journal.pone.0230416),
which should not necessarily be a goal in and of itself given recent
controversies around citation coercion,
working reproducibly will keep you more organized and focused,
and will allow you to produce higher quality work more quickly.
I would also be willing to bet that if reviewers can reproduce your work,
your paper will get through the review process more quickly.

![Data availability standards.](/images/repro-office/elsevier-research-data-guidelines.png)

In any case, here I'm going to show that you don't need to become a software
engineer to start working reproducibly.
Inspired by the article
[Ten Simple Rules for Computational Research](https://doi.org/10.1371/journal.pcbi.1003285),
we're going focus on just two rules:

1. **Keep all files in version control.**
  Something like Dropbox is not sufficient.
  When you make a change you should have to describe that change,
  and that record should exist in the log forever.
  Adding your initials and a number to the filename is also not good enough.
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
caption="Manual or ad hoc 'version control' (don't do this.) From phdcomics.com."
width="70%" %}

We're going to create our workflow with
[Calkit](https://github.com/calkit/calkit),
so if you want to follow along,
make sure it's installed per
[these instructions](https://github.com/calkit/calkit?tab=readme-ov-file#installation)
(you may want to add `--upgrade` to the `pip install` command if you have
an older version installed.)
We'll also need to ensure we have
[generated and stored a token in our local config](https://github.com/calkit/calkit/?tab=readme-ov-file#cloud-integration).

In order to follow rule number 1,
we are going to treat our project's repository, or "repo,"
as the place to store everything.
Any file that has anything to do with our work on this project
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
However, all the Git/DVC stuff will be done for us behind the scenes.

We can start off by creating a Git (and GitHub)
repo for our project
up on the [Calkit website](https://calkit.io).

{% include figure.html
src="/images/repro-office/create-project.png"
caption="Creating the project."
width="450px"
%}

Next, we'll do the only command line thing in this whole process
and spin up a local Calkit server.
This will allow us connect to the web app and allow us to modify the project
on our local machine.
To start the server, open up a terminal or Miniforge command prompt and run:

```sh
calkit local-server
```

If we navigate to our project page on calkit.io,
then go to the local machine page, we see that the repo has never been
cloned to our computer, so let's click the clone button.

![The repo has not yet been cloned.](/images/repro-office/needs-clone.png)

By default, it will be cloned somewhere
like `C:/Users/your-name/calkit/the-project-name`,
which you can see in the status.
We can also see that our repo is "clean,"
i.e., there are no untracked or modified files in there,
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
So, let's add it to the repo by clicking the "Add" button.

{% include figure.html
src="/images/repro-office/untracked-data.png"
caption="We have an untracked file."
width="450px"
%}

After adding and committing,
Calkit is going to automatically push to the remotes
so everything stays backed up,
and again we'll see that our repo is clean and in sync.

Now let's use Excel to create a figure.
If we go in and create a chart inside and save the spreadsheet,
we see up on the local machine page that we have a changed file.
Let's commit that change and give it a message like
"Add chart to spreadsheet".

![Our Excel chart.](/images/repro-office/excel-chart.png)

{% include figure.html
src="/images/repro-office/uncommitted-changes.png"
caption="We have some uncommitted changes in the repo."
width="450px"
%}

Alright, so now our data is in version control and we'll
know if it ever changes.
Now it's time for rule number 2: Generate important artifacts
with a pipeline.
At the moment our pipeline is empty,
so let's create a stage that extracts our chart from Excel into an image
and denotes it as a figure in the project.
On the web interface we'll see there's a button to create a new stage,
and in there we'll find some stage templates to use.
If we select "Figure from Excel",
there will be a few extra fields to fill out:

1. The name of the stage. We'll use `extract-chart`, but you can call it
   whatever you like.
1. The Excel file path relative to the repo (`data.xlsx`).
2. The desired output file path for our image. We'll use `figures/chart.png`,
   but again, you can choose whatever makes sense to you.
3. The title and description of our figure.

{% include figure.html
src="/images/repro-office/new-stage.png"
caption="Creating a new pipeline stage to extract our chart from Excel."
width="450px"
%}

After saving the stage the status view will tell us that the pipeline
is out-of-date,
which makes sense.
We added a stage but haven't yet run the pipeline.
So let's do that.

{% include figure.html
src="/images/repro-office/pipeline-out-of-date.png"
caption="Our pipeline is out-of-date."
width="450px"
%}

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

Now let's open up the Word document and insert our PNG image exported
from the pipeline.
Be sure to use the "link to file" or "insert and link"
option, so Word doesn't duplicate the image data inside
the document.
This will allow us to update the image externally and not need to
reimport into Word.

![Insert link to file.](/images/repro-office/insert-link-to-file.png)

Again when we refresh we'll see that `paper.docx` has uncommitted changes,
so let's commit them with a message like
"Add figure to paper".

Now let's complete our pipeline by adding a stage to convert our
Word document to PDF,
so that can be the main artifact we share with the outside world.
There's a stage template for that on the website,
so follow the stage generation steps we used to extract the figure, but
this time select the "Word document to PDF" template,
filling out the Word document file path, the output PDF path,
add `figures/chart.png` to the list of input dependencies,
and select "publication" as our artifact type.
Fill in the title and description of the publication as well.

{% include figure.html
src="/images/repro-office/word-to-pdf-stage-2.png"
caption="Adding a stage to convert our Word document to PDF."
width="450px"
%}

Again the pipeline will show that it's out-of-date,
so let's run and commit again, using a message like
"Export paper to PDF".
If we open up `paper.pdf` we can see that our figure is there
just like we expected.

But hold on a second you might say.
Why did we go through all this trouble just to create a PDF with
an Excel chart in it?
This would have been only a few steps to do manually!
That would be a valid point if this were a one-off project and nothing
about it would ever change.
However, for a research project, there will almost certainly be multiple
iterations (see again the PhD Comics cartoon above,)
and if we need to do each manual step each iteration,
it's going to get costly time-wise, and we could potentially forget
which steps need to be taken based on what file was changed.
We may end up submitting our paper with a chart that doesn't reflect
the most up-to-date data,
which would mean the chart in the paper could not be reproduced by a
reader.
Imagine if you have multiple datasets,
multiple steps of complex data analysis,
a dozen figures, and some slides to go along with your paper.
Keeping track of all that will consume valuable mental energy that could
be better spent on interpretation and communication of the results!

![Our final pipeline.](/images/repro-office/workflow-page.png)

To close the loop and show the value of using version control and a pipeline,
let's go and add a few rows to our dataset,
which will in turn change our chart in Excel.
If we save the file and look at the status,
we can see that this file is different,
and that our pipeline is again out-of-date,
meaning that our primary output (the PDF of the paper)
not longer reflects our input data.

![Adding rows.](/images/repro-office/chart-more-rows.png)

{% include figure.html
src="/images/repro-office/status-more-rows.png"
caption="After adding a row to the spreadsheet, our pipeline is again out-of-date."
width="450px"
%}

Now with one click we can rerun the pipeline,
which is going to update both our figure PNG file and the paper PDF in one
shot.
We can then create a commit message explaining that we added to the dataset.
These messages can be audited later to see when and why something changed,
which can come in handy if all of a sudden things aren't looking right.
Having the files in version control also means we can go check out an old
version if we made a mistake.

![Updated publication.](/images/repro-office/updated-publication.png)

We did it.
We created a reproducible workflow using Microsoft Word and Excel,
and we didn't need to learn Git or DVC.
Now we can iterate on our data, analysis, figures, and writing,
and all we need to do to get them all up-to-date and backed up is
to run the pipeline and commit the changes.
Now we can share our project and others can reproduce the outputs
(so long as they have a Microsoft Office license, but that's a topic
for another day.)
To recap, all we had to do was follow the two most important rules:

1. All files go in version control.
2. Artifacts need to be generated by the pipeline.

Everything we did here would probably have been a little faster via
the Calkit command line interface (CLI),
but it's important to see that being a terminal wizard is not a prerequisite
for working this way.

You can go browse through this project up on the
[Calkit website](https://calkit.io/petebachant/office-repro-example).

Feel free to shoot me an
[email](mailto:petebachant@gmail.com)
if you'd like help setting up something similar for your project.
