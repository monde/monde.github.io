---
title: "decoding email attachments with ActionMailer::Base receive"
date: 2006-12-30
categories: [web2.0, Rails, Nuby Rails]
---

There are lots of references that say you can decode images and other media attachements in email using the **receive** method of **ActionMailer::Base**

Ruby On Rails Wiki is one: [HowToReceiveEmailsWithActionMailer](./rails/pages/HowToReceiveEmailsWithActionMailer/index.html).

[Rails Recipes](./titles/fr_rr/index.html) Recipe #68 “Testing Incoming Mail” is another.

But those references and many others on the internet don’t show you how to really do it.

Here’s how its done …

The key is to use the TMail::Mail email object’s parts to do your work.
Use the mailer generator to stub out your code:

```
ruby script/generate mailer HelloWorldMail
      exists  app/models/
      create  app/views/hello_world_mail
      exists  test/unit/
      create  test/fixtures/hello_world_mail
      create  app/models/hello_world_mail.rb
      create  test/unit/hello_world_mail_test.rb
```

The full files in my example are contained in this bzip archive: [hello-world-mail.tar.bz2](./tutorials/ruby/hello-world-mail.tar.bz2)

See the hello-world.mail test fixture. It contains a real email file with a ruby logo image file as an attachment. The file goes in the hello\_world\_mail test fixture directory: **test/fixtures/hello\_world\_mail/hello-world.mail**

This is the snippet of code in the unit test that will have the HelloWolrdMail parse that raw file into a TMail::Mail object which is passed into the receive method:

```ruby
  
def 
test_hello_world

      
email_text
 
=
 
read_fixture
('
hello-world.mail
').
join

      
HelloWorldMail
.
receive
(
email_text
)

  
end
```

HelloWolrdMail decodes the mail and places files into the ‘tmp’ directory in your Rails root.

Here is all of the code of the HelloWolrdMail ActionMailer::Base so you don’t have to unzip the archive. The real work is to enumerate over the parts of the mail and then dump the decoded body to disk. TMail auto-magically decodes the content ecoding (7bit, 8bit, quoted-printable, base64, binary). When TMail parses out the attachments of a mail it doesn’t treat a text/plain part as a part. It does parse all of the content to parts but leaves out the original file name. So this is how I get the best of both worlds.

The text of the mail will be contained in #{RAILS\_ROOT}/tmp/1.txt and the ruby-lang.org logo that was attached to the mail will be contained in #{RAILS\_ROOT}/tmp/ruby.gif

**Update 07/10/2007** See DANG Zhengfa’s post in the comments section for a cleaner code. My example was written when I was a bit more of a n00b. Also my code was dealing TMail before it was fixed in the ActionMailer in the latest 1.3.3 release.

**Update 08/01/2007**

Cleaned up the code with better Ruby idioms, when I first wrote it I was still unlearning Java. As PJ says uses attachment\_fu if you just want to get at the content quickly. This code works with Rails 1.2.3 / ActionMailer 1.3.3 which automatically decodes the attachment’s content encoding.

```ruby
class 
HelloWorldMail
 
<
 
ActionMailer
::
Base

  
# email is a TMail::Mail

  
def 
receive
(
email
)

    
#email.attachments are TMail::Attachment

    
#but they ignore a text/mail parts.

    
email
.
parts
.
each_with_index
 
do
 
|
part
,
 
index
|

      
filename
 
=
 
part_filename
(
part
)

      
filename
 
||=
 
"
#{index}
.
#{ext(part)}
"

      
filepath
 
=
 
"
#{RAILS_ROOT}
/tmp/
#{filename}
"

      
puts
 
"
WRITING: 
#{filepath}
"

      
File
.
open
(
filepath
,
File
::
CREAT
|
File
::
TRUNC
|
File
::
WRONLY
,
0644
)
 
do
 
|
f
|

        
f
.
write
(
part
.
body
)

      
end

    
end

  
end

  
# part is a TMail::Mail

  
def 
part_filename
(
part
)

    
# This is how TMail::Attachment gets a filename

    
file_name
 
=
 
(
part
['
content-location
']
 
&&

      
part
['
content-location
'].
body
)
 
||

      
part
.
sub_header
("
content-type
",
 
"
name
")
 
||

      
part
.
sub_header
("
content-disposition
",
 
"
filename
")

  
end

  
CTYPE_TO_EXT
 
=
 
{

    
'
image/jpeg
'
 
=>
 
'
jpg
',

    
'
image/gif
'
  
=>
 
'
gif
',

    
'
image/png
'
  
=>
 
'
png
',

    
'
image/tiff
'
 
=>
 
'
tif
'

  
}

  
def 
ext
(
 
mail
 
)

    
CTYPE_TO_EXT
[
mail
.
content_type
]
 
||
 
'
txt
'

  
end

end
```

The key is to use the TMail::Mail email object’s parts to do your work.
Use the mailer generator to stub out your code:

```
ruby script/generate mailer HelloWorldMail
      exists  app/models/
      create  app/views/hello_world_mail
      exists  test/unit/
      create  test/fixtures/hello_world_mail
      create  app/models/hello_world_mail.rb
      create  test/unit/hello_world_mail_test.rb
```

The full files in my example are contained in this bzip archive: [hello-world-mail.tar.bz2](./tutorials/ruby/hello-world-mail.tar.bz2)

See the hello-world.mail test fixture. It contains a real email file with a ruby logo image file as an attachment. The file goes in the hello\_world\_mail test fixture directory: **test/fixtures/hello\_world\_mail/hello-world.mail**

This is the snippet of code in the unit test that will have the HelloWolrdMail parse that raw file into a TMail::Mail object which is passed into the receive method:

```ruby
  
def 
test_hello_world

      
email_text
 
=
 
read_fixture
('
hello-world.mail
').
join

      
HelloWorldMail
.
receive
(
email_text
)

  
end
```

HelloWolrdMail decodes the mail and places files into the ‘tmp’ directory in your Rails root.

Here is all of the code of the HelloWolrdMail ActionMailer::Base so you don’t have to unzip the archive. The real work is to enumerate over the parts of the mail and then dump the decoded body to disk. TMail auto-magically decodes the content ecoding (7bit, 8bit, quoted-printable, base64, binary). When TMail parses out the attachments of a mail it doesn’t treat a text/plain part as a part. It does parse all of the content to parts but leaves out the original file name. So this is how I get the best of both worlds.

The text of the mail will be contained in #{RAILS\_ROOT}/tmp/1.txt and the ruby-lang.org logo that was attached to the mail will be contained in #{RAILS\_ROOT}/tmp/ruby.gif

**Update 07/10/2007** See DANG Zhengfa’s post in the comments section for a cleaner code. My example was written when I was a bit more of a n00b. Also my code was dealing TMail before it was fixed in the ActionMailer in the latest 1.3.3 release.

**Update 08/01/2007**

Cleaned up the code with better Ruby idioms, when I first wrote it I was still unlearning Java. As PJ says uses attachment\_fu if you just want to get at the content quickly. This code works with Rails 1.2.3 / ActionMailer 1.3.3 which automatically decodes the attachment’s content encoding.

```ruby
class 
HelloWorldMail
 
<
 
ActionMailer
::
Base

  
# email is a TMail::Mail

  
def 
receive
(
email
)

    
#email.attachments are TMail::Attachment

    
#but they ignore a text/mail parts.

    
email
.
parts
.
each_with_index
 
do
 
|
part
,
 
index
|

      
filename
 
=
 
part_filename
(
part
)

      
filename
 
||=
 
"
#{index}
.
#{ext(part)}
"

      
filepath
 
=
 
"
#{RAILS_ROOT}
/tmp/
#{filename}
"

      
puts
 
"
WRITING: 
#{filepath}
"

      
File
.
open
(
filepath
,
File
::
CREAT
|
File
::
TRUNC
|
File
::
WRONLY
,
0644
)
 
do
 
|
f
|

        
f
.
write
(
part
.
body
)

      
end

    
end

  
end

  
# part is a TMail::Mail

  
def 
part_filename
(
part
)

    
# This is how TMail::Attachment gets a filename

    
file_name
 
=
 
(
part
['
content-location
']
 
&&

      
part
['
content-location
'].
body
)
 
||

      
part
.
sub_header
("
content-type
",
 
"
name
")
 
||

      
part
.
sub_header
("
content-disposition
",
 
"
filename
")

  
end

  
CTYPE_TO_EXT
 
=
 
{

    
'
image/jpeg
'
 
=>
 
'
jpg
',

    
'
image/gif
'
  
=>
 
'
gif
',

    
'
image/png
'
  
=>
 
'
png
',

    
'
image/tiff
'
 
=>
 
'
tif
'

  
}

  
def 
ext
(
 
mail
 
)

    
CTYPE_TO_EXT
[
mail
.
content_type
]
 
||
 
'
txt
'

  
end

end
```
