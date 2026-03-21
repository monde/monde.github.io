---
title: "report Resque exceptions to Honeybadger"
date: 2012-08-06
---

Two of my heros, [Ben Curtis](./index.html "Ben Curtis") and [Starr Horne](./index.html "Starr Horne") are building their own application exception reporting service for Rails, and presumably other application frameworks like Sinatra. The service's name is [Honeybadger](./index.html "Honeybadger"). I've been running one of my hobby applications in the Honeybadger for a time. My application uses Resque as its work queue and I like to record exceptions into Honeybadger when they occur.

The Honeybadger gem configures directly into Rails' request/response loop. Therefore, all one has to do is initialize the application correctly with an account authorization code to the service, then view and controller exceptions are automatically recorded. However, if logging exceptions outside of that loop is required, the gist listed below is one way to achieve this goal for a Resque job queue.
