---
title: "I built an OpenClaw plugin"
date: 2026-03-31
---

<img src="/assets/images/openclaw-ebay-plugin-demo.webp" alt="OpenClaw eBay plugin demo" style="float: left; margin: 0 1em 1em 0;">

I hate HTML forms in a browser. eBay listing forms are a particular offender —
dropdowns, required fields, category trees. So I built an OpenClaw plugin for
eBay and the Lobster handles all of it now, efficiently, through eBay's API.
The animated image to the left is the sizzle reel of creating an eBay listing
simply through chat and sharing images. A better one minute video, and the full
six minutes of the interaction is referenced at the end of this post.

eBay does have its own AI image scan to bootstrap a listing from a photo. It
works, but it's baked into eBay's UI — a one-shot feature you can't build on.
With the OpenClaw plugin, the knowledge about how to create a listing lives in
code I own and can reuse. When eBay's API behaves unexpectedly or throws an
edge case, the OpenClaw can heal itself and/or fix plugin code to work around
it. A traditional fixed UX can't do that.

Claude labor is just like human labor. Asking Claude to figure out how to do
something from scratch is fine once, but inefficient the second time. You're
paying to rediscover the same territory every time you run it.

Moving that knowledge into a Skill is a step up. A Skill gives Claude a focused
starting point for repeating a task. But a Skill is still guidance — Claude
still has to reason through the specifics on each invocation, the same way a
person who's done something before still has to think it through each time.

Actions in an OpenClaw plugin go further. They encapsulate repeatable work
against a third-party API so it doesn't have to be relearned on each run. The
how is baked in.

Better yet, a plugin can expose RPCs so other plugins — or the OpenClaw agent
itself — can invoke those focused actions directly without having to relearn
the task. The knowledge accumulates and stays useful across sessions instead of
evaporating when the conversation ends.

If you want to see it in action, here's a one-minute cut with the highlights of
the eBay demo.

<iframe width="560" height="315" src="https://www.youtube.com/embed/1lWGIxBFvWA" title="OpenClaw eBay plugin demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The full six-minute version shows the whole interaction — texting with The
Lobster (aka biddy as it's known to me in Telegram) to build and refine an eBay
listing through a plain chat exchange. It's slow: Biddy is sandboxed in a
Docker container on my laptop, running Claude Opus 4.6, and every message is
bouncing through my home connection to Telegram then out to AT&T and back. But
that's not the point. Watch how the collaboration works — iterating on a
listing just by chatting. I even write the box weight and dimensions on an
index card and feed that to biddy to fill in the shipping details. This is
extremely useful to record freehand when the package is on the scale. A huge
time saver - if you know, you know.

<iframe width="560" height="315" src="https://www.youtube.com/embed/olLAA9LXl_Y" title="OpenClaw eBay listing full demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

I'm thinking about productizing this work, let me know if you are interested
mikemondragon@gmail.com .
