---
title: "maintaining my copy of obtvse"
date: 2012-08-06
---

I'm maintaining my own copy of the [obtvse blog application](./NateW/obtvse/index.html "obtvse blog"). I set my copy up initially as a duplicate repository from obtvse's git repository. These commands were used to duplicate the repo.

```shell
git clone --bare https://github.com/NateW/obtvse.git
git push --mirror git@example.com:monde/whatever.git
```

Now, I can hack on my copy all I want and keep it in a private repository. I've added my favorite capistrano set up and have appended other gems to the Gemfile such as rubyracer to compile assets during deployment. When obtvse gets some code changes that I would like pull into my copy I will do so having NateW's repository as a remote in my local repository such as the following example.

```shell
git remote add natew https://github.com/NateW/obtvse.git
git checkout master
git fetch natew
git merge natew/master
```
