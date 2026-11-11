---
comments: true
date: 2026-11-11
layout: post
title: "AI agents won't work reproducibly if you don't tell them to"
categories:
  - Open science
  - Reproducibility
  - Software engineering
  - AI
  - Agentic AI
  - Research software
---

AI coding agents like Claude Code, Codex, and OpenCode are
amazing little information machines, but their use comes with some risk.
Everyone has heard of the hallucination problems,
where the large language model (LLM) seems to simply make things up,
but what about their use in research computations?
These agents are very good at writing code and analyzing data.
They'll produce beautiful HTML artifacts filled with rich figures
and tables,
but do they work in a verifiable, transparent, and reproducible way,
such that they could be trusted to produce scientific evidence
and fully describe how they did so?

To find out, I set up a little computational experiment.
Claude Code, Codex, and OpenCode were all given the same prompt to
analyze and visualize a dataset, then create a short report.
<!-- TODO: Get n reps in here? -->
Each was repeated multiple times in a "sandbox" so it mimicked
a fresh install with a new user on a new machine.
Their work was evaluated based on whether or not they followed
these computational reproducibility best practices:

1. Use version control to keep a history of all file changes.
2. Use an environment manager to record the exact package versions used,
   i.e., save a "lock file."
3. Use a pipeline or build system that tracks the content in
   (i.e., hashes) input and output files.
4. Define the provenance (or source) for any data imported or created by hand.
5. Automate the propagation of components into composite artifacts, e.g.,
   figures and numerical results computed in a script and then used in a
   document. The alternative is manual uploads or copy/paste.

The implication is that if the agents follow these practices,
it will be quick and easy to verify that the outputs were indeed produced
by the inputs and process definitions (scripts, notebooks, etc.)
The goal is to have something runnable, but not need to actually
run it to be able to understand how the outputs were created,
which is especially important for expensive, long-running tasks like
large scale simulations.
With verification made easier, we can spend more time and effort validating
that the approach properly answers the research questions.

Now let's talk about the results.
I'm not sure if I found this surprising,
but when not asked to work reproducibly, the agents basically never did.
All saved their source code with the exception of one Codex run,
which sent raw text directly into R.
Only one OpenCode agent saved an environment spec file (requirements.txt),
but it didn't include exact versions, so it doesn't count as passing
rule 2.

Of course I can't get through a blog on my own website without
shilling some free software, so I repeated the same experiment
with "Use Calkit." added to the prompt. That's it---just two extra words
and everything else left as is.
This (also maybe not surprisingly) bumped reproducibility rates up
significantly.
All agents saved their source code and used an I/O hashing pipeline.
Nearly all used good environment management practices.
One interesting outlier was Codex,
which never used version control in any run.
OpenCode was the only agent that actually attempted to define the provenance
of the raw data, but only in one instance.
On the whole, however, OpenCode did the best, so if you're looking
for the most transparent and reproducible agent,
it might be your best bet.
It's also the only one whose source code is openly available.

One aspect of reproducibility that was not explicitly graded is the
mapping of numerical results into the report document.
In the non-Calkit case, the agent simply copied the results in,
which was generally okay, except for one case where the agent
averaged already-rounded numbers and quoted a result that was different
from that printed by the analysis by one decimal place.

<!-- TODO: cite recent blog where copy/paste errors were common
https://babieslearninglanguage.blogspot.com/2026/11/an-ai-audit-of-my-works-computational.html
-->

AI agents make producing research outputs so much faster.
This experiment itself was put together with Claude Code and I think
it would have taken at least ten times longer if done by hand.
However, the bottleneck
has now shifted to verification and validation---checking that
the outputs were generated as described, and that they actually back
up the claims.
For verification, following reproducibility best practices is key
This experiment itself was done in a Calkit project, which you are free
to attempt to reproduce, or maybe replicate since it's not really
possible to remove randomness from LLM outputs.
In any case, better reproducibility in your agentic analysis workflows
is two words away: just tell your agents to use Calkit.
