---
title: "assert_redirected_to Expects Strings, Not Symbols and  Simple Localization"
date: 2006-10-28
categories: [Ruby, Rails, Nuby Rails]
tags: [nuby, rails, ruby]
---

I’ve been in the process of refactoring a CRUD-like webapp that I had written in PHP over to the Ruby On Rails Framework. I’m almost done with the re-factor of the object model and views and started going through [A Guide to Testing the Rails](./read/book/5/index.html) to learn the Rails way of unit testing to make my code even better. I was on sub-chapter 9.4 [Response-Related Assertions](./read/chapter/28#page234/index.html) and came upon an error in my unit test of a controller I couldn’t quite figure out. The syntax looked right, the controller logic looked right, and the test logic looked right.

This is a recreation of the error I kept getting with the **assert\_redirected\_to** test:

```bash
$ ruby test/functional/foo_controller_test.rb
Loaded suite test/functional/foo_controller_test
Started
F
Finished in 0.029546 seconds.

  1) Failure:
test_invalid_language(FooControllerTest) [test/functional/foo_controller_test.rb:20]:
response is not a redirection to all of the options supplied (redirection is <{:action=>"index", :language=>"es", :controller=>"foo"}>), difference: <{:action=>:index, :controller=>"foo"}>

1 tests, 4 assertions, 1 failures, 0 errors
```

This controller is using a before filter to re-establish a localization state if the user’s preferred language that is stored in a cookie exists. For simplicity’s sake the webapp has a simple localization framework to render pages into different languages from translations stored in the db. The way it works is if by opening the URL **http://localhost:3000/foo/index/fr** the page at that URL will be localized into French language. When that page is rendered the webapp sets a long lasting cookie to the save the French language preference. The pattern for the URL is **’:controller/:action/:language’** which has been defined in the webapp’s configuration.

**config/routes.rb**

```bash
  
# The localized path the webapp uses

  
map
.
connect
 
'
:controller/:action/:language
',

              
:controller
 
=>
 
'
foo
',

              
:requirements
 
=>
 
{
 
:language
 
=>
 
/
en|es|fr
/
 
}
```

This localization scheme follows the suggested pattern of [URIs, Addressability, and the use of HTTP GET and POST](./2001/tag/doc/whenToUseGet.html) suggested by the W3C. Specifically the webapp exhibits [The Benefits of URI Addressability](./2001/tag/doc/whenToUseGet.html#uris)

- linking
- bookmarking
- caching

I want the controller to be smart so that if the language setting gets corrupted somehow then a default language will get set in a [before\_filter](./classes/ActionController/Filters/ClassMethods.html#M000152) that I’ve called **set\_language**

Here’s how I created the Foo controller for this example.

```bash
$ ruby script/generate controller Foo
      exists  app/controllers/
      exists  app/helpers/
      create  app/views/foo
      exists  test/functional/
      create  app/controllers/foo_controller.rb
      create  test/functional/foo_controller_test.rb
      create  app/helpers/foo_helper.rb
```

This is a basic Foo controller wired to be aware of the localization language setting.

```ruby
class 
FooController
 
<
 
ApplicationController

  
DEFAULT_LANGUAGE
 
=
 
"
en
"

  
VALID_LANGUAGES
 
=
 
%w{
en es fr
}

  
before_filter
 
:set_language

  
def 
index

  
end

private

  
def 
set_language

    
cookie_expire
 
=
 
10
.
years
 
# 10 year cookie

    
cookie_language
 
=
 
DEFAULT_LANGUAGE

    
# get the cookie straight

    
if
 
!
cookies
[
:language
].
nil?
 
&&
 
VALID_LANGUAGES
.
include?
(
cookies
[
:language
])

      
# honor the inbound cookie, change it in the params check

      
cookie_language
 
=
 
cookies
[
:language
]

    
end

    
# now check the language in the GET

    
if
 
VALID_LANGUAGES
.
include?
(
params
[
:language
])

      
cookie_language
 
=
 
params
[
:language
]

    
end

    
cookies
[
:language
]
 
=
 
{
 
:value
 
=>
 
cookie_language
,
 
:expires
 
=>
 
cookie_expire
}

    
# redirect on a bad language

    
if
 
!
VALID_LANGUAGES
.
include?
(
params
[
:language
])

      
redirect_to
 
:controller
 
=>
 
controller_name
,
 
:action
 
=>
 
params
[
:action
],
 
:language
 
=>
 
cookie_language

    
end

  
end

end
```

And the example unit test

```ruby
require
 
File
.
dirname
(
__FILE__
)
 
+
 
'
/../test_helper
'

require
 
'
foo_controller
'

# Re-raise errors caught by the controller.

class 
FooController
;
 
def 
rescue_action
(
e
)
 
raise
 
e
 
end
;
 
end

class 
FooControllerTest
 
<
 
Test
::
Unit
::
TestCase

  
def 
setup

    
@controller
 
=
 
FooController
.
new

    
@request
    
=
 
ActionController
::
TestRequest
.
new

    
@response
   
=
 
ActionController
::
TestResponse
.
new

  
end

  
# test if a bad language is set in path, use the cookie setting if not

  
def 
test_invalid_language

    
@request
.
cookies
['
language
']
 
=
 
CGI
::
Cookie
.
new
('
language
',
 
'
es
')

    
get
 
:index
,
 
'
language
'
 
=>
 
'
ru
'

    
assert_not_nil
 
cookies
['
language
']

    
assert_equal
 
%w{
es
},
 
cookies
['
language
']

    
assert_redirected_to
 
:action
 
=>
 
:index
,
 
:language
 
=>
  
'
es
'

    
#assert_redirected_to :action => 'index', :language => 'es'

    
assert_response
 
:redirect

  
end

end
```

Notice the first **assert\_redirected\_to** that is causing the error with this unit test and the commented correct **assert\_redirected\_to**.

```
assert_redirected_to
 
:action
 
=>
 
:index
,
 
:language
 
=>
  
'
es
'

#assert_redirected_to :action => 'index', :language => 'es'
```

The first version causing the error is a nuby mistake on my part. When code is written in a controller that has ActionController::Base as its ancestor, the [redirect\_to](./classes/ActionController/Base.html#M000209) (which calls [url\_for](./classes/ActionController/Base.html#M000202) ) is a method of controller because of inheritance. That controller action’s are really just public methods of the controller class and can be referenced by their symbol. I used the patterns I’ve seen in controller code for **redirect\_to** and **url\_for** to write my **assert\_redirected\_to** test.

But the unit test inherits from Test::Unit::TestCase, it is not a child of ActionController::Base. So the **assert\_redirected\_to** shouldn’t use the symbol to refer to the index action. It should use the name of the action as a string, here’s the proper code snippet that was commented out above.

```
assert_redirected_to
 
:action
 
=>
 
'
index
',
 
:language
 
=>
 
'
es
'
```

And now the functional test works correctly.

```bash
$ ruby test/functional/foo_controller_test.rb
Loaded suite test/functional/foo_controller_test
Started
.
Finished in 0.016737 seconds.

1 tests, 5 assertions, 0 failures, 0 errors
```

This controller is using a before filter to re-establish a localization state if the user’s preferred language that is stored in a cookie exists. For simplicity’s sake the webapp has a simple localization framework to render pages into different languages from translations stored in the db. The way it works is if by opening the URL **http://localhost:3000/foo/index/fr** the page at that URL will be localized into French language. When that page is rendered the webapp sets a long lasting cookie to the save the French language preference. The pattern for the URL is **’:controller/:action/:language’** which has been defined in the webapp’s configuration.

**config/routes.rb**

```bash
  
# The localized path the webapp uses

  
map
.
connect
 
'
:controller/:action/:language
',

              
:controller
 
=>
 
'
foo
',

              
:requirements
 
=>
 
{
 
:language
 
=>
 
/
en|es|fr
/
 
}
```

This localization scheme follows the suggested pattern of [URIs, Addressability, and the use of HTTP GET and POST](./2001/tag/doc/whenToUseGet.html) suggested by the W3C. Specifically the webapp exhibits [The Benefits of URI Addressability](./2001/tag/doc/whenToUseGet.html#uris)

- linking
- bookmarking
- caching

I want the controller to be smart so that if the language setting gets corrupted somehow then a default language will get set in a [before\_filter](./classes/ActionController/Filters/ClassMethods.html#M000152) that I’ve called **set\_language**

Here’s how I created the Foo controller for this example.

```bash
$ ruby script/generate controller Foo
      exists  app/controllers/
      exists  app/helpers/
      create  app/views/foo
      exists  test/functional/
      create  app/controllers/foo_controller.rb
      create  test/functional/foo_controller_test.rb
      create  app/helpers/foo_helper.rb
```

This is a basic Foo controller wired to be aware of the localization language setting.

```ruby
class 
FooController
 
<
 
ApplicationController

  
DEFAULT_LANGUAGE
 
=
 
"
en
"

  
VALID_LANGUAGES
 
=
 
%w{
en es fr
}

  
before_filter
 
:set_language

  
def 
index

  
end

private

  
def 
set_language

    
cookie_expire
 
=
 
10
.
years
 
# 10 year cookie

    
cookie_language
 
=
 
DEFAULT_LANGUAGE

    
# get the cookie straight

    
if
 
!
cookies
[
:language
].
nil?
 
&&
 
VALID_LANGUAGES
.
include?
(
cookies
[
:language
])

      
# honor the inbound cookie, change it in the params check

      
cookie_language
 
=
 
cookies
[
:language
]

    
end

    
# now check the language in the GET

    
if
 
VALID_LANGUAGES
.
include?
(
params
[
:language
])

      
cookie_language
 
=
 
params
[
:language
]

    
end

    
cookies
[
:language
]
 
=
 
{
 
:value
 
=>
 
cookie_language
,
 
:expires
 
=>
 
cookie_expire
}

    
# redirect on a bad language

    
if
 
!
VALID_LANGUAGES
.
include?
(
params
[
:language
])

      
redirect_to
 
:controller
 
=>
 
controller_name
,
 
:action
 
=>
 
params
[
:action
],
 
:language
 
=>
 
cookie_language

    
end

  
end

end
```

And the example unit test

```ruby
require
 
File
.
dirname
(
__FILE__
)
 
+
 
'
/../test_helper
'

require
 
'
foo_controller
'

# Re-raise errors caught by the controller.

class 
FooController
;
 
def 
rescue_action
(
e
)
 
raise
 
e
 
end
;
 
end

class 
FooControllerTest
 
<
 
Test
::
Unit
::
TestCase

  
def 
setup

    
@controller
 
=
 
FooController
.
new

    
@request
    
=
 
ActionController
::
TestRequest
.
new

    
@response
   
=
 
ActionController
::
TestResponse
.
new

  
end

  
# test if a bad language is set in path, use the cookie setting if not

  
def 
test_invalid_language

    
@request
.
cookies
['
language
']
 
=
 
CGI
::
Cookie
.
new
('
language
',
 
'
es
')

    
get
 
:index
,
 
'
language
'
 
=>
 
'
ru
'

    
assert_not_nil
 
cookies
['
language
']

    
assert_equal
 
%w{
es
},
 
cookies
['
language
']

    
assert_redirected_to
 
:action
 
=>
 
:index
,
 
:language
 
=>
  
'
es
'

    
#assert_redirected_to :action => 'index', :language => 'es'

    
assert_response
 
:redirect

  
end

end
```

Notice the first **assert\_redirected\_to** that is causing the error with this unit test and the commented correct **assert\_redirected\_to**.

```
assert_redirected_to
 
:action
 
=>
 
:index
,
 
:language
 
=>
  
'
es
'

#assert_redirected_to :action => 'index', :language => 'es'
```

The first version causing the error is a nuby mistake on my part. When code is written in a controller that has ActionController::Base as its ancestor, the [redirect\_to](./classes/ActionController/Base.html#M000209) (which calls [url\_for](./classes/ActionController/Base.html#M000202) ) is a method of controller because of inheritance. That controller action’s are really just public methods of the controller class and can be referenced by their symbol. I used the patterns I’ve seen in controller code for **redirect\_to** and **url\_for** to write my **assert\_redirected\_to** test.

But the unit test inherits from Test::Unit::TestCase, it is not a child of ActionController::Base. So the **assert\_redirected\_to** shouldn’t use the symbol to refer to the index action. It should use the name of the action as a string, here’s the proper code snippet that was commented out above.

```
assert_redirected_to
 
:action
 
=>
 
'
index
',
 
:language
 
=>
 
'
es
'
```

And now the functional test works correctly.

```bash
$ ruby test/functional/foo_controller_test.rb
Loaded suite test/functional/foo_controller_test
Started
.
Finished in 0.016737 seconds.

1 tests, 5 assertions, 0 failures, 0 errors
```
