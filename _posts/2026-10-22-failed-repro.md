---
comments: true
date: 2026-10-22
layout: post
title: "A journal article reviewer actually tried to reproduce our results... and failed"
categories:
  - Open science
  - Reproducibility
  - Software engineering
---

Ever since starting my PhD back in 2012,
any paper I published (unless there were some commercial restrictions)
included open code, data, simulation configs, even computer aided design (CAD)
files.
Per the FAIR principles promoted by the Open Science movement...
And yet, throughout all those rounds of journal article review,
not once did a referee actually try to run the code.

Now, maybe it was because it didn't look easy to run,
or the work seemed simple enough that there was no risk that the
code didn't match the mathematical formulas and prose describing
the methods.
Whatever it was, the "supplementary materials",
which I feel and integral to the work, not just supplementary,
were not checked, as far as I could tell.

Fast forward to 2025 and I'm working with a team at Caltech,
University of Minnesota, and more,
to rebuild an astronomical alert broker so it can scale up to accommodate
the much heavier data stream from the
Vera C. Rubin observatory, or Legacy Survey of Space and Time (LSST),
an instrument that will facilitate numerous discoveries in astrophysics
and astronomy.

We had written a paper about the new broker,
[BOOM](https://github.com/boom-astro/boom),
and it included a strong scaling test to show that indeed,
this new system could scale to meet the load it would encounter.
I used this as an opportunity to use Calkit to integrate this scaling
test and its results with the writing, done by most others on the team
in Overleaf.
Basically, we were changing the code and iterating on how the test was
run dozens of times, and I didn't want the "reproducibility anxiety"
or tedium of manually copying and pasting figures and results into Overleaf.
The final scaling enhancement factor was an output of the pipeline,
injected into the LaTeX source, so even that did not need a find-and-replace
when it inevitably changed as we iterated.
