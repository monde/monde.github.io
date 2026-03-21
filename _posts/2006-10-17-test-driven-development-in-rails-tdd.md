---
title: "Test Driven Development In Rails (TDD)"
date: 2006-10-17
categories: [Ruby, Typo, Seattle.rb, Rails]
tags: [rails, ruby, seattle.rb, typo]
---

I was talking to [Geoffrey Grosenbach](./index.html) ([of nuby on rails fame](./index.html)) at [Seattle.rb](./groups/show/1/index.html) tonight mostly about Typo and his new [Peep Code](./index.html) screen casts. Somehow he told us that his next Peep Code screen cast was going to be on TDD. That was my opening to complain about actually writing the test first. To be frank, I put my foot in my mouth, and unit testing in Rails has changed the way I code and in turn has made me a better programmer.

I’ve read the “[A Guide to Testing the Rails](./read/book/5/index.html)” at Ruby On Rails and so should you. While I was reading it I would go into the rails application I was working on
at the time and implement my testing. First the unit tests and then functional tests. Working on my code and my tests at the same has helped me to learn more features in the Rails framework to make my tests pass!

The rest of the [HowtosTesting](./rails/pages/HowtosTestingat/index.html) section in Ruby On Rails has other granular topics on Rails testing.

Tips (while in the root of your rails app):

```bash
$ rake test
```

Rake all tests.

```bash
$ rake test:units
```

Rake only unit tests.

```bash
$ rake test:functionals
```

Rake only functional tests.

```bash
$ ruby test/unit/foo_test.rb
```

Run a single unit test on the foo unit.

```bash
$ ruby test/functional/foo_controller_test.rb
```

Run a single functional test on the foo controller.

```bash
$ rake db:test:clone_structure
```

Clone the development DB to the test DB.

```bash
$ rake stats
```

Find out your code and tests stats (including Code to Test Ratio).

```bash
$ rake -T
```

List all the tasks that your rake can do.

I’ve read the “[A Guide to Testing the Rails](./read/book/5/index.html)” at Ruby On Rails and so should you. While I was reading it I would go into the rails application I was working on
at the time and implement my testing. First the unit tests and then functional tests. Working on my code and my tests at the same has helped me to learn more features in the Rails framework to make my tests pass!

The rest of the [HowtosTesting](./rails/pages/HowtosTestingat/index.html) section in Ruby On Rails has other granular topics on Rails testing.

Tips (while in the root of your rails app):

```bash
$ rake test
```

Rake all tests.

```bash
$ rake test:units
```

Rake only unit tests.

```bash
$ rake test:functionals
```

Rake only functional tests.

```bash
$ ruby test/unit/foo_test.rb
```

Run a single unit test on the foo unit.

```bash
$ ruby test/functional/foo_controller_test.rb
```

Run a single functional test on the foo controller.

```bash
$ rake db:test:clone_structure
```

Clone the development DB to the test DB.

```bash
$ rake stats
```

Find out your code and tests stats (including Code to Test Ratio).

```bash
$ rake -T
```

List all the tasks that your rake can do.
