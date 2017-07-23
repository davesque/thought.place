---
title: Towards an Understanding of Search Engines
published: 2017-07-22T09:00:00-0400
---

## Developing an Intuition

Imagine a robot which starts on some random web page on the internet.  The
robot clicks a random link on this page and is led to a second page.  On this
second page, the robot clicks another random link and is led to a third page
and so on.  We could imagine that, if this process continued on forever, the
robot might eventually visit every page on the web.^[Attentive readers may
realize that this is not entirely true.  For instance, if the robot navigated
to a page with no links, it would get stuck.  For now, let's assume the robot
*will* visit every page and that it won't run into anything that would cause it
to get stuck in a certain pattern.]  During this journey, our robot would
probably find itself revisiting certain pages again and again.  After all, the
web has a lot of popular sites that everyone visits and that are linked to from
many places.  Such sites could be ones like *wikipedia.com* or *facebook.com*.
These sites that our robot finds often are the "important" sites on the
internet.

This sense of importance that we've just described generally characterizes the
way that search engines rank and index web pages on the internet.  We can
describe the process in a few steps:

* We begin on some random page.
* We take an infinite, random walk of the web and record the frequencies with
  which we encounter every page that we come across.
* We use these frequencies to figure out the likelihood of ending up at each
  page after clicking a link during any step of our walk.
* We consider these likelihoods to be the ranks of the pages we found (i.e.
  pages with higher likelihoods of being visited are considered to be more
  important).

Let's look at some diagrams to get a better sense of what we're talking about.
Below, we'll consider a collection of "mini" internets that have only a few
pages.  Pages will be represented by circles with numbers in the center and
links will be arrows connecting the circles.  For example, an arrow pointing
from one circle to another will represent a link going from one page to
another.

Now, imagining our robot and its random browsing again, if the web looked like
figure 1, could we guess the likelihood that the robot would find itself on
page 1 at any given time during an infinite walk?

<figure>
  \begin{tikzpicture}[scale=1.5, transform shape]
    \definecolor{nodecolor}{RGB}{204,204,255}
    \tikzset{vertex/.style = {shape=circle,fill=nodecolor,draw,minimum size=.3in}}
    \tikzset{edge/.style = {->,> = latex'}}

    \node[vertex] (1) at (0,2) {1};
    \node[vertex] (2) at (-1.5,0) {2};
    \node[vertex] (3) at (1.5,0) {3};

    \draw[edge] (1) to (2);
    \draw[edge] (2) to (3);
    \draw[edge] (3) to (1);
  \end{tikzpicture}

  <figcaption>Figure 1: A tiny world-wide web.</figcaption>
</figure>

In this case, we would probably say that the likelihood is 1 in 3.  This
follows from the fact that each page links to the next in a very regular way.
So it's reasonable to say that each page's likelihood of being encountered is
the same.  What if we added a link from page 2 back to page 1 as seen in figure
2?  Would page 1's likelihood change?

<figure>
  \begin{tikzpicture}[scale=1.5, transform shape]
    \definecolor{nodecolor}{RGB}{204,204,255}
    \tikzset{vertex/.style = {shape=circle,fill=nodecolor,draw,minimum size=.3in}}
    \tikzset{edge/.style = {->,> = latex'}}

    \node[vertex] (1) at (0,2) {1};
    \node[vertex] (2) at (-1.5,0) {2};
    \node[vertex] (3) at (1.5,0) {3};

    \draw[edge] (1) to[bend left] (2);
    \draw[edge] (2) to[bend left] (1);
    \draw[edge] (2) to (3);
    \draw[edge] (3) to (1);
  \end{tikzpicture}

  <figcaption>Figure 2: A web with more links.</figcaption>
</figure>

Now things seem a bit less intuitive.  Page 1 seems pretty important (since it
has the highest number of links that point to it), but how can we judge the
importance of pages 2 and 3?  We also have to admit that the whole notion of an
"infinite" walk sounds a bit crazy and impractical.  How could we actually *do*
that?  Wouldn't that require an infinite amount of time?  Furthermore, how do
we handle the case when our robot finds a page with no links to other pages as
seen with page 1 in figure 3?

<figure>
  \begin{tikzpicture}[scale=1.5, transform shape]
    \definecolor{nodecolor}{RGB}{204,204,255}
    \tikzset{vertex/.style = {shape=circle,fill=nodecolor,draw,minimum size=.3in}}
    \tikzset{edge/.style = {->,> = latex'}}

    \node[vertex] (1) at (0,2) {1};
    \node[vertex] (2) at (-1.5,0) {2};
    \node[vertex] (3) at (1.5,0) {3};

    \draw[edge] (2) to (1);
    \draw[edge] (2) to (3);
    \draw[edge] (3) to (1);
  \end{tikzpicture}

  <figcaption>Figure 3: A web with a "black hole".</figcaption>
</figure>

What if our robot begins in some part of the web which doesn't refer to any
pages outside of itself (i.e. the robot gets stuck not just on a certain page
but in a certain part of the web as seen in figure 4)?

<figure>
  \begin{tikzpicture}[scale=1.5, transform shape]
    \definecolor{nodecolor}{RGB}{204,204,255}
    \tikzset{vertex/.style = {shape=circle,fill=nodecolor,draw,minimum size=.3in}}
    \tikzset{edge/.style = {->,> = latex'}}

    \node[vertex] (1) at (-1,1.5) {1};
    \node[vertex] (2) at (-1,0) {2};
    \node[vertex] (3) at (1,1.5) {3};
    \node[vertex] (4) at (1,0) {4};

    \draw[edge] (1) to[bend left] (2);
    \draw[edge] (2) to[bend left] (1);
    \draw[edge] (3) to[bend left] (4);
    \draw[edge] (4) to[bend left] (3);
  \end{tikzpicture}

  <figcaption>Figure 4: A web with isolated sections.</figcaption>
</figure>

To answer all these questions, we need to find a more systematic way to talk
about this problem^[The algorithm we've described in this first section is, in
fact, how an early version of Google's very own PageRank algorithm worked.  So,
at one point in recent history, this algorithm was poised to make billions of
dollars.  The rest of this article will touch on more of the details of the
PageRank algorithm.].

## A More Systematic Approach

### Overview

First, let's introduce some basic terminology.  During the rest of this
article, we're going to use two related concepts in our discussion: the
concepts of a **state machine** and a **graph**.  For our purposes, these two
terms are equivalent.  A **state machines** is composed of a number of states
in addition to a number transitions between those states.  In our diagrams from
the first section, the circles were the states and the arrows were the
transitions.  Likewise, a **graph** is composed of a number of vertices and a
number of edges.  In the same diagrams, the circles were the vertices and the
arrows were the edges.  We can think of the web as both a state machine *and* a
graph.

Now that we've hopefully clarified some things, let's think of the web as a
state machine.  Think back to our random walker.  When our walker comes to a
new page (when it transitions into a new state), it has to randomly choose
which link to click (choose the next state into which it should transition).

Let's say that each link has an equal probability of being clicked.  This gives
us the following equation for the probability of clicking a link during any
step of our walk:

\begin{align*}
  \text{probability of clicking link $x$} = \frac{1}{\text{total \# of links on the page where $x$ is found}}
\end{align*}

We're beginning to see that we're not just talking about a state machine, but a
*probabilistic* one &mdash; that is, a state machine which randomly transitions
between states based on some set of probabilities for each state.  Such an idea
is also sometimes referred to as a **Markov chain**^[A Markov chain more
generally describes the idea of a sequence of events which is "memoryless"
&mdash; that is, when the likelihood of future events in some process can be
determined entirely from the current situation or state.  In our case, this
term is appropriate since our random walker basically uses only the links on
its current page to choose where to go.  We say "basically" here because there
are a few more details to the situation which we'll get to later.].

Let's visualize this.  We imagine that our walker has come to page 1 and is now
picking which page to go to from there.  It gives each link on page 1 an equal
probability of being clicked as seen in figure 5:

<figure>
  \begin{tikzpicture}[->,>=latex',scale=1.5,transform shape]
    \definecolor{nodecolor}{RGB}{204,204,255}
    \tikzset{vertex/.style = {shape=circle,fill=nodecolor,draw,minimum size=.3in}}

    \node[vertex] (1) at (0,0) {1};
    \node[vertex] (2) at (3,1.5) {2};
    \node[vertex] (3) at (3,0) {3};
    \node[vertex] (4) at (3,-1.5) {4};

    \path (1) edge node[above] {$\frac{1}{3}$} (2);
    \path (1) edge node[above] {$\frac{1}{3}$} (3);
    \path (1) edge node[above] {$\frac{1}{3}$} (4);
  \end{tikzpicture}

  <figcaption>Figure 5: State machine with transition probabilities.</figcaption>
</figure>

The total number of links on page 1 is 3 so the probability of clicking any one
of those links is $1/3$.  To illustrate this idea further, let's annotate
figure 2 from the first section with some probabilities.  In figure 6, we see
this annotated version of figure 2 where each link from page 2 has probability
$1/2$ of being clicked.  The link from page 1 has probability 1 (a 100% chance)
of being clicked as does the link from page 3:

<figure>
  \begin{tikzpicture}[->,>=latex',scale=1.5,transform shape]
    \definecolor{nodecolor}{RGB}{204,204,255}
    \tikzset{vertex/.style = {shape=circle,fill=nodecolor,draw,minimum size=.3in}}

    \node[vertex] (1) at (0,2) {1};
    \node[vertex] (2) at (-1.5,0) {2};
    \node[vertex] (3) at (1.5,0) {3};

    \path (1) edge[bend left] node[below right] {1} (2);
    \path (2) edge[bend left] node[above left] {$\frac{1}{2}$} (1);
    \path (2) edge node[below] {$\frac{1}{2}$} (3);
    \path (3) edge node[above right] {1} (1);
  \end{tikzpicture}

  <figcaption>Figure 6: Another state machine with transition probabilities.</figcaption>
</figure>

Since we're trying to be systematic, we need a way to represent this process
mathematically.  As it turns out, there is a way to do this using vectors and
matrices.

### Using Vectors and Matrices

From here on out, we're going to assume the reader has some familiarity with
a number of concepts from linear algebra including the concepts of a **vector**
and a **matrix**.  Khan Academy has [a good
course](https://www.khanacademy.org/math/linear-algebra) for anyone interested
in doing some learning on these subjects.

In linear algebra, we represent probabilistic state machines using **transition
matrices**.  A **transition matrix** is a matrix which represents the vertices
and edges in a graph, giving a probability or weight to each edge.  It is
defined in terms of the **adjacency matrix** of a graph as well as the graph's
**degree matrix**.

A graph's adjacency matrix $A$ is defined as follows:

\begin{equation*}
A_{ij} = \begin{cases}
  1\ \text{if vertex $i$ links to vertex $j$} \\
  0\ \text{otherwise}
\end{cases}
\end{equation*}

As we can see in the definition above, an adjacency matrix encodes the edges in
a graph as well as each edge's direction.  This gives us the following
adjacency matrix for the graph seen in figure 6:

\begin{equation*}
A = \begin{bmatrix}
  0 & 1 & 0 \\
  1 & 0 & 1 \\
  1 & 0 & 0
\end{bmatrix}
\end{equation*}

Now for the degree matrix $D$.  It's defined as follows:

\begin{equation*}
D_{ij} = \begin{cases}
  \text{\# of links leaving vertex $i$ if $i = j$} \\
  0\ \text{otherwise}
\end{cases}
\end{equation*}

A degree matrix encodes the number of edges pointing away from each vertex in a
graph.  For our graph, that looks like this:

\begin{equation*}
D = \M{%
  1 & 0 & 0 \\
  0 & 2 & 0 \\
  0 & 0 & 1
}
\end{equation*}

After all this, we can finally define our transition matrix as follows:

\begin{align*}
  T &= A^T D^{-1} \\
    &= \M{%
      0 & 1 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    } \M{%
      1 & 0 & 0 \\
      0 & \sfrac{1}{2} & 0 \\
      0 & 0 & 1
    } \\
    &= \M{%
      0 & \sfrac{1}{2} & 1 \\
      1 & 0 & 0 \\
      0 & \sfrac{1}{2} & 0
    }
\end{align*}

What are we seeing here?  In column 1 of $T$, we see 1 in the second row and
0's in the other rows.  This means there's a 100% probability of moving to page
2 from page 1.  Therefore, column 1 corresponds to the probabilities of
transitioning from page 1 to any other page.  Likewise, column 2 corresponds to
the transition probabilities for page 2 and so on.

Now, how do we actually *use* this transition matrix which represents our state
machine?  How do we actually *run* the machine?  The process is detailed below:

\begin{align}
  \text{next state vector} &= T \times \text{previous or initial state vector} \\
  \B{s}_n &= T \B{s}_{n - 1} \\
  \B{s}_1 &= T \B{s}_0 \\
  \implies \M{0 \\ 1 \\ 0} &= \M{%
    0 & \sfrac{1}{2} & 1 \\
    1 & 0 & 0 \\
    0 & \sfrac{1}{2} & 0
  } \M{1 \\ 0 \\ 0}
\end{align}

In equations 1 and 2 above, the transition matrix $T$ multiplies with some
state vector to perform the action of transitioning to the next state.
Concretely, in equation 4, we begin our random walker on page 1 (state 1) by
choosing an initial state vector with 1 as its first element as seen on the
right-hand side.  After the matrix-vector multiplication, we see that the 1 has
moved into the second slot on the left-side.  This means that our walker ended
up on page 2 after one "random" step.^[In this case, it was not exactly random
since page 1 links to page 2 and nothing else.]  Let's see what happens if we
continue this process.  We now have a new state vector $\mathbf{s}_1$.  We feed
$\mathbf{s}_1$ back into the transition equation to get the next state vector
$\mathbf{s}_2$:

\begin{align*}
  \B{s}_2 &= T \B{s}_1 \\
  \implies \M{\sfrac{1}{2} \\ 0 \\ \sfrac{1}{2}} &= \M{%
    0 & \sfrac{1}{2} & 1 \\
    1 & 0 & 0 \\
    0 & \sfrac{1}{2} & 0
  } \M{0 \\ 1 \\ 0}
\end{align*}

Now, looking at the value of $\mathbf{s}_2$, we see there's a 50% probability
that we're on page 1 and a 50% probability that we're on page 3.  Put another
way, there was an equal chance that our random walker went from page 2 back to
page 1 or from page 2 on to page 3.

Let's continue this process for several more steps:

\begin{align*}
  \B{s}_3 &= \M{%
    0.5 \\
    0.5 \\
    0
  } = \M{%
    0 & 0.5 & 1 \\
    1 & 0 & 0 \\
    0 & 0.5 & 0
  } \M{%
    0.5 \\
    0 \\
    0.5
  } \\
  \B{s}_4 &= \M{%
    0.25 \\
    0.5 \\
    0.25
  } = T \M{%
    0.5 \\
    0.5 \\
    0
  } \\
  \B{s}_5 &= \M{%
    0.5 \\
    0.25 \\
    0.25
  } = T \M{%
    0.25 \\
    0.5 \\
    0.25
  } \\
  \B{s}_6 &= \M{%
    0.375 \\
    0.5 \\
    0.125
  } = T \M{%
    0.5 \\
    0.25 \\
    0.25
  } \\
  \B{s}_7 &= \M{%
    0.375 \\
    0.375 \\
    0.25
  } = T \M{%
    0.375 \\
    0.5 \\
    0.125
  } \\
  \B{s}_8 &= \M{%
    0.4375 \\
    0.375 \\
    0.1875
  } = T \M{%
    0.375 \\
    0.375 \\
    0.25
  } \\
  \B{s}_9 &= \M{%
    0.375 \\
    0.4375 \\
    0.1875
  } = T \M{%
    0.4375 \\
    0.375 \\
    0.1875
  } \\
  \B{s}_{10} &= \M{%
    0.40625 \\
    0.375 \\
    0.21875
  } = T \M{%
    0.375 \\
    0.4375 \\
    0.1875
  } \\
  \B{s}_{11} &= \M{%
    0.40625 \\
    0.40625 \\
    0.1875
  } = T \M{%
    0.40625 \\
    0.375 \\
    0.21875
  } \\
  \vdots \\
  \B{s}_{100} &= \M{%
    0.4 \\
    0.4 \\
    0.2
  } = T \B{s}_{99} \\
  \B{s}_{101} &= \M{%
    0.4 \\
    0.4 \\
    0.2
  } = T \M{%
    0.4 \\
    0.4 \\
    0.2
  } \\
  \B{s}_{102} &= \M{%
    0.4 \\
    0.4 \\
    0.2
  } = T \M{%
    0.4 \\
    0.4 \\
    0.2
  } \\
  \vdots
\end{align*}

Curious.  It appears as though our state vectors stabilized and are no longer
changing as we perform transitions.  If we examine the state vectors past
$\mathbf{s}_6$, we can see that our vectors were already beginning to approach
this stable state.  So what does this mean?

Well, we've actually ended up with a vector which "ranks" the pages in our
miniature web (i.e. a [PageRank](https://en.wikipedia.org/wiki/PageRank)
vector).  The first element in the vector is $0.4$ which means that, during an
infinite walk, we have a 4 in 10 chance of landing on page 1 after each step.
The second element is $0.4$ which means that the same is true for page 2.  Page
3 only has a 2 in 10 chance of being encountered during each step of the walk.

## Edge Cases

### Dangling Vertices

So are we done?  Did we come up with a perfect approach to this problem?  Not
quite.  As mentioned before, what if the walker hits a page with no links?

\begin{align*}
  \M{0 \\ 0 \\ 0} &= \M{%
  0 & \sfrac{1}{2} & 1 \\
  0 & 0 & 0 \\
  0 & \sfrac{1}{2} & 0 \\
  } \M{1 \\ 0 \\ 0}
\end{align*}

Right away, we hit a null state (i.e. a state vector whose elements are all
zero).  Any further state transitions will also lead to this null state.  So
how do we fix this?  One approach, which we'll use, is to simply set every
value in the "page 1 column" to $1/n$ where $n$ is the total number of pages in
our graph.

\begin{align*}
  \M{%
  \sfrac{1}{3} \\
  \sfrac{1}{3} \\
  \sfrac{1}{3}
  } &= \M{%
  \sfrac{1}{3} & \sfrac{1}{2} & 1 \\
  \sfrac{1}{3} & 0 & 0 \\
  \sfrac{1}{3} & \sfrac{1}{2} & 0 \\
  } \M{%
  1 \\
  0 \\
  0
  }
\end{align*}

This makes some intuitive sense.  If we imagine a person browsing the web
coming to a page with no links, would we say that they're stuck on that page?
No.  They probably just think of some other page to go to.  We might say that
this idea is represented in the act of changing any zero columns to sets of
equal probabilities.

### Dangling Sets of Vertices and Circular Linking

What if our walker wanders into some corner of the internet that doesn't
reference anything outside of itself?  Maybe such an area could be an online
manual that only links to other sections in the same manual.  The walker would
get stuck there, endlessly flipping between manual pages.  Also, what if the
walker happens upon a set of pages that link to each other in a perfectly
circular fashion as seen in figure 1 from the first section?  This would
present a mathematical problem.  If our initial state vector began on one of
those pages, the 1 element would just move between positions and the vector
would never stabilize.  Both of these problems are seen with the mini web in
figure 4.  We give the transition matrix for this web below multiplied a few
times with a possible state vector:

\begin{align*}
  \M{0 \\ 1 \\ 0 \\ 0} &= \M{%
  0 & 1 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 1 \\
  0 & 0 & 1 & 0
  } \M{1 \\ 0 \\ 0 \\ 0} \\
  \M{1 \\ 0 \\ 0 \\ 0} &= \M{%
  0 & 1 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 1 \\
  0 & 0 & 1 & 0
  } \M{0 \\ 1 \\ 0 \\ 0} \\
  \M{0 \\ 1 \\ 0 \\ 0} &= \M{%
  0 & 1 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 1 \\
  0 & 0 & 1 & 0
  } \M{1 \\ 0 \\ 0 \\ 0} \\
  \M{1 \\ 0 \\ 0 \\ 0} &= \M{%
  0 & 1 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 1 \\
  0 & 0 & 1 & 0
  } \M{0 \\ 1 \\ 0 \\ 0} \\
  \vdots
\end{align*}

We can see the state vector alternating and never stabilizing.  Also, the slots
in the state vector which correspond to pages 3 and 4 are zero.  However, this
doesn't reflect the fact that those pages are linked to from somewhere and
should have a rank greater than zero.  How do we fix this?

Let's ask our intuition again.  What would a person do if they found themselves
roaming around in a cyclic part of the web?  They would probably just choose
some other page to visit.  In fact, there's probably always a small chance they
will suddenly get bored, decide to stop clicking links, and simply navigate to
a random page they think of off the top of their head.

We can represent this idea mathematically:

\begin{align*}
  G &= (1 - p) T + \frac{p}{n} \mathds{1} \mathds{1}^T
\end{align*}

What do we have here?  We have an outer product of $\mathbb{1}$ vectors which will
become an $n \times n$ matrix of ones ($n$ being the number of pages in our
internet).  This matrix of ones is multiplied by a scalar $p/n$.  We've already
defined $n$.  We say that the value $p$ is a "tuning" probability that
indicates how likely our walker is during any given step to randomly jump to
any page in our internet.  By multiplying $p/n$ with a matrix of all ones, we
get a tuning matrix with our tuning probability $p$ evenly divided across all
elements.  We also multiply our original transition matrix $T$ by the
probabilistic complement of $p$ (which is $1 - p$) and sum it with the tuning
matrix.

This gives us a matrix $G$ which is a new version of $T$ which has been
slightly redistributed according to our tuning probability.  Now, during any
step of our walk, the walker might jump to any other page, but it is more
likely to follow the links present on each page.

Let's calculate $G$ using the $4 \times 4$ transition matrix above (with the
cyclic behavior) and a tuning probability of $1/100$:

\begin{align*}
  G &= (1 - p) T + \frac{p}{n} \mathds{1} \mathds{1}^T \\
  &= (1 - \sfrac{1}{100}) \begin{bmatrix}
    0 & 1 & 0 & 0 \\
    1 & 0 & 0 & 0 \\
    0 & 0 & 0 & 1 \\
    0 & 0 & 1 & 0
  \end{bmatrix} +
  \frac{\sfrac{1}{100}}{4} \begin{bmatrix}
    1 & 1 & 1 & 1 \\
    1 & 1 & 1 & 1 \\
    1 & 1 & 1 & 1 \\
    1 & 1 & 1 & 1
  \end{bmatrix} \\
  &= \frac{99}{100} \begin{bmatrix}
    0 & 1 & 0 & 0 \\
    1 & 0 & 0 & 0 \\
    0 & 0 & 0 & 1 \\
    0 & 0 & 1 & 0
  \end{bmatrix} +
  \frac{1}{400} \begin{bmatrix}
    1 & 1 & 1 & 1 \\
    1 & 1 & 1 & 1 \\
    1 & 1 & 1 & 1 \\
    1 & 1 & 1 & 1
  \end{bmatrix} \\
  &= \begin{bmatrix}
    0 & \sfrac{99}{100} & 0 & 0 \\
    \sfrac{99}{100} & 0 & 0 & 0 \\
    0 & 0 & 0 & \sfrac{99}{100} \\
    0 & 0 & \sfrac{99}{100} & 0
  \end{bmatrix} +
  \begin{bmatrix}
    \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} \\
    \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} \\
    \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} \\
    \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400}
  \end{bmatrix} \\
  &= \begin{bmatrix}
    \sfrac{1}{400} & \sfrac{397}{400} & \sfrac{1}{400} & \sfrac{1}{400} \\
    \sfrac{397}{400} & \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} \\
    \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{397}{400} \\
    \sfrac{1}{400} & \sfrac{1}{400} & \sfrac{397}{400} & \sfrac{1}{400}
  \end{bmatrix}
\end{align*}

We can see that every page now has a slight probability of being visited even
if there were no links to it in the original graph.  Also, every column in the
matrix still sums to 1 and correctly represents a probability distribution.
Using this transition matrix, the walker will eventually navigate to every
page.

## Eigenvectors and Eigenvalues

In linear algebra, we say that a vector $\mathbf{x}$ is an **eigenvector** of a
matrix $A$ if the following equation holds true:

\begin{align*}
  A \B x &= \lambda \B x && \text{where $\lambda$ is some constant value}
\end{align*}

This says that, after transforming the vector $\mathbf{x}$ using the matrix
$A$, the result is simply a scalar multiple of $\mathbf{x}$.  That multiple,
$\lambda$, is the **eigenvalue** which corresponds to the eigenvector
$\mathbf{x}$.  These complementary ideas of eigenvectors and eigenvalues are
central to the topic of linear algebra.  Together, they succinctly characterize
the actions performed by a matrix when it is multiplied with a vector.

Let's now consider if these ideas remind us of anything we've seen in our
discussion so far.  What if the matrix $A$ was replaced with one of our
transition matrices $T$?  Also, what if the vector $\mathbf{x}$ was replaced
with one of our stable state vectors?  Would the above equation still hold
true?  Let's see:

\begin{align*}
  T \B s &= \M{%
    0 & 0.5 & 1 \\
    1 & 0 & 0 \\
    0 & 0.5 & 0
  } \M{.4 \\ .4 \\ .2}
  = \M{.4 \\ .4 \\ .2} = \B s \\
  \implies T \B s &= \B s
\end{align*}

We can see that our state vector $\mathbf{s}$ is indeed an eigenvector of $T$
with an eigenvalue of $1$.

We can now define the problem of finding the rank vector of pages on the
internet concisely in terms of linear algebra.  We say that the rank vector of
the web is the eigenvector of the web's transition matrix with eigenvalue
1.^[Actually, it is this eigenvector scaled by the inverse of the sum of its
terms.  This scaling would guarantee that the vector represents a probability
distribution and that its terms sum to 1.]
