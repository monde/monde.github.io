---
title: "distribute scripts as gist micro-gems"
date: 2013-01-20
---

It's really easy to distribute scripts, not just gems, as gist micro-gems. Since rubygems and bundler can handle complicated dependencies the scripts you distribute can be more advanced than just ten or twenty lines.

I wrote a script to generate an OAuth key and secret for the Tumblr API and I made it available as a micro-gem. It is encapsulated in [gist 4577106](./4577106/index.html) To generate your key and secret is as simple as the following:

```shell
mkdir /some/working/dir
cd /some/working/dir

wget \
https://gist.github.com/raw/4577106/6bc9befedcd5238ce9f2ee562cace666dece460c/Gemfile

bundle install
bundle exec generate-token
```

One bit of useful flare is the ability to [set the bindir in the gemspec](./4577106#file-generate-tumblr-oauth-token-gemspec/index.html) of the microgem to dot "." - the current working directory. This allows `bundle exec generate-token` to work correctly since github gists don't allow files to be in sub-directories, and the default bindir in rubygems is 'bin/'.
