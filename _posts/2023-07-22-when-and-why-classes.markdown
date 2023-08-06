---
comments: true
layout: post
title: When and why to use classes (in Python anyway)
---

I can almost remember when I first learned about object-oriented programming
(OOP) and classes in Python.
It was probably when I first wanted to build a desktop GUI app with PyQt,
where everything is a class, and I just followed the examples I saw
elsewhere, using `self` as needed without really knowing what it meant.
This [desktop GUI app](https://github.com/petebachant/TurbineDAQ)
was responsible for automating my experimental setup,
which towed a vertical-axis turbine down a tow tank while collecting
loads, torque, and wake flow data.

For processing data from my
[first experiment](https://github.com/UNH-CORE/RVAT-baseline),
I wrote purely procedural code, since I was weening
myself off of MATLAB at the time, which at that point didn't have any
OOP capabilities, as far as I know.
But for the [next](https://github.com/UNH-CORE/RVAT-Re-dep),
I had this idea that I should be writing in the OOP style,
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
Maybe I should start with what isn't the purpose of a class.
In his video above Brian Will states this very well: classes should not be
"doers". This is a pattern I've seen a bit in software written by people like
me ("real life", e.g., civil, mechanical, chemical engineers who turned to
software without formal software engineering training).
Typically it involves creating a doer object, calling one method on it,
and throwing it away. For example:

```python
problem = NavierStokes()
solver = EquationSolver(tol=5)
solution = solver.solve(problem)
```

The code above fictitiously solves the Navier--Stokes equations,
forcing the user to instantiate two different objects along the way,
and probably throw them out or ignore them,
keeping what they really care about: the `solution`.
In Python, this could have simply been written as:

```python
solution = solve(problem="navier-stokes", tol=5)
```

Side note: We could have had the user pass in an instance of a `Problem`
class, but I typically like function arguments to be primitive types, so would
point the literal `"navier-stokes"` to that class, if it were written that
way, but it could also point to a function.
Doing it this way also means we don't force the user to import or know anything
about `NavierStokes`, because why should they.

Now this leaves us with the question what is the type of `solution`.
If we follow the principle of simplicity, we could simply make it a `dict`
or a NumPy array,
but a `solution` probably represents something that could deserve to be a class,
since it represents important long-lived state that is likely
irrelevant to much of the rest of the application.
We could have something like:

```python
class Solution:
    def __init__(self, data):
        self.data = data
    def visualize(self):
        ...
    def write(self):
        ...
    def load(self):
        ...
```

In this example we are now tying some actions to `Solution` by using OOP.
This might be easier than something like:

```python
from visualization import visualize

visualize(solution)
```

So, a class should not be a doer, but a class _can be_
a container for long-lived state
that is irrelevant to the rest of the application.
That last rule is an important one, which we may actually be breaking.
If this Python module or package we're working on is truly
dedicated to solving and visualizing solutions, using the module itself as
the main object could be just as easy to understand:

```python
import mysolverpackage as ms

solution = ms.solve(...)
ms.visualize_solution(solution)
ms.write_solution(solution)
```

In this case, `solution` could still be a fairly primitive type, i.e.,
a `dict`, `array`, or even Pandas `DataFrame`, with a structure or schema
that is understood by the rest of the application.
One benefit to doing things this way is that reading and writing can be
simple with built-in serialization libraries, e.g., `json`
(`json.dumps(Solution())` would fail without some additional code).

Using OOP for important application data has this strange irrationality or
backwardness.
Should the application be manipulating the data or should the data be
manipulating itself?
The latter feels wrong, and this is described well by
[this article](https://andreidascalu.medium.com/i-dont-like-object-oriented-programming-anymore-d38fa9ed3a77).
To go back to our first example, should a data collection run from our
experiment process itself, or is the application processing the data from
that run.

Another way to think about a class is as a custom, more exotic (complex!),
data type.
I'd argue that at the very least one shouldn't create a class for the
first iteration of a software project or feature.
If our project evolves to have many different _types_ of solutions,
equations, or solver algorithms,
then maybe a OOP makes sense,
but overall, hiding them as much as possible is also a preference of mine.
Have external code point to these using primitive types rather than forcing
them to know anything about class names, how to instantiate them, etc.

Another reason to avoid using classes in Python is that they essentially
become a dumping ground for limitless mutable state through the `self` keyword.
Moseley and Marks note that a primary source of complexity in software is
state, and mutable state is more complex than immutable.
If we're using a `Solution` class in our program, there is nothing preventing
anything that's using that class from mutating an instance at any time.

```python
s = Solution()
s.data = 5
s.other_data = 6
```

We could protect `data` by making it a... protected... attribute
(with a preceding underscore) and defining access to is through the
`property` decorator, but there is nothing preventing us from adding
`other_data` at any point, and even `_data` could be mutated at will.
So, is this custom data type giving us essential complexity? Probably not.

A good way to avoid mutating custom data types in Python is to use
the `dataclass` decorator.

TODO: Avoid inheritance.

## Hearing out the other side

I have heard that OOP is absolutely crucial in large enterprise applications
to avoid duplicated or strongly couples code, which can enable development
teams to be decoupled from each other.
Setting aside the question of whether or not "large" applications should even
exist (are they essential complexity?),
are classes really the only way to achieve code reuse and decoupling?
Firstly, using inheritance to avoid duplications is already problematic.
Modules of pure functions can do the same thing,
achieving polymorphism and consistent interfaces.
Pydantic can help with type checking arguments to these pure functions.
If you know a problem that is truly easier to deduplicate/decouple with
classes instead of pure functions, please let me know.

## Summary and conclusions

Any application will have objects that it deals with in order to model
its relationships to the real world.
The main question is whether or not you want the objects to be in charge
of managing themselves or if the application should be responsible for
managing the objects.
In my opinion, the application should manage the data, not the other way
around, so OOP should not be used for the main application logic.
However, classes can be useful in some cases.

To wrap things up, I would first say to avoid writing classes as much as
possible in Python.
The first version of your app should probably not define any classes.

If after things are working and you notice that there is a bunch of duplicated
long-lived state, then refactoring to use a class can make sense.
However, this class should be named after and represent state (data),
not actions.
Do not write doer classes.

Avoid initializing and mutating classes all over your application.
Write a function to instantiate.

Valid use cases are:

- Defining schemas that are thin wrappers over primitive types.
- Encapsulating long-lived state that would be inefficient to recreate like
  database connections.
- Encapsulating long-lived state that is irrelevant in other parts of the
  application.
  For example, a trained machine learning model.
  The weights, or tree, or regression coefficients, etc.,
  are probably only necessary to make predictions,
  so they can be hidden inside of a class.
  A DataFrame, which has columns and values that don't make sense
  outside the context of the dataset itself.

You probably won't use classes to do true OOP (message passing).
If you do, you'll probably run into confusion about what state should be
encapsulated by what class,
and end up coupling them to share state anyway.

If you're using classes in a way where they are short-lived,
you probably should not be,
because you're probably just using classes to write procedures.

If you're using classes in Python to reuse code via inheritance you
probably should not be.

Classes should have as few methods as possible. The app should be manipulating
the data, rather than telling the data to mutate itself.

ORM?
