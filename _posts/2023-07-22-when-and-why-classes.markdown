---
comments: true
layout: post
title: When and why to use classes (in Python anyway)
---

TL;DR: Classes are for encapsulating _long-lived_ application state.

Okay, so what does that mean?
State is data, like something you might keep in memory or a database,
and encapsulation means you put a wall around that state
and only let it be accessed through an interface
(methods and properties).
But what does long-lived mean?
This is hard to quantify,
but if your class instances are created and discarded after calling
one or two methods on them, they probably aren't long-lived.

But let's back up a second.
Why can class usage be problematic?
Firstly, let me admit that I don't like object-oriented programming.
I find it to be backwards, i.e., it has objects to encapsulate
state and have those objects mutate themselves.
It seems much more intuitive that the application should be the one in
charge, not the data.
That being said, nearly all applications will involve objects---I just don't
think it's all that helpful to have the objects manage themselves.

I have personally seen lots of class abuse.
I have even fallen prey to the "shiny new thing" pitfall when I first
learned about classes and assumed that's how all my code should be written.
So, this article is meant to help you avoid that trap.

Two videos helped snap me out of my class illusions:
1. TODO
2. TODO

## Concrete examples of worthwhile encapsulation of long-lived state

1. GUI applications. The components of a UI are essentially long-lived.
   They can be hidden, change color, store user input.
   I think these objects are quite intuitive to interact with like
   `button1.hide()` rather than `hide_button("button1")`.
2. Background threads that collect data, or maybe threads in general that
   constantly create new state. These seem very useful to encapsulate.
3. Machine learning models. Training a model creates state in order to make
   predictions. `model.predict(data)` seems pretty intuitive,
   though I'm not so sure about `model.fit(data)`,
   since we're having the instance mutate itself,
   and an untrained model isn't very useful.

## When not to use classes

1. To reduce duplicate code via inheritance. It is not commonly accepted that
   inheritance is problematic.
   I will make an exception if the inheritance happens in the
   same module, however,
   but I am also biased towards pure functions as a better way to avoid
   duplication.
   On the other hard, duplicate code isn't the end of the world if it's
   easy to understand.
2. To write procedures. If you are instantiating a class, calling one method,
   and only care about the result,
   you probably shouldn't use a class.

## Bonus application: Type hinting and validation

Pydantic.
This isn't long-lived state per se,
but Pydantic models are quite helpful to define data types
to be used throughout the application,
and these happen to be defined as classes.
I would avoid attaching too many methods to them, however,
following the principle of letting the application
handle the data instead of the data handling itself.

## Lastly, a word about complexity

Maybe the most important reason to avoid using classes is that
we want to minimize complexity,
and complexity comes from additional state in our application that is
not essential to the problem we're solving.
Complexity gets even worse when the state it mutable.
Since classes encapsulate state,
it logically follows that if you write lots of them,
you're potentially creating a lot of state in your application.
Python is especially bad for this because the `self` keyword gives one
a limitless dumping ground for mutable state.

## Old stuff below

```python
import foxes

states = foxes.input.states.Timeseries("timeseries_3000.csv.gz", ["WS", "WD","TI","RHO"])

mbook = foxes.ModelBook()

farm = foxes.WindFarm()
foxes.input.farm_layout.add_from_file(farm, "test_farm_67.csv", turbine_models=["NREL5MW"])

algo = foxes.algorithms.Downwind(mbook, farm, states, ["Jensen_linear_k007"])
farm_results = algo.calc_farm()

print(farm_results)
```

This example shows us creating lots of instances of classes,
tying them together in strange ways,
and only really calling one method that produces anything of interest
(`calc_farm`).

We create `mbook` without any input and pass it into another instantiation
of a class.

This could have simply been written as

```python
import foxes

farm_results = foxes.simulate_farm(
    states_fpath="timeseries_3000.csv.gz",
    layout_fpath="test_farm_67.csv",
    turbine_models=["NREL5MW"],
    algo="Jensen_linear_k007",
)
```

TODO: More, LoC, examples of usage, etc.

Fast-forward a decade or so, and now I'm at [WindESCo](https://windesco.com),
writing software that
processes much bigger sets of turbine data in many different ways.
My typical fallback is to write procedural code and pure functions,
because I personally find that the easiest to understand,
but we started playing around with writing our data processing pipelines as
classes using inheritance.
It seemed to work okay, and enabled us to define a generic procedure,
filling in the details by overriding methods or configuring parameters via
class attributes.
We could also bundle together visualization and processing together into
the classes,
potentially creating cohesion,
and maybe reducing repetition.

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
This also makes it easy to expose these function via REST API,
since all the parameters are already JSON-serializable.

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

Let's look at a trivial example to show how classes can lead to
unnecessary complexity.

Imagine our program is supposed to calculate the area of various shapes.
We could use classes.
But we see classes are only actually useful if the shapes data
is long-lived.

TODO: Add some bad examples.


## Other resources

- [Stop writing classes](https://www.youtube.com/watch?v=o9pEzgHorH0)
