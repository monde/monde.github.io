---
title: "helpful Ruby idioms (to me)"
date: 2007-08-27
categories: [Ruby]
tags: [ruby]
---

Before coming to Ruby I had spent a lot of time coding Java and some C/C++ . Like any programmer I spend a lot of time working with data structures (and now blocks in Ruby). I would often fall back to idioms concerning data structure size in those legacy languages but in Ruby they are bad habits.

The [Enumerable](https://ruby-doc.org/3.4.1/Enumerable.html) module that is mixed in to [Array](https://ruby-doc.org/3.4.1/Array.html), [Hash](https://ruby-doc.org/3.4.1/Hash.html), and others is your friend. Use its idioms to tell you the **state** of your data structure rather raw details as in Java that imply state. For instance in Java, we test for elements in a collection with.size() (like myhash.size() == 0), but in Ruby having elements (or not) is more statefully conveyed with .any? and .empty?

Some goodies in [Enumerable](https://ruby-doc.org/3.4.1/Enumerable.html) :

- [any?](https://ruby-doc.org/3.4.1/Enumerable.html#method-i-any-3F) – do we have any elements?
- [empty?](https://ruby-doc.org/3.4.1/Array.html#method-i-empty-3F) (in Array class) – are we void of elements?
- [detect](https://ruby-doc.org/3.4.1/Enumerable.html#method-i-detect) – return the first element that matches the criteria in the block
- [select](https://ruby-doc.org/3.4.1/Enumerable.html#method-i-select) – return all the elements that match the criteria in a block
- [each\_with\_index](https://ruby-doc.org/3.4.1/Enumerable.html#method-i-each_with_index) – enumerate over elements in the data structure AND automatically give me an index (which means I don’t have to predefine one)

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
