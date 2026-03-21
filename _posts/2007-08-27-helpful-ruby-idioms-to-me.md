---
title: "helpful Ruby idioms (to me)"
date: 2007-08-27
categories: [Ruby]
tags: [ruby]
---

Before coming to Ruby I had spent a lot of time coding Java and some C/C++ . Like any programmer I spend a lot of time working with data structures (and now blocks in Ruby). I would often fall back to idioms concerning data structure size in those legacy languages but in Ruby they are bad habits.

The [Enumerable](./core/classes/Enumerable.html) module that is mixed in to [Array](./core/classes/Array.html), [Hash](./core/classes/Hash.html), and others is your friend. Use its idioms to tell you the **state** of your data structure rather raw details as in Java that imply state. For instance in Java, we test for elements in a collection with.size() (like myhash.size() == 0), but in Ruby having elements (or not) is more statefully conveyed with .any? and .empty?

Some goodies in [Enumerable](./core/classes/Enumerable.html) :

- [any?](./core/classes/Enumerable.html#M003163) – do we have any elements?
- [empty?](./core/classes/Array.html#M002200) (in Array class) – are we void of elements?
- [detect](./core/classes/Enumerable.html#M003154) – return the first element that matches the criteria in the block
- [select](./core/classes/Enumerable.html#M003156) – return all the elements that match the criteria in a block
- [each\_with\_index](./core/classes/Enumerable.html#M003168) – enumerate over elements in the data structure AND automatically give me an index (which means I don’t have to predefine one)

And example in an irb session:

```bash
mike@butch 10001 ~$ irb
irb(main):001:0> a = ['hello', 'ruby-20', 'ruby']
=> ["hello", "ruby-20", "ruby"]
irb(main):002:0> a.detect{|v| v =~ /foo/}
=> nil
irb(main):003:0> a.detect{|v| v =~ /hello/}
=> "hello" 
irb(main):004:0> a.detect{|v| v =~ /ruby/}
=> "ruby-20" 
irb(main):005:0> a.select{|v| v =~ /ruby/}
=> ["ruby-20", "ruby"]
irb(main):006:0> a.empty?
=> false
irb(main):007:0> a.any?
=> true
irb(main):008:0> a.each_with_index{|v,i| puts "index: #{i}, val #{v}"}
index: 0, val hello
index: 1, val ruby-20
index: 2, val ruby
=> ["hello", "ruby-20", "ruby"]
```
