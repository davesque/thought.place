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
can be represented with a state machine.  Each page on the web is one state of
the state machine and all the links between pages are the transitions between
those states.

Let's say that each link has an equal probability of being taken by our random
walker robot during one step of its walk.  This means that, if our walker is on
a certain page (our machine is in a certain state), each link on that page has
an equal chance of being clicked by our walker (each state transition has an
equal chance of taking place).  This gives the following equation for a given
link's probability of being clicked:

\\[
  \text{probability of clicking link $x$} = \frac{1}{\text{total \# of links on the page where $x$ is found}}
\\]
