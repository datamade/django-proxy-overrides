Allow overriding fields on Proxy models.

Mostly, you won't want to do this. However, I did have a situation where it would
be useful, mainly for reducing the numbers of queries I was having to run.


I've started using `Proxy` models in some code for handling specialisation: basically,
the data for each subclass is in the same shape. This is mainly because I'm storing a
handful of regular fields, but then a `JSON` object containing other stuff that is
possibly only relevant to a single subclass.

In hindsight, I'd probably use proper multi-table inheritance, but it's a bit late for
that right now.

So, there is one main model that is subclassed in every instance. In addition, there are
several other models that will probably be subclassed if they are relevant to the case
for which the master model is subclassed. Each of these models contains a relation back
to the master model.

If you subclass one of these other models, and then traverse the related link, you'll get
back the master superclass, when in actuality, you want the subclass. Similarly, if you
instantiate one of the master subclasses, and get the related other objects, you want the
related subclass, but you'll get the superclass.

Perhaps code will explain:

