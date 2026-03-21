---
title: "Rails Models in a Namespace"
date: 2007-07-29
categories: [Ruby, Rails, Nuby Rails]
tags: [rails, ruby]
---

If you are starting to get a cluttered model space in your Rails application
you should consider placing your models in a namespace. As an example I’m
going to go through a Rails application I’m calling Recipes. If my
models were starting to have the namespace implied in the class names such as
AppleFruit in **app/models/apple\_fruit.rb** then that’s starting to smell like
rotten apples. A better namespace would be Fruit::Apple in **app/models/fruit/apple.rb**

This is what we’ll be modeling. Fruits of Apples and Oranges via single table
inheritance. And Vegetables of Potatoes and Carrots through single table
inheritance.

We’ll have Ingredients that belong to Fruit, Vegetables, and Recipes.
Ingredients are a limited kind of join model going from the recipe through
to the kind of ingredient (i.e. fruit or vegetable). Ingredients are a true
join model from the fruit or vegetables back to their associated recipes.
The Ingredient is polymorphic because Fruits and Vegetables are different kinds of
objects.

Finally Recipes are another single table inheritance model but by
convention they will only have ingredients, they won’t be associated
to the kinds of ingredients through the polymorphic Ingredient class.
To access the specific kinds of ingredients from the recipe’s perspective
you must access the collection of ingredients and then program the desired
behavior to access the kinds of ingredients in your application logic.

Here’s a graph of the models we are designing (click for bigger picture):

The graph was made with [Railroad](./index.html) which uses
[Graphiz](./index.html) to generate the graphs.

All of the source for this example as available at the following Subversion
code repository

**svn checkout http://svn.mondragon.cc/svn/recipes/trunk/ recipes**

[http://svn.mondragon.cc/svn/recipes/trunk/](./svn/recipes/trunk/http://svn.mondragon.cc/svn/recipes/trunk/index.html)

## Setup

For simplicity we’ll be using a sqlite3 database for this application, now that
we are eating fruits and vegetables we don’t need to be any fatter with an external
database server floating around. This example is done in Rails 1.2.3

Before we go on let me give you a quote that [Eric Hodel](./index.html)
has been putting in the footer of his emails:

```bash
Poor workers blame their tools. Good workers build better tools. The
best workers get their tools to do the work for them. -- Syndicate Wars
```

I’ve been learning many things from Eric and I try to emulate what he does as
a developer. Two things he always does is practice test driven development and
uses a tool he wrote called [autotest](./ZSS/Products/ZenTest/index.html)
to make TDD easier to accomplish. autotest does supports Rails out of the box.
Now on with our recipes…

This is the **config/database.yml** we’ll be using:

```bash
market: &market
  adapter: sqlite3

development:
  database: "db/development.db" 
  <<: *market

production:
  database: "db/production.db" 
  <<: *market

test:
#  database: ":memory:" 
  database: "db/test.db" 
  <<: *market
```

And we’ll start off by putting our sessions in the database and then running the migration to ensure
we have our database settings correct.

```
rake db:sessions:create
rake db:migrate
rake test
```

Now in a separate console cd into the root of your application and start autotest

```
autotest
```

it will run in your directory and whenever you save a test or code file the corresponding
unit tests will be fired for those files.

## Fruits and Vegetables models

### Fruits

Now lets make a Base of our Apples and Orange model with single table inheritance, after
the fixture is generated we need to fix where its placed as in the example. Note we are
declaring a string attribute named ‘type’ to the model generator. The string is really a
column and having a column named ‘type’ is a Rails idiom signaling single table inheritance.

```bash
ruby script/generate model Fruit::Base type:string
mv test/fixtures/fruit/fruit_bases.yml test/fixtures/
rmdir test/fixtures/fruit/
```

In your unit test test/unit/fruit/base\_test.rb you need to clue the test into
knowing which table/fixture is to be used in the namespace. Coincidently note
that your tables and fixtures will still look somewhat flat even though your model classes
have depth. After you save the test autotest should be complaining the about an error
with the SQL since you haven’t yet migrated your schema. Lets also change the default
truth test the generator runs so that autotest is testing something of value for
better test driven development

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
/../../test_helper
'

class 
Fruit::BaseTest
 
<
 
Test
::
Unit
::
TestCase

  
fixtures
 
:fruit_bases

  
set_fixture_class
 
:fruit_bases
 
=>
 
Fruit
::
Base

  
# if our notion of a valid new fruit changes then we'll catch it that here

  
def 
test_should_be_valid

    
f
 
=
 
Fruit
::
Base
.
new

    
assert
 
f
.
valid?

  
end

end
```

In your base fruit model you also have to mark which table to assign the class in its namespace

```ruby
class 
Fruit::Base
 
<
 
ActiveRecord
::
Base

  
set_table_name
 
:fruit_bases

end
```

Now migrate your schemas and then re-save your **app/models/fruit/base.rb** and you should see
autotest is happy, it doesn’t have any errors or failures.

```
rake db:migrate
```

See, autotest is happy, it doesn’t have any errors or failures

```ruby
/usr/local/bin/ruby -I.:lib:test -rtest/unit -e "%w[test/unit/fruit/base_test.rb].each { |f| require f }" | unit_diff -u
Loaded suite -e
Started
.
Finished in 0.48792 seconds.

1 tests, 1 assertions, 0 failures, 0 errors
```

Now lets generate our Apples and Oranges, but the generator is going to create
test/fixtures/fruit/fruit\_apples.yml and test/fixtures/fruit/fruit\_oranges.yml
and we won’t need those fixtures because we are using single table inheritance
and we’ll only have one fixture for all of the fruits: test/fixtures/fruit\_bases.yml
Migrations for Fruit::Orange and Fruit::Apple are also generated. We don’t need
those because we are doing single table inheritance from the Fruit::Base
Migrate the schema while you are at it.

```
ruby script/generate model Fruit::Apple
rm db/migrate/*_create_fruit_apple.rb
rm test/fixtures/fruit/fruit_apples.yml
ruby script/generate model Fruit::Orange
rm db/migrate/*_create_fruit_apple.rb
rm test/fixtures/fruit/fruit_oranges.yml
rmdir test/fixtures/fruit/
rake db:migrate
```

For simplicity of this example we want to have a Apple and a Orange in our fruits
fixture test/fixtures/fruit\_bases.yml

```
one:
  id: 1
  type: Apple
two:
  id: 2
  type: Orange
```

This is what their models and tests should look like, as you go through saving your changes
lining up the files watch what autotest is telling you. Do not react to autotest until after
you have set up apple.rb, orange.rb, apple\_test.rb, and orange\_test.rb files. See how our
inheritance is denoted in the models Fruit::Apple < Fruit::Base and Fruit::Orange < Fruit::Base

**app/models/fruit/apple.rb**

```ruby
class 
Fruit::Apple
 
<
 
Fruit
::
Base

end
```

**test/unit/fruit/apple\_test.rb**

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
/../../test_helper
'

class 
Fruit::AppleTest
 
<
 
Test
::
Unit
::
TestCase

  
fixtures
 
:fruit_bases

  
set_fixture_class
 
:fruit_bases
 
=>
 
Fruit
::
Base

  
# loading from the fixture there is only one Apple

  
def 
test_there_should_only_be_one_apple_in_the_fixture

    
assert_equal
 
1
,
 
Fruit
::
Apple
.
find
(
:all
).
length

  
end

end
```

Orange will follow the same pattern as Apple.

Once completed have a sanity check with the rake test:unit task

```
rake test:unit
```

### Vegetables

Do everything we just did for Fruits, but this time for Vegetables. We want to
end up with Vegetable::Base, Vegetable::Carrot, and Vegetable::Potato . Don’t forget
to trigger single table inheritance when you generate the base and trim out the
non single table inheritance from the Carrots and Potatoes fixtures.

## Ingredient model

Now we’ll make the Ingredient model. It will use a polymorphic association so that it can
refer to fruits and vegetables. From a Fruit::Base perspective the ingredient model will
be a join model to recipes (we’ll update our Fruit::Base code shortly to accomplish this)
From recipe’s perspective (which we will generate shortly) the ingredient model can not
be used as a join model to fruits and vegetables because the polymorphic side the of
ingredients can not be used in this manner.

Generate the model with ‘kind’ being the name used in the polymorphic idiom (kind\_id, kind\_type)
for heterogeneous ingredients and recipe\_id used to join a kind of ingredient (fruit, vegetable, etc.)
back to the recipe that uses it.

```bash
ruby script/generate model Ingredient::Base kind_id:integer kind_type:string recipe_id:integer
mv test/fixtures/ingredient/ingredient_bases.yml test/fixtures/ingredient_bases.yml
rmdir test/fixtures/ingredient/
```

**app/models/ingredient/base.rb**

```ruby
##

# A polymorphic model to associate different kinds of

# specific ingredients with a recipe.  The joining nature

# of the ingredient is one way from its kind to the recipe.

# The recipe cannot go through the ingredient to its kind

# due to a limitation in the polymorphic model.

class 
Ingredient::Base
 
<
 
ActiveRecord
::
Base

  
set_table_name
 
:ingredient_bases

  
belongs_to
 
:kind
,
 
:polymorphic
 
=>
 
true

  
belongs_to
 
:recipe
,
 
:class_name
 
=>
 
"
Recipe::Base
",
 
:foreign_key
 
=>
 
"
recipe_id
"

end
```

There is not anything of significance about the polymorphic declaration of the Ingredient model.
However since the Recipe is itself in a namespace we need to help ActiveRecord with the recipe
association declaring the class\_name of the recipe and the foreign key to it.

Don’t forget to write a unit test for you Ingredient model.

We also need to update the basic fruit and vegetable base models.

Here is the updated **app/models/fruit/base.rb**

```ruby
##

# A fruit base class that uses single table inheritance.

# Specific kinds of fruits should inherit from this class.

# A fruit has ingredients as join a model through which

# recipes that include the fruit can be found.

class 
Fruit::Base
 
<
 
ActiveRecord
::
Base

  
set_table_name
 
:fruit_bases

  
has_many
 
:ingredient
,
 
:class_name
 
=>
 
'
Ingredient::Base
',

           
:foreign_key
 
=>
 
:kind_id
,
 
:conditions
 
=>
 
"
kind_type LIKE 'Fruit::%'
"

  
has_many
 
:recipes
,
 
:through
 
=>
 
:ingredient
,
 
:uniq
 
=>
 
true

end
```

Notice that the fruit base has many ingredients. But because ingredients are polymorphic
(has an kind\_id column and a kind\_type column) the fruit base needs to declare the foreign key
that the ingredient uses to refer to it and what the kind\_type column will look like when
an ingredient is pointing to fruit. Once that is established then the ingredient model can
be used as a join model which we go through to get to the recipe that includes this kind of
ingredient.

Update your vegetable base model accordingly.

## Recipe model

Now lets generate the recipe model. Its using single table inheritance and we’ll give
each recipe a title so this is what our generation looks like. Don’t forget to
flatten the fixtures again.

```bash
ruby script/generate model Recipe::Base type:string title:string
mv test/fixtures/recipe/recipe_bases.yml test/fixtures/recipe_bases.yml
rmdir test/fixtures/recipe/
```

**app/models/recipe/base.rb**

```ruby
class 
Recipe::Base
 
<
 
ActiveRecord
::
Base

  
set_table_name
 
:recipe_bases

  
has_many
 
:ingredients
,
 
:class_name
 
=>
 
'
Ingredient::Base
',
 
:foreign_key
 
=>
 
:recipe_id

  
# If we could go through ingredients to their kinds this is how we would make

  
# the association.  However polymorphic models cannot be used as a join model

  
# when the join is towards the heterogeneous type referenced by the model

  
# has_many :kinds, :through => :ingredients

end
```

Again, we need to clue AR in to which ingredient model we are associating with and what the foreign key
used. Don’t for get to write your tests.

## Runtime

### Integration test

Be sure to check out the source code of the example. It has an integration test that runs the
model through its paces using predefined fixtures. This is the test

**test/integration/recipes\_test.rb**

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

##

# Tests the recipes system with the simple yaml fixtures

class 
RecipesTest
 
<
 
ActionController
::
IntegrationTest

  
# load up all the fixtures

  
fixtures
 
:fruit_bases

  
set_fixture_class
 
:fruit_bases
 
=>
 
Fruit
::
Base

  
fixtures
 
:vegetable_bases

  
set_fixture_class
 
:vegetable_bases
 
=>
 
Vegetable
::
Base

  
fixtures
 
:ingredient_bases

  
set_fixture_class
 
:ingredient_bases
 
=>
 
Ingredient
::
Base

  
fixtures
 
:recipe_bases

  
set_fixture_class
 
:recipe_bases
 
=>
 
Recipe
::
Base

  
def 
test_fruit_salad_recipe_should_have_apples_and_oranges

    
r
 
=
 
Recipe
::
Base
.
find
(
:first
,
 
:conditions
 
=>
 
{
:title
 
=>
 
"
Fruit Salad
"})

    
assert
 
r

    
r
.
ingredients
.
collect
 
do
 
|
i
|

      
assert
(
i
.
kind
.
class 
==
 
Fruit
::
Apple
 
||
 
i
.
kind
.
class 
==
 
Fruit
::
Orange
)

    
end

  
end

  
def 
test_apple_pie_recipe_should_only_have_apples

    
r
 
=
 
Recipe
::
Base
.
find
(
:first
,
 
:conditions
 
=>
 
{
:title
 
=>
 
"
Apple Pie
"})

    
assert
 
r

    
r
.
ingredients
.
collect
 
do
 
|
i
|

      
assert_equal
 
Fruit
::
Apple
,
 
i
.
kind
.
class
    
end

  
end

  
def 
test_apple_should_be_in_fruit_salad_and_apple_pie

    
a
 
=
 
Fruit
::
Apple
.
find
(
:first
)

    
# there are 3 recipes but check that the through across the polymorphic

    
# ingredients is limited to fruit

    
assert_equal
 
2
,
 
a
.
recipes
.
length

    
a
.
recipes
.
each
 
do
 
|
r
|

      
assert
(
r
.
title
 
==
 
"
Apple Pie
"
 
||
 
r
.
title
 
==
 
"
Fruit Salad
")

    
end

  
end

end
```

You can explicitly run only the integration test with rake thus:

```
rake test:integration
```

Or run a specific function with the integration test such as:

```
ruby test/integration/recipes_test.rb -n test_apple_pie_recipe_should_only_have_apples
```

### Rails console

In the Rails console the following code also shows some behavior that can be
exercised with our Recipes, Ingredients, Fruits and Vegetables:

```
ruby script/console
```

Run this code in the console

```bash
# create an apple and orange ingredient

a
 
=
 
Fruit
::
Apple
.
create!

o
 
=
 
Fruit
::
Orange
.
create!

apple
 
=
 
Ingredient
::
Base
.
create!
 
:kind
 
=>
 
a

orange
 
=
 
Ingredient
::
Base
.
create!
 
:kind
 
=>
 
o

# notice that the recipe hasn't been assigned

# for this ingredient  "recipe_id"=>nil

apple
.
attributes

r
 
=
 
Recipe
::
Base
.
create!
 
:title
 
=>
 
"
Fruit Salad
"

r
.
ingredients
 
<<
 
apple

r
.
ingredients
 
<<
 
orange

# now the apple ingredient is associated with the

# recipe "recipe_id"=>1

apple
.
attributes

# look at the ingredients in this recipe, we have to go

# through the ingredient to inspect their kinds because

# we can not go through the join model from its polymorphic side

r
.
ingredients
.
collect
{|
i
|
 
i
.
kind
}

r
.
ingredients
.
collect
{|
i
|
 
i
.
kind
.
type
}

# make another recipe using the apple object

# (not the first apple ingredient) so the apple

# object can tell us which recipes it belongs to

r
 
=
 
Recipe
::
Base
.
create!
 
:title
 
=>
 
"
Apple Pie
"

apple
 
=
 
Ingredient
::
Base
.
create!
 
:kind
 
=>
 
a

r
.
ingredients
 
<<
 
apple

# and we can see that the apple instance knows which recipes

# it is included with now

a
.
recipes

a
.
recipes
.
collect
{|
r
|
 
r
.
title
}

a
.
ingredient
.
collect
{|
i
|
 
i
.
recipe
}

a
.
ingredient
.
collect
{|
i
|
 
i
.
recipe
.
title
}

# note STI finders are smart by its class, base

# returns all fruit, orange only returns oranges

Fruit
::
Base
.
find
(
:all
)

Fruit
::
Orange
.
find
(
:all
)
```

## Wrap-up

All of the source for this example as available at the following Subversion
code repository

**svn checkout http://svn.mondragon.cc/svn/recipes/trunk/ recipes**

[http://svn.mondragon.cc/svn/recipes/trunk/](./svn/recipes/trunk/http://svn.mondragon.cc/svn/recipes/trunk/index.html)

Here is my **lib/tasks/diagrams.rake** to generate Railroad’s graphs with these
Rake tasks:

```bash
rake doc:diagram:controllers   # generate controllers diagram
rake doc:diagram:models        # generate models diagram
rake doc:diagrams              # generate object graphs of models and controllers
```

```bash
namespace
 
:doc
 
do

  
namespace
 
:diagram
 
do

    
desc
 
"
generate models diagram
"

    
task
 
:models
 
do

      
sh
 
"
railroad -i -l -a -m -M | dot -Tsvg | sed 's/font-size:14.00/font-size:11.00/g' > doc/models.svg
"

    
end

    
desc
 
"
generate controllers diagram
"

    
task
 
:controllers
 
do

      
sh
 
"
railroad -i -l -C | neato -Tsvg | sed 's/font-size:14.00/font-size:11.00/g' > doc/controllers.svg
"

    
end

  
end

  
desc
 
"
generate object graphs of models and controllers
"

  
task
 
:diagrams
 
=>
 
%w(
diagram:models diagram:controllers
)

end
```

## Setup

For simplicity we’ll be using a sqlite3 database for this application, now that
we are eating fruits and vegetables we don’t need to be any fatter with an external
database server floating around. This example is done in Rails 1.2.3

Before we go on let me give you a quote that [Eric Hodel](./index.html)
has been putting in the footer of his emails:

```bash
Poor workers blame their tools. Good workers build better tools. The
best workers get their tools to do the work for them. -- Syndicate Wars
```

I’ve been learning many things from Eric and I try to emulate what he does as
a developer. Two things he always does is practice test driven development and
uses a tool he wrote called [autotest](./ZSS/Products/ZenTest/index.html)
to make TDD easier to accomplish. autotest does supports Rails out of the box.
Now on with our recipes…

This is the **config/database.yml** we’ll be using:

```bash
market: &market
  adapter: sqlite3

development:
  database: "db/development.db" 
  <<: *market

production:
  database: "db/production.db" 
  <<: *market

test:
#  database: ":memory:" 
  database: "db/test.db" 
  <<: *market
```

And we’ll start off by putting our sessions in the database and then running the migration to ensure
we have our database settings correct.

```
rake db:sessions:create
rake db:migrate
rake test
```

Now in a separate console cd into the root of your application and start autotest

```
autotest
```

it will run in your directory and whenever you save a test or code file the corresponding
unit tests will be fired for those files.

## Fruits and Vegetables models

### Fruits

Now lets make a Base of our Apples and Orange model with single table inheritance, after
the fixture is generated we need to fix where its placed as in the example. Note we are
declaring a string attribute named ‘type’ to the model generator. The string is really a
column and having a column named ‘type’ is a Rails idiom signaling single table inheritance.

```bash
ruby script/generate model Fruit::Base type:string
mv test/fixtures/fruit/fruit_bases.yml test/fixtures/
rmdir test/fixtures/fruit/
```

In your unit test test/unit/fruit/base\_test.rb you need to clue the test into
knowing which table/fixture is to be used in the namespace. Coincidently note
that your tables and fixtures will still look somewhat flat even though your model classes
have depth. After you save the test autotest should be complaining the about an error
with the SQL since you haven’t yet migrated your schema. Lets also change the default
truth test the generator runs so that autotest is testing something of value for
better test driven development

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
/../../test_helper
'

class 
Fruit::BaseTest
 
<
 
Test
::
Unit
::
TestCase

  
fixtures
 
:fruit_bases

  
set_fixture_class
 
:fruit_bases
 
=>
 
Fruit
::
Base

  
# if our notion of a valid new fruit changes then we'll catch it that here

  
def 
test_should_be_valid

    
f
 
=
 
Fruit
::
Base
.
new

    
assert
 
f
.
valid?

  
end

end
```

In your base fruit model you also have to mark which table to assign the class in its namespace

```ruby
class 
Fruit::Base
 
<
 
ActiveRecord
::
Base

  
set_table_name
 
:fruit_bases

end
```

Now migrate your schemas and then re-save your **app/models/fruit/base.rb** and you should see
autotest is happy, it doesn’t have any errors or failures.

```
rake db:migrate
```

See, autotest is happy, it doesn’t have any errors or failures

```ruby
/usr/local/bin/ruby -I.:lib:test -rtest/unit -e "%w[test/unit/fruit/base_test.rb].each { |f| require f }" | unit_diff -u
Loaded suite -e
Started
.
Finished in 0.48792 seconds.

1 tests, 1 assertions, 0 failures, 0 errors
```

Now lets generate our Apples and Oranges, but the generator is going to create
test/fixtures/fruit/fruit\_apples.yml and test/fixtures/fruit/fruit\_oranges.yml
and we won’t need those fixtures because we are using single table inheritance
and we’ll only have one fixture for all of the fruits: test/fixtures/fruit\_bases.yml
Migrations for Fruit::Orange and Fruit::Apple are also generated. We don’t need
those because we are doing single table inheritance from the Fruit::Base
Migrate the schema while you are at it.

```
ruby script/generate model Fruit::Apple
rm db/migrate/*_create_fruit_apple.rb
rm test/fixtures/fruit/fruit_apples.yml
ruby script/generate model Fruit::Orange
rm db/migrate/*_create_fruit_apple.rb
rm test/fixtures/fruit/fruit_oranges.yml
rmdir test/fixtures/fruit/
rake db:migrate
```

For simplicity of this example we want to have a Apple and a Orange in our fruits
fixture test/fixtures/fruit\_bases.yml

```
one:
  id: 1
  type: Apple
two:
  id: 2
  type: Orange
```

This is what their models and tests should look like, as you go through saving your changes
lining up the files watch what autotest is telling you. Do not react to autotest until after
you have set up apple.rb, orange.rb, apple\_test.rb, and orange\_test.rb files. See how our
inheritance is denoted in the models Fruit::Apple < Fruit::Base and Fruit::Orange < Fruit::Base

**app/models/fruit/apple.rb**

```ruby
class 
Fruit::Apple
 
<
 
Fruit
::
Base

end
```

**test/unit/fruit/apple\_test.rb**

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
/../../test_helper
'

class 
Fruit::AppleTest
 
<
 
Test
::
Unit
::
TestCase

  
fixtures
 
:fruit_bases

  
set_fixture_class
 
:fruit_bases
 
=>
 
Fruit
::
Base

  
# loading from the fixture there is only one Apple

  
def 
test_there_should_only_be_one_apple_in_the_fixture

    
assert_equal
 
1
,
 
Fruit
::
Apple
.
find
(
:all
).
length

  
end

end
```

Orange will follow the same pattern as Apple.

Once completed have a sanity check with the rake test:unit task

```
rake test:unit
```

### Vegetables

Do everything we just did for Fruits, but this time for Vegetables. We want to
end up with Vegetable::Base, Vegetable::Carrot, and Vegetable::Potato . Don’t forget
to trigger single table inheritance when you generate the base and trim out the
non single table inheritance from the Carrots and Potatoes fixtures.

## Ingredient model

Now we’ll make the Ingredient model. It will use a polymorphic association so that it can
refer to fruits and vegetables. From a Fruit::Base perspective the ingredient model will
be a join model to recipes (we’ll update our Fruit::Base code shortly to accomplish this)
From recipe’s perspective (which we will generate shortly) the ingredient model can not
be used as a join model to fruits and vegetables because the polymorphic side the of
ingredients can not be used in this manner.

Generate the model with ‘kind’ being the name used in the polymorphic idiom (kind\_id, kind\_type)
for heterogeneous ingredients and recipe\_id used to join a kind of ingredient (fruit, vegetable, etc.)
back to the recipe that uses it.

```bash
ruby script/generate model Ingredient::Base kind_id:integer kind_type:string recipe_id:integer
mv test/fixtures/ingredient/ingredient_bases.yml test/fixtures/ingredient_bases.yml
rmdir test/fixtures/ingredient/
```

**app/models/ingredient/base.rb**

```ruby
##

# A polymorphic model to associate different kinds of

# specific ingredients with a recipe.  The joining nature

# of the ingredient is one way from its kind to the recipe.

# The recipe cannot go through the ingredient to its kind

# due to a limitation in the polymorphic model.

class 
Ingredient::Base
 
<
 
ActiveRecord
::
Base

  
set_table_name
 
:ingredient_bases

  
belongs_to
 
:kind
,
 
:polymorphic
 
=>
 
true

  
belongs_to
 
:recipe
,
 
:class_name
 
=>
 
"
Recipe::Base
",
 
:foreign_key
 
=>
 
"
recipe_id
"

end
```

There is not anything of significance about the polymorphic declaration of the Ingredient model.
However since the Recipe is itself in a namespace we need to help ActiveRecord with the recipe
association declaring the class\_name of the recipe and the foreign key to it.

Don’t forget to write a unit test for you Ingredient model.

We also need to update the basic fruit and vegetable base models.

Here is the updated **app/models/fruit/base.rb**

```ruby
##

# A fruit base class that uses single table inheritance.

# Specific kinds of fruits should inherit from this class.

# A fruit has ingredients as join a model through which

# recipes that include the fruit can be found.

class 
Fruit::Base
 
<
 
ActiveRecord
::
Base

  
set_table_name
 
:fruit_bases

  
has_many
 
:ingredient
,
 
:class_name
 
=>
 
'
Ingredient::Base
',

           
:foreign_key
 
=>
 
:kind_id
,
 
:conditions
 
=>
 
"
kind_type LIKE 'Fruit::%'
"

  
has_many
 
:recipes
,
 
:through
 
=>
 
:ingredient
,
 
:uniq
 
=>
 
true

end
```

Notice that the fruit base has many ingredients. But because ingredients are polymorphic
(has an kind\_id column and a kind\_type column) the fruit base needs to declare the foreign key
that the ingredient uses to refer to it and what the kind\_type column will look like when
an ingredient is pointing to fruit. Once that is established then the ingredient model can
be used as a join model which we go through to get to the recipe that includes this kind of
ingredient.

Update your vegetable base model accordingly.

## Recipe model

Now lets generate the recipe model. Its using single table inheritance and we’ll give
each recipe a title so this is what our generation looks like. Don’t forget to
flatten the fixtures again.

```bash
ruby script/generate model Recipe::Base type:string title:string
mv test/fixtures/recipe/recipe_bases.yml test/fixtures/recipe_bases.yml
rmdir test/fixtures/recipe/
```

**app/models/recipe/base.rb**

```ruby
class 
Recipe::Base
 
<
 
ActiveRecord
::
Base

  
set_table_name
 
:recipe_bases

  
has_many
 
:ingredients
,
 
:class_name
 
=>
 
'
Ingredient::Base
',
 
:foreign_key
 
=>
 
:recipe_id

  
# If we could go through ingredients to their kinds this is how we would make

  
# the association.  However polymorphic models cannot be used as a join model

  
# when the join is towards the heterogeneous type referenced by the model

  
# has_many :kinds, :through => :ingredients

end
```

Again, we need to clue AR in to which ingredient model we are associating with and what the foreign key
used. Don’t for get to write your tests.

## Runtime

### Integration test

Be sure to check out the source code of the example. It has an integration test that runs the
model through its paces using predefined fixtures. This is the test

**test/integration/recipes\_test.rb**

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

##

# Tests the recipes system with the simple yaml fixtures

class 
RecipesTest
 
<
 
ActionController
::
IntegrationTest

  
# load up all the fixtures

  
fixtures
 
:fruit_bases

  
set_fixture_class
 
:fruit_bases
 
=>
 
Fruit
::
Base

  
fixtures
 
:vegetable_bases

  
set_fixture_class
 
:vegetable_bases
 
=>
 
Vegetable
::
Base

  
fixtures
 
:ingredient_bases

  
set_fixture_class
 
:ingredient_bases
 
=>
 
Ingredient
::
Base

  
fixtures
 
:recipe_bases

  
set_fixture_class
 
:recipe_bases
 
=>
 
Recipe
::
Base

  
def 
test_fruit_salad_recipe_should_have_apples_and_oranges

    
r
 
=
 
Recipe
::
Base
.
find
(
:first
,
 
:conditions
 
=>
 
{
:title
 
=>
 
"
Fruit Salad
"})

    
assert
 
r

    
r
.
ingredients
.
collect
 
do
 
|
i
|

      
assert
(
i
.
kind
.
class 
==
 
Fruit
::
Apple
 
||
 
i
.
kind
.
class 
==
 
Fruit
::
Orange
)

    
end

  
end

  
def 
test_apple_pie_recipe_should_only_have_apples

    
r
 
=
 
Recipe
::
Base
.
find
(
:first
,
 
:conditions
 
=>
 
{
:title
 
=>
 
"
Apple Pie
"})

    
assert
 
r

    
r
.
ingredients
.
collect
 
do
 
|
i
|

      
assert_equal
 
Fruit
::
Apple
,
 
i
.
kind
.
class
    
end

  
end

  
def 
test_apple_should_be_in_fruit_salad_and_apple_pie

    
a
 
=
 
Fruit
::
Apple
.
find
(
:first
)

    
# there are 3 recipes but check that the through across the polymorphic

    
# ingredients is limited to fruit

    
assert_equal
 
2
,
 
a
.
recipes
.
length

    
a
.
recipes
.
each
 
do
 
|
r
|

      
assert
(
r
.
title
 
==
 
"
Apple Pie
"
 
||
 
r
.
title
 
==
 
"
Fruit Salad
")

    
end

  
end

end
```

You can explicitly run only the integration test with rake thus:

```
rake test:integration
```

Or run a specific function with the integration test such as:

```
ruby test/integration/recipes_test.rb -n test_apple_pie_recipe_should_only_have_apples
```

### Rails console

In the Rails console the following code also shows some behavior that can be
exercised with our Recipes, Ingredients, Fruits and Vegetables:

```
ruby script/console
```

Run this code in the console

```bash
# create an apple and orange ingredient

a
 
=
 
Fruit
::
Apple
.
create!

o
 
=
 
Fruit
::
Orange
.
create!

apple
 
=
 
Ingredient
::
Base
.
create!
 
:kind
 
=>
 
a

orange
 
=
 
Ingredient
::
Base
.
create!
 
:kind
 
=>
 
o

# notice that the recipe hasn't been assigned

# for this ingredient  "recipe_id"=>nil

apple
.
attributes

r
 
=
 
Recipe
::
Base
.
create!
 
:title
 
=>
 
"
Fruit Salad
"

r
.
ingredients
 
<<
 
apple

r
.
ingredients
 
<<
 
orange

# now the apple ingredient is associated with the

# recipe "recipe_id"=>1

apple
.
attributes

# look at the ingredients in this recipe, we have to go

# through the ingredient to inspect their kinds because

# we can not go through the join model from its polymorphic side

r
.
ingredients
.
collect
{|
i
|
 
i
.
kind
}

r
.
ingredients
.
collect
{|
i
|
 
i
.
kind
.
type
}

# make another recipe using the apple object

# (not the first apple ingredient) so the apple

# object can tell us which recipes it belongs to

r
 
=
 
Recipe
::
Base
.
create!
 
:title
 
=>
 
"
Apple Pie
"

apple
 
=
 
Ingredient
::
Base
.
create!
 
:kind
 
=>
 
a

r
.
ingredients
 
<<
 
apple

# and we can see that the apple instance knows which recipes

# it is included with now

a
.
recipes

a
.
recipes
.
collect
{|
r
|
 
r
.
title
}

a
.
ingredient
.
collect
{|
i
|
 
i
.
recipe
}

a
.
ingredient
.
collect
{|
i
|
 
i
.
recipe
.
title
}

# note STI finders are smart by its class, base

# returns all fruit, orange only returns oranges

Fruit
::
Base
.
find
(
:all
)

Fruit
::
Orange
.
find
(
:all
)
```

## Wrap-up

All of the source for this example as available at the following Subversion
code repository

**svn checkout http://svn.mondragon.cc/svn/recipes/trunk/ recipes**

[http://svn.mondragon.cc/svn/recipes/trunk/](./svn/recipes/trunk/http://svn.mondragon.cc/svn/recipes/trunk/index.html)

Here is my **lib/tasks/diagrams.rake** to generate Railroad’s graphs with these
Rake tasks:

```bash
rake doc:diagram:controllers   # generate controllers diagram
rake doc:diagram:models        # generate models diagram
rake doc:diagrams              # generate object graphs of models and controllers
```

```bash
namespace
 
:doc
 
do

  
namespace
 
:diagram
 
do

    
desc
 
"
generate models diagram
"

    
task
 
:models
 
do

      
sh
 
"
railroad -i -l -a -m -M | dot -Tsvg | sed 's/font-size:14.00/font-size:11.00/g' > doc/models.svg
"

    
end

    
desc
 
"
generate controllers diagram
"

    
task
 
:controllers
 
do

      
sh
 
"
railroad -i -l -C | neato -Tsvg | sed 's/font-size:14.00/font-size:11.00/g' > doc/controllers.svg
"

    
end

  
end

  
desc
 
"
generate object graphs of models and controllers
"

  
task
 
:diagrams
 
=>
 
%w(
diagram:models diagram:controllers
)

end
```
