---
comments: true
layout: post
title: When and why to use classes (in Python anyway)
---

I can almost remember when I first learned about object-oriented programming
and classes in Python.
It was probably when I first wanted to build a desktop GUI app with PyQt,
where everything is a class, and I just followed the examples I saw
elsewhere, using `self` as needed without really knowing what it meant.
This [desktop GUI app](https://github.com/petebachant/TurbineDAQ)
was responsible for automating my experimental setup,
which towed a vertical-axis turbine down a tow tank while collecting
loads, torque, and wake flow data.

For my
[first experiment](https://github.com/UNH-CORE/RVAT-baseline),
I wrote purely procedural code, since I was weening
myself off of MATLAB at the time, which at that point didn't have any
OOP capabilities, as far as I know.
But for the [next](https://github.com/UNH-CORE/RVAT-Re-dep),
I had this idea that I should be writing in OOP,
because, I dunno, it was an option?

Anyway, I am going to do something that usually induces plenty of cringe
and look at some old code, analyzing these two projects to see if
using classes was truly a good idea in the later one.
Essentially, the purpose of both of these projects was to reduce the data
to some aggregates and create some plots from them.
At the top of each lived a `process.py` and a `plot.py` script, which were
intended to be the main command line interface to do the work.

In the older project, `process.py` simply looked like:

```python
import pyrvatbl.processing as pr

if __name__ == "__main__":
    pr.batchperf()
    pr.batchwake()
```

So, we imported the local processing module `pyrvatbl.processing`, and called
two functions out of it, processing the performance data, then the wake data.


TODO: More, LoC, examples of usage, etc.


Fast-forward a decade or so, and now I'm at [WindESCo](https://windesco.com),
writing software that
processes much bigger sets of turbine data in many different ways.
My typical fallback is to write procedural code and pure functions, because
I personally find that the easiest to understand,
but we started playing around with writing our data processing algorithms as
classes using inheritance.
It seemed to work okay, and enabled us to define a generic procedure,
filling in the details by overriding methods or configuring parameters via
class attributes.

However, I then stumbled upon this video, and it made me question what we
were doing:

<iframe width="560" height="315" src="https://www.youtube.com/embed/QM1iUe6IofM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

What followed was an existential rabbit hole with the need to answer the
question: Should OOP ever be used, and if so, when and why?
Along the way, the concept of complexity arose,
namely that it should be
[avoided like the plague](https://github.com/papers-we-love/papers-we-love/blob/main/design/out-of-the-tar-pit.pdf).

This really resonated with me.
I had always felt the need to write software as simply as possible for my
dumb future self out of laziness.
I had sometimes felt a little guilty about this.
I'd see someone else's apparently complex code and feel
like I wasn't good enough to write complex things.
I mean, sure, I was probably working on easy problems, which
deserve simple solutions,
but if you follow the principles in Moseley and Marks' paper above,
the goals for your software, business, project, dare I say life,
should also be as simply as
possible, i.e., retaining only "essential complexity."

So, what is the purpose of a class?
