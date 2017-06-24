---
title: jQuery.live() performance issues
---

Here's an interesting issue that came up recently.  The other day, I managed to
tackle a large bug at work that led to a tremendous speed increase in our app.
This bug had been around for a while, but its cause hadn't yet been determined.

It turned out that the culprits were event listeners set up with
`jQuery.live()`.  Let it be known that `$.live()` generally does not behave as
expected, particularly when it is called on a jQuery object that was
constructed with a context selector.  We had been using the following method
for calling `$.live()`:

```javascript
$("input[title='Update']", "#module_a").live("click", function () {
  // Event handling code...
});
```

The above code does not function the way you'd think.  First of all, when
specifying a context for a live event trigger (as `#module_a` was specified
above), that context must already exist in the document.  This goes against
what you'd expect from an event trigger that is set up in this way.  After all,
live triggers are distinguished from simple bind triggers in that they are
supposed to apply not just to existing elements but to non-existent, future
elements as well.  Second, a context must be specified as a _DOM_ element and
nothing else.  So that code should have been written this way:

```javascript
// The only difference here is that "#module_a" is
// now $("#module_a")[0] which gets the DOM
// element of #module_a.
$("input[title='Update']", $("#module_a")[0]).live("click", function () {
    // Event handling code...
});
```

Our problem was two-fold.  We had not yet created the context for that trigger.
Furthermore, we were not specifying the context correctly.  We naturally
assumed that contexts specified for live triggers work as they do in any other
case, accepting either a selector string, jQuery object, or DOM element.

The net effect of this was that large amounts (thousands) of event listeners
were being installed on the document root, which is the default context for
live triggers.  So, any event that fired in our app had to make it through a
veritable gauntlet of bubble listeners.  Before, there had been a particularly
troublesome function (`matchSelector`) which was showing tens of thousands of
calls in our profiler runs.  After implementing a proper fix for the missing
context issue, calls to `matchSelector` dropped by a factor of about 100.

The jQuery [documentation for live](http://api.jquery.com/live/) does mention
this special behavior under the "Event Context" section, but it is not given
nearly enough emphasis considering the impact it can have on performance in
large web applications (**Update - 2/18/2013**: this shortcoming in the docs
appears to have been rectified).  In fact, I found out about the issue on an
entirely separate site: 

[NetTuts+ - Quick Tip: The Difference Between Live() and Delegate()](http://net.tutsplus.com/tutorials/javascript-ajax/quick-tip-the-difference-between-live-and-delegate/)

I hope they work out this quirky behavior in a future release.

**Update - 2/18/2013**: `jQuery.live` was deprecated in jQuery version 1.7 and
removed in version 1.9 on account of its inefficiencies.  The API documentation
also appears to have been updated with a more informative explanation of the
caveats when using `jQuery.live`.
