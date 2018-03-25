---
title: So What is Type Variance?
---

Some of us may have heard the terms **covariant** and **contravariant** get
tossed around in discussions about typing in programming languages.  What do
these things mean and why are they important?

To set the context, let's look at some simple examples of code to warm up our
intuitions.  We have a code snippet below that might look like something you
could see as part of a parsing library^[It's common to use animal analogies
when illustrating these concepts but we're opting for something a bit more
meaningful here.]:

```python
from typing import Iterable


class Node:
    def __init__(self, result):
        self.result = result

    @property
    def value(self):
        return self.result


class Integer(Node):
    @property
    def value(self):
        return int(self.result)


def print_values(nodes: Iterable[Node]):
    for node in nodes:
        print(node.value)


int_nodes = [Integer('123'), Integer('234')]


# Will this type check?
print_values(int_nodes)
```

Since Python 3.5, the `typing` module includes a number of classes which are
useful for type annotation and checking.  The annotation is done via the colon
and arrow syntax seen above (available in any version of Python 3).  The
checking can be done with the popular [mypy](http://mypy-lang.org/) library.

In the above code snippet, we've got a few things.  There's a base class,
`Node`, which we can imagine might be used to hold the result of some parsing
operation.  There's also a sub class, `Integer`, which might be used to hold
and process the result of parsing a integer literal.  The question is this:
will the final line type check?

The definition of `print_values` indicates that the function is expecting to be
given some kind of iterable value containing `Node` instances.  We're passing
the contents of `int_nodes`, which contains an iterable of `Integer` instances,
to `print_values`.  Will this work?  The answer is yes.
