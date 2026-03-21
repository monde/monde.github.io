---
title: "Save your file after calling YAML::dump"
date: 2007-01-25
categories: [Ruby, Nuby Rails]
tags: [ruby, yaml]
---

Not saving a yaml file after calling YAML::dump cost me about two hours the other day. Here’s an example:

```bash
# load

fnm
='
myyaml.yml
'

h
 
=
 
YAML
::
load_file
(
fnm
)
 
||
 
Hash
.
new

# add to hash

h
[
:foo
]='
bar
'

#save

=begin
# don't do it like this ...
f = File.open(fnm, 'w')
YAML::dump(h, f)
#close writes the file to disk
f.close
=end

# file gets closed after block executes

File
.
open
(
fnm
,
 
'
w
')
 
do
 
|
out
|

   
YAML
.
dump
(
h
,
 
out
)

end
```
