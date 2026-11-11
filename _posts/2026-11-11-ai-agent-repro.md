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
analyze and visualize a dataset.
<!-- TODO: Get n reps in here? -->
Each was repeated multiple times in a "sandbox" so it mimicked
a fresh install with a new user on a new machine.
Their work was evaluated based on whether or not they followed
these computational reproducibility best practices:

1. Use version control to keep a history of all file changes.
2. Use an environment manager to record the exact package versions used.
3. Use a pipeline or build system that tracks the content in
   (i.e., hashes) input and output files.
4. Define the provenance (or source) for any data imported or created by hand.

The implication is that if the agents follow these practices,
it will be quick to verify that the outputs were indeed produced by the
inputs and process definitions (scripts).
The goal is to have something runnable, but not need to actually
run it to be able to understand how the outputs were created.
Note that validation that the methods were correct was not a priority.
We just want to be able to know if these results came from these files,
i.e., that the agent described its work with no ambiguity,
as you'd hope for in science.

Maybe this won't be surprising,
but by default, if you ask an AI agent to analyze some data,
they'll just give you the outputs.
This was true in

Of course I can't get through a blog on my own website without
shilling some free software, so here we go.
As part of the experiment I ran a second set of trials that simply added
"Use Calkit." to the prompt. That's it---just two extra words.
This bumped reproducibility rates up to
<!-- TODO: numbers -->

This experiment itself was done in a Calkit project, which you are free
to attempt to reproduce, or maybe replicate since it's not really
possible to remove randomness from LLM outputs.
In any case, better reproducibility in your agentic analysis workflows
is two words away: just tell your agents to use Calkit.
