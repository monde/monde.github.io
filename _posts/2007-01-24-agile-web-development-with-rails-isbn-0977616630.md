---
title: "Agile Web Development with Rails (ISBN 0977616630)"
date: 2007-01-24
categories: [web2.0, Rails, Nuby Rails, Books]
tags: [books, rails, web2.0]
---

|  |  |
| --- | --- |
| I’ve started reading the second edition of [Agile Web Development with Rails](./titles/rails/index.html) . I’m going to try something different and append my notes from each chapter to his blog entry as I read them. I bought this book from The Pragmatic Programmers site with the PDF copy of the book. I like having the PDF copies of their books (I currently own the [PickAxe book](./titles/ruby/index.html) , the Agile Rails book, and the [Rail Recipes](./titles/fr_rr/index.html) books) so I can reference them without having to search the internet or crack open my real book for a discussion of a question I might have. |  |

## 01/23/2006

I started by reading the Contents to get a feel for the layout of the book. During my reading session I knew I would at least read the Introduction. But during my next reading session I’m going to jump back to Appendix A “Introduction to Ruby” and read that. I read the PickAxe book last fall but I feel like I need a refresher to Ruby coding. I would like to think of myself as a beginning Ruby programmer that is learning Ruby by learning Rails. So the refresher is going to help with that goal. The next Ruby book I read will either be “The Ruby Way” or another reading of PickAxe. Anyway, back to my “Agile Web Development with Rails” notes …

### Notes from the Introduction

- Rails is a framework that is becoming state of the art for Web 2.0 applications.
- Rails is [MVC](./wiki/Model-view-controller/index.html) (Model, View, Controller compound desing pattern) based with unit and functional testing integral to the framework.
- Rails is structured by convention over configuration. This makes programs shorter, ensures [DRY](./wiki/DRY/index.html) (Don’t Repeat Yourself) convention, and allows for a common/shared knowledge among developers.
- Rails is helping define new web standards which helps in applying features such as [AJAX](./wiki/AJAX/index.html) (Asynchronous JavaScript and XML) and [RESTful](./wiki/Representational_State_Transfer/index.html) (Representational State Transfer) interfaces.
- Rails was extracted from a real world application. That is a means of creating a framework. This allows a basic Rails setup is a starting point for an application that is already halfway implemented.
- Rails is agile and favors:
  - Individuals and interactions over processes and tools
  - Working software over comprehensive documentation
  - Customer collaboration over contract negotiation
  - Responding to change over following a plan
- Rails is driven by collaboration and change based on needs

The chapter ends with notes about the conventions used in the layout of the book. And acknowlegements to the Rails community and the book reviewers.

## 01/28/2006

I jumped back to “Appendix A – Introduction to Ruby” to brush up my Ruby language knowledge. It was a good tune up. I had read the PickAxe book last fall and reading this enhanced the practical knowledge I have gained since then.

### Notes from Appendix A – Introduction to Ruby

There was a reminder that most of this section was derived from chapter 2 of the PickAxe book.

**Everything is an object.** A class is a combination of state and methods to access and modify the state. In informal OO speak an object is a class instance. Classes are created by calling a constructor, in Ruby the constructor is called *new* and it have parameters (or not). An instantiated class has instance variables and methods and a class has class variables and methods. Instance methods are invoked by sending a message to the object.

**Ruby Names**, there are local variables, instance variables, class variables, and global variables. Ruby uses symbols as well, a symbol can be thought of as string literals that are converted into constants. Or a symbol refers to the thing named by the symbol name.

**Methods** Forms of methods are:

```ruby
def foo; end
def foo
end
def foo()
end
```

The return value from a method is its last evaluated expression.

**Strings** are constructed with a single quote, double quote, and the string literal block %{ } . Very little processing is done on a single quoted string whereas expression interpolation is performed on a double quoted and sting literal forms of a string.

**Class Names** begin with a upper case letter (by convention). There are class and instance methods. Pre-fixing *self* to a method declaration makes the method a class level method.

**Instance Variables** of an object start with *@* and are available to all instance methods. Instance variables are not directly available outside of the class.

**Module** provides convenience methods *attr\_accessor*, *attr\_reader*, *attr\_writer* to create getters and setters on instance variables. Modules are like classes but you do not create objects from modules. Modules define a namespace. They define methods at won’t clash if used elsewhere. Modules can be mixed into classes so that functionality can be reused without inheritance. Rails helpers are written as modules. A view template gets its helper view mixed in to it.

**Arrays and Hashes** are indexed collections. Arrays are indexed by numbers as keys, hashes use objects as keys. Both can hold objects of different types.

```
[1,2,3,4]
```

is an array literal,

```
{foo=>bar,:hello=>'world'}
```

is a hash literal. Hash keys are unique. Rails typically use symbols as keys in hashes. When a hash doesn’t hold a key it returns nil. Ruby treats nil as false in conditional statements. Hashes can be parameters to a method and don’t need to use their literal {} braces if they are the last argument to the method (Rails makes use of that language feature frequently).

**nil** is a No-op object, and Ruby treats nil as false in conditional statement.

**Control structures** Common conditionals are if, elsif, else, and common looping constructs are for and while, and blocks attached to iterators. Both conditionals and loops can be used as statement modifiers so that a statement is only executed within context of the control structure:

```
a=foo if a > 2
a=a+2 while a < 100
```

**Regular Expressions** Literal patterns are delimited by / ... / or %r{ ... } . Regex can be used to test strings with the match operator =~ . The match returns nil if no match is found, or the string index of where the match starts. This lends itself to the match operator being used in conditional statements.

**Blocks** Block literals delimited by { ... } and *do … end* . The appear after a call to a method. The method can invoke the block if it calls yield. They are often used with iterators.

**Exceptions** Are objects of class Exception or one of its derivatives. The *raise* method causes an exception to be raised. Exceptions are handed in *begin, rescue, else, end* blocks. The exception class is the argument to the rescue method and its instance can be gathered with the => operator.

**Marshalling** is converting an object into a stream. Anonymous classes and modules cannot be marshalled and will cause a TypeError if an attempt to marshal them is made. Rails stores session data via marshalling. Objects that contain specific runtime data such as IO objects can not be marshalled.

**Iterative Ruby – irb** irb is a shell that can execute ruby code interactively and is useful to inspect how code snippets will behave.

**Ruby Idioms** Some ruby idioms are, by convention methods with ! at the end of their name modify the receiver. Methods with ? at the end of their name typically return a boolean. *a||b* is ternary like structure for assignment, *a\_ is evaluated first, if nil or false \_b* is evaluated. *self* refers to the class not the instance. *self.new* will evaluate to the level of inheritance from which the evaluation is made.

**Documentation** Use RDoc to generate HTML format and *ri* format documentation for ruby classes. Use a web browser to view the HTML documentation use the **ri** command to view the ri format documentation.

## 02/01/2007

### Notes from Chapter 2 Rails Architecture

Rails has defined constraints to its architecture and it implements the Model View Controller pattern. Constraints and patterns makes it easier to create applications.

Model – Is responsible for maintaining the state of an application. model contains business rules and acts as gatekeeper and datastore.

View – Generates the suer interface based on data in the model.

Controller – Orchestrates the application. Receives outside events (user input), interacts with the model and pass information to the view to render.

Rails uses intelligent/defined defaults and this results in applications that favor convention over configuration. A request is handled by the rails router. The router decides which controller to send the request to. Specifically, the request is sent to a method of the controller class which is called an “action” in the context of rails. The path that makes up the request contains other information, such as an ID that corresponds to a data object and the router processes the path encoding as well. The encoding of the request implies a state of the application. The encoding of the application state is a basis of REST – Representational State Transfer.

Model -> ActiveRecord is the system that represents rows and tables in a database as classes and class instances (objects) in the application. ActiveRecord is object centric rather than database centric. That means an application interacts with objects that are represented in the database. This lends itself to the OO principle of encapsulating what varies, another way to say that is DRY – Don’t Repeat Yourself. DRY helps eliminate duplicate code, code duplication lends itself to errors because it is harder to maintain as features are added.

ActiveRecord is the Rails ORM -> Object Relational Mapper. A class represents a table, and objects of the class represent rows from the table. Class level methods represent table level methods. Object level methods represent row level operations (i.e. change a value). A Rails table, by convention, is named in lower case plural form such as “phones” and the class for the table is named in singular upper case form such as “Phone”.

View & Controller -> ActionPack is the Rails View and Controller.

View -> Dynamic content in rails is created with templates which are typically rhtml. rhtml files contain ERb -> embedded ruby so that ruby code can be executed in the template. The view has other templating schemes such as rxml for XML documents and rjs for java script fragments.

Controller -> coordinates interaction between the user, the views, and the model. The controller is structured and operates by convention allowing the developer to concentrate on application level development. The controller routes external requests to internal actions. In manages caching strategies of the views. It manages helper modules for the view, and manages sessions for application state.

## 02/08/2007

### Notes from Chapter 3 – Installing Rails

Most developers use the command line. Use version control, checking in source often. Use a text based IDE that colorize code and auto-tab. MySQL tidbits.

### Notes from Chapter 4 – Simple Rails Application

```bash
$ rails myproject
```

creates a rails project named “myproject”

The rails generator lays out a directory structure. Generator/helper scripts are in the script/ directory and file that make up the application (model, view, controller) are in the app/ directory.

```bash
$ ruby script/server
```

runs WEBrick web server in development mode (the default), the “-e” argument can be used to explicitly set the run mode of development, test, production.

In development mode WEBrick reloads all files with each request. Use a generator script to generator different rails components (controllers, scaffold, etc.)

```bash
$ ruby script/generate controller Foo
```

the name passed to the controller task is the real desired class name.

In the most simple case rails maps a controller and action to a URI as ”/controller/action/id”. Assume Foo controller has “bar” action, then its URI is ”/foo/bar”. View for the bar action of the Foo controller is at app/views/foo/bar.rhtml . The master layout for the Foo controller is at app/views/layouts/foo.rhtml .
ERb goes in rhtml files. Controller instance variables (i.e. @myvar) are available to the view in its ERb <= @myvar %> to print. -> at the end of an ERb statement removes newline endings. <= ... %> outputs text and < ... %> executes code only.

Views have helper methods, a common one is h() which escapes characters properly for viewing in a webbrowser. Set variables in a controller, only print or enumerate those variables in the view. Views are linked to its controller actions with the “link\_to” helper method. Helpers make lots of use of symbol => object mappings as parameters to the helper method.

### Notes from Chapter 5 – Depot Application part 2

Initial guesses about an application usually turn out wrong. Use incremental development.

Define use cases, statements about how some entity uses a system. Define roles like “buyer” and “seller”.

Diagram some simple page flows.

Define a simple data diagram to illustrate data relationships.

Change your design as needed, design should serve application developer, not visa versa.

### Notes from Chapter 6 – Creating a new application.

Rails generator:

```bash
$ rails myapp
```

generates directory structure and initial configuration files.

Setup database connection configuration in conf/database.yml

Start using db migration upfront:

```bash
$ rake db:migrate
```

Create a model and table:

```bash
$ ruby script/generate model MyModel
```

a migration is created at db/migrate/001\_create\_mymodel.rb
Edit the migration to specify the columns (class attributes) of the new model then migrate changes again:

```bash
$ rake db:migrate
```

Generate a controller

```bash
$ ruby script/generate controller MyController
```

use scaffold to dynamically generate CRUD (create, read, update, delete) views by wiring controller to a model, i.e.

```ruby
class MyController < ApplicationController
  scaffold :mymodel
end
```

Add new columns with db migration. Remember that defining self.up and self.down in your ActiveRecord::Migration specifies modifications and how to revert modifications to the table/model respectively. Also, migration files start with three digits and are fired in order, i.e. 000\_a.rb … 001\_b.rb … 089\_foo.rb

Model classes that are children of ActiveRecord::Base have validation methods for their data, e.g. validates\_presence\_of, validates\_numericality\_of, validates\_uniqueness\_of, validates\_format\_of, and others. A child should override the “validate” method if special consideration should needs to be applied to the model. “validate” will be called the object is saved, “errors” can be added in validate which stops the object from being saved.

Static scaffold can be generated with:

```bash
$ ruby script/generate scaffold mymodel
```

the CRUD view files for that scaffold are written to disk and can be modified.

Views have access variables (instance) set in the controller.

Setup testing data with data only migration.

Master layout for a model is in app/views/layouts.

There a number of view helpers such as: “cycle” to alternate row colors via css, “h” to properly escape HTML, and “truncate” to clip text.

link\_to should be “idempotent” i.e. a GET request should generate the same result every time it is executed. Pass the parameter

```
:method => post
```

to link\_to if a link will modify the state of an application (keeping you app idempotent).

In the master layout use <%= yield :layout %> to inject controller action output into layout.

## 02/15/2007

### Notes from Chapter 7 – Catalog

Controller generator can also create actions as a convenience:

```bash
$ ruby script/generate controller myclass do_foo add_bar
```

Define class level finder in the model, avoid calling a model’s find method in the controller. This keeps the controller a consumer of the search, not a producer and consumer of the search.

Add stylesheets to layout with style\_sheet\_link\_tag

In layout yield to a controller’ output with <%= yeild :layout %>. The old way is to output the variable @content\_for\_layout .

Output helper number\_to\_currency

Use css

```
display: inline;"
```

to have a submit button not wrap lines.

### Notes from Chapter 8 – Cart

Sessions can be stored in files or the db

*session* is a hash to access object stored in a session.

Default session are serialized to disk.

Set sessions to reside in the DB with:

```bash
$ rake db:sessions:create
$ rake db:migrate
```

Accessing a session

```
session[:foo] = Bar.new
```

use symbols to key into the session hash.

*params* hash holds parameters passed into the application.

In forms make the object of the form be the :id argument e.g.
<%= button\_to “Add Bar”, :action => :add\_fooo, :id => bar %>
the id of the bar will be used. Now params[:id] will hold the id of bar for something like bar = Bar.find(params[:id]) . id of bar is called the primary key for bar.

Here’s cool finder for arrays to remember:

```
item_of_interest = @myarr.find{|foo| foo.bar == somebar}
```

Rake command to clear sessions while developing:

```
rake db:sessions:clear
```

see Ch. 27 p. 629 about sweeping sessions.

Only store simple data in the session like strings and numbers.

Error handling – A good strategy: log error, post message, return to previous state. Use the *flash* has to set the message, e.g.

```
flash[:notice] = 'Bar'
```

Example of a finder that handles an error and flashes a message:

```
begin
  foo = Foo.find(params[:id])
rescue ActiveRecord::RecordNotFound
  logger.error("Bad Foo!")
  flash[:notice] = "Bad Foo!" 
  redirect_to :action => :index
else
  @bar.add_foo(foo)
end
```

Display flash:

```bash
<% if flash[:notice] -%>
  <%= flash[:notice] %>
<% end -%>

Also see global error handler that mails admins on page 629.
              
```

## 01/23/2006

I started by reading the Contents to get a feel for the layout of the book. During my reading session I knew I would at least read the Introduction. But during my next reading session I’m going to jump back to Appendix A “Introduction to Ruby” and read that. I read the PickAxe book last fall but I feel like I need a refresher to Ruby coding. I would like to think of myself as a beginning Ruby programmer that is learning Ruby by learning Rails. So the refresher is going to help with that goal. The next Ruby book I read will either be “The Ruby Way” or another reading of PickAxe. Anyway, back to my “Agile Web Development with Rails” notes …

### Notes from the Introduction

- Rails is a framework that is becoming state of the art for Web 2.0 applications.
- Rails is [MVC](./wiki/Model-view-controller/index.html) (Model, View, Controller compound desing pattern) based with unit and functional testing integral to the framework.
- Rails is structured by convention over configuration. This makes programs shorter, ensures [DRY](./wiki/DRY/index.html) (Don’t Repeat Yourself) convention, and allows for a common/shared knowledge among developers.
- Rails is helping define new web standards which helps in applying features such as [AJAX](./wiki/AJAX/index.html) (Asynchronous JavaScript and XML) and [RESTful](./wiki/Representational_State_Transfer/index.html) (Representational State Transfer) interfaces.
- Rails was extracted from a real world application. That is a means of creating a framework. This allows a basic Rails setup is a starting point for an application that is already halfway implemented.
- Rails is agile and favors:
  - Individuals and interactions over processes and tools
  - Working software over comprehensive documentation
  - Customer collaboration over contract negotiation
  - Responding to change over following a plan
- Rails is driven by collaboration and change based on needs

The chapter ends with notes about the conventions used in the layout of the book. And acknowlegements to the Rails community and the book reviewers.

## 01/28/2006

I jumped back to “Appendix A – Introduction to Ruby” to brush up my Ruby language knowledge. It was a good tune up. I had read the PickAxe book last fall and reading this enhanced the practical knowledge I have gained since then.

### Notes from Appendix A – Introduction to Ruby

There was a reminder that most of this section was derived from chapter 2 of the PickAxe book.

**Everything is an object.** A class is a combination of state and methods to access and modify the state. In informal OO speak an object is a class instance. Classes are created by calling a constructor, in Ruby the constructor is called *new* and it have parameters (or not). An instantiated class has instance variables and methods and a class has class variables and methods. Instance methods are invoked by sending a message to the object.

**Ruby Names**, there are local variables, instance variables, class variables, and global variables. Ruby uses symbols as well, a symbol can be thought of as string literals that are converted into constants. Or a symbol refers to the thing named by the symbol name.

**Methods** Forms of methods are:

```ruby
def foo; end
def foo
end
def foo()
end
```

The return value from a method is its last evaluated expression.

**Strings** are constructed with a single quote, double quote, and the string literal block %{ } . Very little processing is done on a single quoted string whereas expression interpolation is performed on a double quoted and sting literal forms of a string.

**Class Names** begin with a upper case letter (by convention). There are class and instance methods. Pre-fixing *self* to a method declaration makes the method a class level method.

**Instance Variables** of an object start with *@* and are available to all instance methods. Instance variables are not directly available outside of the class.

**Module** provides convenience methods *attr\_accessor*, *attr\_reader*, *attr\_writer* to create getters and setters on instance variables. Modules are like classes but you do not create objects from modules. Modules define a namespace. They define methods at won’t clash if used elsewhere. Modules can be mixed into classes so that functionality can be reused without inheritance. Rails helpers are written as modules. A view template gets its helper view mixed in to it.

**Arrays and Hashes** are indexed collections. Arrays are indexed by numbers as keys, hashes use objects as keys. Both can hold objects of different types.

```
[1,2,3,4]
```

is an array literal,

```
{foo=>bar,:hello=>'world'}
```

is a hash literal. Hash keys are unique. Rails typically use symbols as keys in hashes. When a hash doesn’t hold a key it returns nil. Ruby treats nil as false in conditional statements. Hashes can be parameters to a method and don’t need to use their literal {} braces if they are the last argument to the method (Rails makes use of that language feature frequently).

**nil** is a No-op object, and Ruby treats nil as false in conditional statement.

**Control structures** Common conditionals are if, elsif, else, and common looping constructs are for and while, and blocks attached to iterators. Both conditionals and loops can be used as statement modifiers so that a statement is only executed within context of the control structure:

```
a=foo if a > 2
a=a+2 while a < 100
```

**Regular Expressions** Literal patterns are delimited by / ... / or %r{ ... } . Regex can be used to test strings with the match operator =~ . The match returns nil if no match is found, or the string index of where the match starts. This lends itself to the match operator being used in conditional statements.

**Blocks** Block literals delimited by { ... } and *do … end* . The appear after a call to a method. The method can invoke the block if it calls yield. They are often used with iterators.

**Exceptions** Are objects of class Exception or one of its derivatives. The *raise* method causes an exception to be raised. Exceptions are handed in *begin, rescue, else, end* blocks. The exception class is the argument to the rescue method and its instance can be gathered with the => operator.

**Marshalling** is converting an object into a stream. Anonymous classes and modules cannot be marshalled and will cause a TypeError if an attempt to marshal them is made. Rails stores session data via marshalling. Objects that contain specific runtime data such as IO objects can not be marshalled.

**Iterative Ruby – irb** irb is a shell that can execute ruby code interactively and is useful to inspect how code snippets will behave.

**Ruby Idioms** Some ruby idioms are, by convention methods with ! at the end of their name modify the receiver. Methods with ? at the end of their name typically return a boolean. *a||b* is ternary like structure for assignment, *a\_ is evaluated first, if nil or false \_b* is evaluated. *self* refers to the class not the instance. *self.new* will evaluate to the level of inheritance from which the evaluation is made.

**Documentation** Use RDoc to generate HTML format and *ri* format documentation for ruby classes. Use a web browser to view the HTML documentation use the **ri** command to view the ri format documentation.

## 02/01/2007

### Notes from Chapter 2 Rails Architecture

Rails has defined constraints to its architecture and it implements the Model View Controller pattern. Constraints and patterns makes it easier to create applications.

Model – Is responsible for maintaining the state of an application. model contains business rules and acts as gatekeeper and datastore.

View – Generates the suer interface based on data in the model.

Controller – Orchestrates the application. Receives outside events (user input), interacts with the model and pass information to the view to render.

Rails uses intelligent/defined defaults and this results in applications that favor convention over configuration. A request is handled by the rails router. The router decides which controller to send the request to. Specifically, the request is sent to a method of the controller class which is called an “action” in the context of rails. The path that makes up the request contains other information, such as an ID that corresponds to a data object and the router processes the path encoding as well. The encoding of the request implies a state of the application. The encoding of the application state is a basis of REST – Representational State Transfer.

Model -> ActiveRecord is the system that represents rows and tables in a database as classes and class instances (objects) in the application. ActiveRecord is object centric rather than database centric. That means an application interacts with objects that are represented in the database. This lends itself to the OO principle of encapsulating what varies, another way to say that is DRY – Don’t Repeat Yourself. DRY helps eliminate duplicate code, code duplication lends itself to errors because it is harder to maintain as features are added.

ActiveRecord is the Rails ORM -> Object Relational Mapper. A class represents a table, and objects of the class represent rows from the table. Class level methods represent table level methods. Object level methods represent row level operations (i.e. change a value). A Rails table, by convention, is named in lower case plural form such as “phones” and the class for the table is named in singular upper case form such as “Phone”.

View & Controller -> ActionPack is the Rails View and Controller.

View -> Dynamic content in rails is created with templates which are typically rhtml. rhtml files contain ERb -> embedded ruby so that ruby code can be executed in the template. The view has other templating schemes such as rxml for XML documents and rjs for java script fragments.

Controller -> coordinates interaction between the user, the views, and the model. The controller is structured and operates by convention allowing the developer to concentrate on application level development. The controller routes external requests to internal actions. In manages caching strategies of the views. It manages helper modules for the view, and manages sessions for application state.

## 02/08/2007

### Notes from Chapter 3 – Installing Rails

Most developers use the command line. Use version control, checking in source often. Use a text based IDE that colorize code and auto-tab. MySQL tidbits.

### Notes from Chapter 4 – Simple Rails Application

```bash
$ rails myproject
```

creates a rails project named “myproject”

The rails generator lays out a directory structure. Generator/helper scripts are in the script/ directory and file that make up the application (model, view, controller) are in the app/ directory.

```bash
$ ruby script/server
```

runs WEBrick web server in development mode (the default), the “-e” argument can be used to explicitly set the run mode of development, test, production.

In development mode WEBrick reloads all files with each request. Use a generator script to generator different rails components (controllers, scaffold, etc.)

```bash
$ ruby script/generate controller Foo
```

the name passed to the controller task is the real desired class name.

In the most simple case rails maps a controller and action to a URI as ”/controller/action/id”. Assume Foo controller has “bar” action, then its URI is ”/foo/bar”. View for the bar action of the Foo controller is at app/views/foo/bar.rhtml . The master layout for the Foo controller is at app/views/layouts/foo.rhtml .
ERb goes in rhtml files. Controller instance variables (i.e. @myvar) are available to the view in its ERb <= @myvar %> to print. -> at the end of an ERb statement removes newline endings. <= ... %> outputs text and < ... %> executes code only.

Views have helper methods, a common one is h() which escapes characters properly for viewing in a webbrowser. Set variables in a controller, only print or enumerate those variables in the view. Views are linked to its controller actions with the “link\_to” helper method. Helpers make lots of use of symbol => object mappings as parameters to the helper method.

### Notes from Chapter 5 – Depot Application part 2

Initial guesses about an application usually turn out wrong. Use incremental development.

Define use cases, statements about how some entity uses a system. Define roles like “buyer” and “seller”.

Diagram some simple page flows.

Define a simple data diagram to illustrate data relationships.

Change your design as needed, design should serve application developer, not visa versa.

### Notes from Chapter 6 – Creating a new application.

Rails generator:

```bash
$ rails myapp
```

generates directory structure and initial configuration files.

Setup database connection configuration in conf/database.yml

Start using db migration upfront:

```bash
$ rake db:migrate
```

Create a model and table:

```bash
$ ruby script/generate model MyModel
```

a migration is created at db/migrate/001\_create\_mymodel.rb
Edit the migration to specify the columns (class attributes) of the new model then migrate changes again:

```bash
$ rake db:migrate
```

Generate a controller

```bash
$ ruby script/generate controller MyController
```

use scaffold to dynamically generate CRUD (create, read, update, delete) views by wiring controller to a model, i.e.

```ruby
class MyController < ApplicationController
  scaffold :mymodel
end
```

Add new columns with db migration. Remember that defining self.up and self.down in your ActiveRecord::Migration specifies modifications and how to revert modifications to the table/model respectively. Also, migration files start with three digits and are fired in order, i.e. 000\_a.rb … 001\_b.rb … 089\_foo.rb

Model classes that are children of ActiveRecord::Base have validation methods for their data, e.g. validates\_presence\_of, validates\_numericality\_of, validates\_uniqueness\_of, validates\_format\_of, and others. A child should override the “validate” method if special consideration should needs to be applied to the model. “validate” will be called the object is saved, “errors” can be added in validate which stops the object from being saved.

Static scaffold can be generated with:

```bash
$ ruby script/generate scaffold mymodel
```

the CRUD view files for that scaffold are written to disk and can be modified.

Views have access variables (instance) set in the controller.

Setup testing data with data only migration.

Master layout for a model is in app/views/layouts.

There a number of view helpers such as: “cycle” to alternate row colors via css, “h” to properly escape HTML, and “truncate” to clip text.

link\_to should be “idempotent” i.e. a GET request should generate the same result every time it is executed. Pass the parameter

```
:method => post
```

to link\_to if a link will modify the state of an application (keeping you app idempotent).

In the master layout use <%= yield :layout %> to inject controller action output into layout.

## 02/15/2007

### Notes from Chapter 7 – Catalog

Controller generator can also create actions as a convenience:

```bash
$ ruby script/generate controller myclass do_foo add_bar
```

Define class level finder in the model, avoid calling a model’s find method in the controller. This keeps the controller a consumer of the search, not a producer and consumer of the search.

Add stylesheets to layout with style\_sheet\_link\_tag

In layout yield to a controller’ output with <%= yeild :layout %>. The old way is to output the variable @content\_for\_layout .

Output helper number\_to\_currency

Use css

```
display: inline;"
```

to have a submit button not wrap lines.

### Notes from Chapter 8 – Cart

Sessions can be stored in files or the db

*session* is a hash to access object stored in a session.

Default session are serialized to disk.

Set sessions to reside in the DB with:

```bash
$ rake db:sessions:create
$ rake db:migrate
```

Accessing a session

```
session[:foo] = Bar.new
```

use symbols to key into the session hash.

*params* hash holds parameters passed into the application.

In forms make the object of the form be the :id argument e.g.
<%= button\_to “Add Bar”, :action => :add\_fooo, :id => bar %>
the id of the bar will be used. Now params[:id] will hold the id of bar for something like bar = Bar.find(params[:id]) . id of bar is called the primary key for bar.

Here’s cool finder for arrays to remember:

```
item_of_interest = @myarr.find{|foo| foo.bar == somebar}
```

Rake command to clear sessions while developing:

```
rake db:sessions:clear
```

see Ch. 27 p. 629 about sweeping sessions.

Only store simple data in the session like strings and numbers.

Error handling – A good strategy: log error, post message, return to previous state. Use the *flash* has to set the message, e.g.

```
flash[:notice] = 'Bar'
```

Example of a finder that handles an error and flashes a message:

```
begin
  foo = Foo.find(params[:id])
rescue ActiveRecord::RecordNotFound
  logger.error("Bad Foo!")
  flash[:notice] = "Bad Foo!" 
  redirect_to :action => :index
else
  @bar.add_foo(foo)
end
```

Display flash:

```bash
<% if flash[:notice] -%>
  <%= flash[:notice] %>
<% end -%>

Also see global error handler that mails admins on page 629.
              
```
