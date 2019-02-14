Overview of a "Story Compiler"
------------------------------

_Chris Pressey, Nov 12 2015_

This is an extremely simplified description of the story generator I'm working
on.  It glosses over most of the details, but hopefully provides an overview
of the architecture.  I've tried to write it for a general intermediate-programmer
audience; no knowledge of compiler construction is assumed.

### First, about the name ###

A compiler is a program which, typically, takes
program source code (almost always in a text file) as input, and produces
a file in some format that the computer can more easily execute.  Well-known
examples are the Java Compiler (`javac`) and the GNU C Compiler (`gcc`), but
in fact lots of programming language interpreters contain a compiler in them
somewhere.  (Javascript, for example, is compiled "just in time" in a web
browser before it's run.)

However, I've been calling this generator a "story compiler" _not_ because it works
like a typical compiler, but because a lot of its internal parts look a
lot like the internal parts of a typical compiler.  It works _sort of_ like a
compiler, but the analogy is sometimes strained.

So, when reading this, you can just forget about the "compiler" angle if you like.
It will probably be easier to think about, if you just think of it as a story generator.

### How the story is represented ###

The story, at any given point, is represented by a _tree_ where each tree
node can have any number of children.

Unfortunately, trees are difficult to draw in ASCII.  And recursive data
structures with references might not be everyone's cup of tea.

Luckily, there's a way to think about them and write them out that is usually
simpler: a tree is basically _a list that can contain other lists inside it_
(and those sublists can contain lists inside them, and so forth on down.)

So, this is a tree:

    [a, [b, c], d, [[e, f], g]]

At every point in the program, the story is represented by something that
looks like that.

### What we do with these trees ###

Inside the generator, we have a bunch of functions.  Each of them takes a
tree as input, and returns a slightly different tree.

The functions are often called back-to-back, one after the other, like

    tree = transform_tree_in_some_way(tree)
    tree = transform_tree_in_some_other_way(tree)
    tree = apply_yet_another_transformation(tree)

and we call this pattern a _pipeline_.  Each function call in it, we call
a _stage_.

This generator is basically one long pipeline.  Currently, it has about
a dozen stages.

(Note that, each time we call a function, we get a _new_ tree.  We don't
change the old tree, and in fact we do what we can to prevent it from being
changed — it's an _immutable_ data structure.  This is often less efficient
than changing a tree directly, but it is also often easier to reason about.)

This isn't the entire picture.  There is also a "database" of things —
characters, items, settings, and the like — that exists alongside the
pipeline.  Parts of the tree can refer to objects in this database.
But the pipeline is where most of the activity happens.

### Where do we begin? ###

No story is generated purely out of thin air.  You have to start with
_something_.  Because this generator works on trees, naturally, it starts
with a tree.

In principle, the "story compiler" could read this initial tree from a
text file (written in e.g. JSON or YAML), and it would probably be more
deserving of the name "compiler" if it did.  But, I only have a month,
so for expediency, the initial tree is hard-coded in the generator.

Early in my discussion thread, I mentioned the "null story":

> Once upon a time, they lived happily ever after.

The compiler starts with a tree representation which basically matches that.
It looks something like this:

    [IntroduceCharacters, *, CharactersConvalesce]

Think of the `*` as a placeholder for the parts of the story that aren't written yet.

### How this is turned into a story ###

One of the first stages of the pipeline is the "plot complicator", which takes
this initial tree and creates a new tree where every `*` is replaced by some subplot
that it picks out of a hat (more or less).  For example, after complication, the new tree might be

    [IntroduceCharacters, [JewelsStolen, *, JewelsRecovered, *], CharactersConvalesce]

If we want a fairly involved story, we don't have to run this stage just once,
we can run it many times.  And if all the subplots themselves contain `*`'s,
this process can continue for as long as you like.  Currently, it's run about
five times.

Once we're happy with how complex the plot is, there's a stage that takes that
final plot tree, removes any remaining `*`'s, and flattens it, producing a tree
like:

    [IntroduceCharacters, JewelsStolen, JewelsRecovered, CharactersConvalesce]

And from that, the generator can print out a fairly nice synopsis.

(Note that flattening a tree like this is a convenient thing to do at various
points in the pipeline.  Just because a list _can_ contain embedded sublists
doesn't mean it _has_ to.)

Then there's a stage that turns those plot developments into sequences of events.

This is actually a very murky area in the generator, and a lot of it is written
in an ad-hoc fashion, and I'm not happy about that... but for now, let's just
pretend it's simple.  Say it basically looks for particular plot developments,
and replaces them with particular sequences of events, like so:

    IntroduceCharacters → [DescribeBurglar, DescribeDetective]
    JewelsStolen → [BurglarTakesJewels, BurglarEscapes]
    JewelsRecovered → [DetectiveCatchesBurglar, DetectiveTakesJewels]
    CharactersConvalesce → [BurglarEscapes, DetectiveGoesHome]

So the resulting tree after this stage looks like:

    [
        [DescribeBurglar, DescribeDetective],
        [BurglarTakesJewels, BurglarEscapes],
        [DetectiveCatchesBurglar, DetectiveTakesJewels],
        [BurglarEscapes, DetectiveGoesHome],
    ]

Which is then flattened:

    [DescribeBurglar, DescribeDetective, BurglarTakesJewels, BurglarEscapes,
     DetectiveCatchesBurglar, DetectiveTakesJewels, BurglarEscapes, DetectiveGoesHome]

and then ultimately text is generated.  This part is a bit murky too, but for
simplicity, just assume that we go through the tree and for every event we see,
we print out a corresponding sentence:

> The burglar was a tall person.  The detective was a short person.  The burglar took the
> jewels.  The burglar escaped.  The detective caught the burglar.  The detective
> took the jewels.  The burglar escaped.  The detective went home.

And there we have a story.

And that is basically how this generator works, if we ignore all the messy details.

### What does a stage actually do? ###

Earlier I mentioned that a stage takes a tree and returns another tree, but that
might leave you wondering how the stage actually does that.

Well, a tree is a recursive data structure, so the easiest way to do that is to
write each stage as a recursive function.  If you're familiar with design patterns,
you may know this as a "visitor".  But if you're not comfortable with recursion,
this may be perplexing at first — it does take a while to wrap your head around it.

I'll give a simple example in pseudo-code.  Say we wanted to take a tree, and
return a new tree where all the events of a certain type have been removed.
(There are actually stages in this generator that do that.)  Say we want to
get rid of all events that involve the burglar, just before we write out the
story.  (We're going for a "Garfield minus Garfield" feel, I guess.)
We could write a stage like this:

    function remove_burglar_events(tree) {
        new_children = []  //  an empty list

        for each child in tree {
            if child is an event that involves the burglar {
                // do nothing!
            } else {
                new_child = remove_burglar_events(child)
                append new_child to new_children
            }
        }

        return new Tree(new_children)
    }

Notice how, in the `else` block, this function calls itself - that's the recursion.  We actually make many new trees, one for each subtree of the tree we're given, and we "glue" them back together to form the new tree that we return to the caller.

Most of the stages in this generator look more or less like that, only with
more complex logic in the middle part.
