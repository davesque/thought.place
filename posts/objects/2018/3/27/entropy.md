---
title: Understanding Entropy (Information Theory)
---

In the world of computing and technology, it's not unusual to run into the term
"entropy".  A common place to encounter this term might be in a password
manager app.  If you use such an app to generate a random password, it might
give you some feedback about how "good" the password is.  Usually, this
feedback comes in the form of a printout that says how much "entropy", measured
in bits,  a password contains.  This printout might also be accompanied by a
bar which appears to increase in length and change in color from red to green
as the generated password is found to have more bits of entropy.  So it's
probably clear that more entropy is better.  We can also imagine that, if a
password is considered better, it's probably harder to guess.

So what's this all about?  How do programs like that actually calculate how
many bits of entropy are contained in passwords?  Also, once you've got that
figure, how should you interpret it?  What does it actually mean?  If you've
always wondered, then read on.

## Measuring Randomness

To get some insight into this, let's consider the following question: how can
randomness be measured?  The question might seem strange.  After all, random is
random, right?  Whether we're talking about a coin flip or a slot machine or
even the weather, it seems reasonable to say that something is either random or
pre-determined.  But imagine this:

Say you have a friend that always wants to decide what to do based on the
outcome of a coin flip.  They keep this coin in their pocket and always call
the side...and they always seem to get to decide what to do.  After a while,
you begin to suspect the coin may not be fair---that is, it may be more likely
to fall on one side than the other.  You might want to know just how unfair
this coin is.

What you're asking is, "How random is this coin?"  If the coin lands on heads
half the time and tails half the time, that's as random as you could hope for
it to be.  You're not going to have much luck guessing the side for a flip.
However, if the coin lands on heads $1/4$ of the time and tails $3/4$ of the
time, that's a different story.  In that case, it's correct to say that the
coin is much less random.  The coin would be even less random still if it
landed on tails $9/10$ of the time.
