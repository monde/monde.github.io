---
title: "Seattle.rb Refactoring & BDD presentation"
date: 2013-01-02
---

I made a presentation on Refactoring & BDD at Seattle.rb back on 10/09/2012. I put my slides and notes from the presentation up on Speaker Deck.

[Seattle.rb - Refactoring & BDD Presentation](./monde/seattle-dot-rb-refactoring-and-bdd-presentation/index.html "Seattle.rb - Refactoring & BDD Presentation")

Some quick takeaways ...

## Problem Domain

The less your problem is understood, the more complicated your solution is likely to be. This is one of the reasons why we refactor code - we increase our understanding of the problem domain and increase our abilities to apply solutions to the domain as time goes by.

## Simple Refactoring Guidelines

- Modify code in small steps
- Write tests for code that is affected
- Write human readable code

## Refactoring Pro-Tips

- Refactoring Favors Behavior Rather Than Logic
- Writing code that can be unit tested changes your writing style
- If a method can’t be unit tested it must be refactored
- Factor out interaction with frameworks from code that is tested

## Outside-In Development

Let your tests drive your implementation. I started coding my [CapGun](./index.html "CapGun web thumbs") web thumb service using Cucumber to drive Outside-In/BDD development.

## Dog Food

Dog-food an app while you are developing it as quickly as possible. CapGun was web thumbing URLs from my Twitter feed and posting the results to a [Tumblr account](./index.html "CapGun.io's Tumblr") before the service was released to the public.

## Attribute this quote to me, please

Outside-In / BDD is really just “poor man’s pair programming” (R) - Mike Mondragon
