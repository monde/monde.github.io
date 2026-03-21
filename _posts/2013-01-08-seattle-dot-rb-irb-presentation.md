---
title: "Seattle.rb IRB presentation"
date: 2013-01-08
---

I gave a lightening talk about IRB (Interactive Ruby Shell) at [Seattle.rb](./index.html) on 01/08/2013.

Here is my speaker deck:
[https://speakerdeck.com/monde/seattle-dot-rb-irb-presentation](./monde/seattle-dot-rb-irb-presentation/index.html)

Here my notes and example irbrc's:
[http://bit.ly/seattle-rb-irb](./seattle-rb-irb/index.html)

The [irbtools gem](./janlelis/irbtools/index.html) is really massive in all of the features it curates together. As mentioned in the deck, I prefer a more simple setup of:

- integrated vim to edit/paste code via the [interactive editor gem](./jberkel/interactive_editor/index.html)
- load/save command history (require 'irb/ext/save-history')
- tab completion on object methods (require 'irb/completion')
