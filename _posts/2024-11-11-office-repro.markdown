---
comments: true
date: 2024-11-11
layout: post
title: Microsoft Word and Excel have no place in a reproducible workflow... right?
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
and being somewhat certain about how they were produced,
but it's not mandatory.

It's also not usually mandatory to work in a reproducible or open way, i.e.,
sharing all code, data, and other important information
so that others can create the same results.
These days, many journals are requiring a "data availability statement"
(see the example from Elsevier below,)
which allows authors to explain why code and data might not be available,
but hopefully someday it will be fully mandatory to share everything,
so here we're going to help you get a head start on that.
Who knows. Maybe if the reviewers can reproduce your work during the review
process, your paper will be published more quickly
(side note: has anyone studied that?)
At the very least, you'll probably get
[more citations](https://doi.org/10.1371/journal.pone.0230416).
I also hypothesize that working reproducibly will make you more efficient
and organized, leading to faster production of higher quality work,
so there's an individual benefit here too.

![Data availability standards.](/images/repro-office/elsevier-research-data-guidelines.png)

Inspired by the article
[Ten Simple Rules for Computational Research](https://doi.org/10.1371/journal.pcbi.1003285),
we're going to keep things simple and focus on two rules:

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

We're going to do this with the help of Calkit, so make sure it's installed
per
[these instructions](https://github.com/calkit/calkit?tab=readme-ov-file#installation)
(you may want to add `--upgrade` to the `pip install` command if you have
an older version installed.)

The first thing we're going to do is create a Git (and GitHub)
repo for our project,
which can be done up on the [Calkit website](https://calkit.io).
Don't worry though, we're not actually going to interact with Git directly.
I know this is a major sticking point for some people,
and I get it---learning Git is a daunting task.
However, Calkit will be doing the Gitting for us, so we're going to
_use Git without using Git_.

We are going to treat our project repo as the place to put everything.
That's right,
everything that has anything to do with our work on this project
goes in the repo.
This will save us time later because there will be no question about
where to look for stuff, because the answer is: in the repo.

The only command line thing we're going to do is spin up a local Calkit
server to connect to the web app and allow us to modify the project
on our local machine.
Someday this will likely run as a background service,
but for now, it needs to be started manually.
So, open up a terminal and run:

```sh
calkit local-server
```

TODO: Show server terminal running

If we navigate to our project page on the Calkit website,
then go to the local machine page, we see that the repo has never been
cloned to our computer, so let's click the clone button

TODO: Show local machine needing clone and cloning. Animated GIF?

By default, this will be cloned somewhere
like `C:/Users/YourName/calkit/the-project-name`,
which you can see in the status.

Now that we have our repository cloned locally let's "collect" our data.
We are going to do this by adding some rows to an Excel spreadsheet
and saving it in our project repo `data.xlsx`.

TODO: Show Excel rows being added.

Back on the Calkit local machine page,
we see that the `data.xlsx` spreadsheet is showing up as an untracked
file in our repo.
So, let's add it to the repo.

Now let's use Excel to create a figure.
If we go in and create a chart inside and save the spreadsheet,
we see up on the local machine page that we have a changed file.
Let's commit that change and give it a message like
"Add chart to spreadsheet".

Alright, so our data is in version control.
Now it's time to get to rule number 2: generate important artifacts
with a pipeline.
At the moment our pipeline is empty,
so let's create a stage that extracts our chart from Excel into an image
and denotes it as a figure in the repo.
