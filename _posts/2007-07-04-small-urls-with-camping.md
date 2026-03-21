---
title: "small urls with Camping"
date: 2007-07-04
categories: [web2.0, Ruby, Rails, Camping]
tags: [camping, hurl]
---

I am happy to announce yet another very small URL generator called

**[hurl it](./index.html)** => http://hurl.it/

In fact its first entry is [this very blog post](./x/index.html).

There are obvious predecessors and the recent (and very cool) Rails based [urlTea](./index.html) which itself I think is inspired by [rubyurl](./index.html)

But [hurl it](./index.html) is not those things, [hurl it](./index.html) is a Camping application. [Camping](./files/README.html) is a Microframework written by [why the lucky stiff](./index.html), a [MVC](./wiki/Model-view-controller/index.html) based framework that is a total size of 4K and written in Ruby. Camping applications are small, light weight, and are intended to do one thing really well. [hurl it](./index.html) does one thing very well – RESTfully create and serve very small URLs.

[hurl it](./index.html) has these attributes

- is a [Camping](./files/README.html) application
- RESTful (index, show, and create verbs) and responds to application/xml
- tunes its use of ActiveRecord for use with the performanced minded MyISAM engine
- developed with Agile practices including full unit and functional tests using [Mosquito](./index.html)
- is open source under the MIT License
- has a neat-o base 62 number algorithm using the alphabet of 0-9,A-Z,a-z that would be good to know on an interview

[hurl it](./index.html) is meant to be the honey layer in your peanut butter sandwich on wheat bread. [hurl it](./index.html) is not the sandwich nor tries to be anything more than really super awesome at representing long URLs as really short URLs.

Things I’ve found helpful during [hurl it](./index.html) development

- [Evan Weaver](./index.html) Camping Master
- [top-secret tuned mysql configurations for rails](./articles/2007/04/30/top-secret-tuned-mysql-configurations-for-rails/index.html) (EV)
- [rv-a-tool-for-luxurious-camping](./articles/2006/12/19/rv-a-tool-for-luxurious-camping/index.html) a SysV init.d reference implementation for daemonizing Camping apps (EV)
- [Camping, a Microframework](./files/README.html) (by \_why)
- [Mosquito](./index.html) Camping test framework (by TF GG)

I wrote a SysV init.d setup for Gentoo based on Evan’s work call [RV2](./articles/2007/07/05/rv2-camping-on-gentoo)

**Source**

svn checkout http://svn.mondragon.cc/svn/hurl hurl

or

svn checkout http://svn.mondragon.cc/svn/hurl/tags/hurl-1.0/ hurl
