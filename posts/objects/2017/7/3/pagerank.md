---
title: Towards an Understanding of Search Engines
---

## Intuition

Imagine a robot which starts on some random page on the web &mdash; we'll call
it page 1.  The robot clicks some random link on page 1 and is led to page 2.
On page 2, the robot clicks another random link and is led to page 3 and so on.
Let's assume that, if this process continues on forever, the robot would
eventually visit every page on the web^[Attentive readers may realize that this
is not entirely true.  For instance, if the robot navigated to a page with no
links, it would get stuck.  For now, we assume the robot *will* visit every
page and that there are no strange circumstances that would cause the robot to
get stuck in a certain pattern.].  We can imagine that the robot might find
itself revisiting certain pages that are referred to often by others.  These
pages which are more commonly encountered are the important pages on the
internet.  Such pages could be ones like *wikipedia.com* or *nytimes.com*.

This sense of importance that we've just described more or less characterizes
the way that search engines rank and index web pages on the internet.  We can
describe the process in a few steps:

* We begin on some random page.
* We take an infinite, random walk of the web and record the frequencies with
  which we encounter every page that we come across.
* We use these frequencies to determine the probability of encountering each
  page after clicking a link during any step of our walk.
* We consider these probabilities to be the ranks of the pages we encountered
  (i.e. pages with higher probabilities of being encountered are considered to
  be more important).

If the web looked like figure 1, could we guess the probability that we would
find ourselves on page 1 during any step of an infinite walk?

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

What if we added a link from page 2 back to page 1 as seen in figure 2?  Would
page 1's probability change?

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

Of course, this all sounds a bit crazy.  How could we do an infinite walk of
the web?  Wouldn't that require an infinite amount of time?  Also, how do we
handle the case when the robot finds a page with no links to other pages as
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

  <figcaption>Figure 3: A web with a black hole.</figcaption>
</figure>

What if the robot begins in some part of the web which doesn't refer to any
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

  <figcaption>Figure 4: A web with isolated zones.</figcaption>
</figure>

To answer all these questions, we need to find a more systematic approach to
this problem.

## Algorithm

### Overview

More abstractly, the process of doing our infinite walk like we described above
can be represented with a state machine.  Each page on the web is one state in
the machine and all the links between pages are the transitions between those
states.

Let's say that each link has an equal probability of being taken by our random
walker robot during one step of its walk.  This means that, if our walker is on
a certain page (our machine is in a certain state), each link on that page has
an equal chance of being clicked by our walker (each state transition has an
equal chance of taking place).  This gives the following equation for a given
link's probability of being clicked:

\begin{align*}
  \text{probability of clicking link $x$} = \frac{1}{\text{total \# of links on the page where $x$ is found}}
\end{align*}

We're beginning to see that we're not just talking about a state machine, but a
*probabilistic* one &mdash; that is, a state machine which randomly transitions
between states based on some set of probabilities for each state.

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

To illustrate this idea further, let's annotate figure 2 with some
probabilities.  In figure 6, we see from these annotations that each link from
page 2 has a 1 in 2 chance of being clicked.  The link from page 1 has a 100%
chance of being clicked as does the link from page 3:

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
mathematically.  As it turns out, there is a way to do this using linear
algebra.

### Linear Algebraic Approach

In linear algebra, we represent probabilistic state machines using **transition
matrices**.  A **transition matrix** is a matrix which encodes the vertices and
edges in a graph, giving a probability or weight to each edge.  It is defined
in terms of the **adjacency matrix** of a graph as well as the graph's **degree
matrix**.

A graph's adjacency matrix $A$ is defined as follows:

\begin{equation*}
A_{ij} = \begin{cases}
  1\ \text{if vertex $i$ links to vertex $j$} \\
  0\ \text{otherwise}
\end{cases}
\end{equation*}

This gives us the following adjacency matrix for the graph seen in figure 6:

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

For our graph, that looks like this:

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
the transition probabilites for page 2 and so on.

Great!  Now, how do we actually *use* the state machine?  How do we actually
*run* it?  The process is detailed below:

\begin{align}
  \text{next state} &= T \times \text{previous or initial state} \label{eq:transition-informal} \\
  \B{s}_n &= T \B{s}_{n - 1} \label{eq:transition-formal} \\
  \B{s}_1 &= T \B{s}_0 \\
  \implies \M{0 \\ 1 \\ 0} &= \M{%
    0 & \sfrac{1}{2} & 1 \\
    1 & 0 & 0 \\
    0 & \sfrac{1}{2} & 0
  } \M{1 \\ 0 \\ 0} \label{eq:transition-actual}
\end{align}

In equations 1 and 2 above, the transition matrix $T$ multiplies with some
state vector to perform the action of transitioning to the next state.
Concretely, in equation 4, we begin our random walker on page 1 (state 1) by
choosing an initial state vector with 1 in its first slot as seen on the
right-hand side.  After the matrix-vector multiplication, we see that the 1 has
moved into the second slot on the left-side.  This means that our walker ended
up on page 2 after one "random" step^[In this case, it was not exactly random
since page 1 links to page 2 and nothing else.].  Let's see what happens if we
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
