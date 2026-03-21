---
title: "wrapping processes in IO.popen and festivaltts4r"
date: 2007-10-26
categories: [Ruby, Rails, Gems]
tags: [festivaltts4r, gems, rails, ruby]
---

There is a cool gem called [Festival TTS for Ruby](./projects/festivaltts4r/index.html) . What it does is take text, pass it into the  [The Festival Speech Synthesis System](./projects/festival/index.html) , then transform the WAV from Festival into an MP3. festivaltts4r provides a programming interface to use its functionality in an application. The project includes a Flash media player so that you can use festivaltts4r easily in a Rails application. [Listen](./index.html) to their example Rails application. To use the Flash player you need to check out the project as a plugin to your Rails app like so:

```
ruby script/plugin install svn+ssh://rubyforge.org/var/svn/festivaltts4r/plugins/festivaltts_on_rails
```

festival4r.rb adds #to\_speech and #to\_mp3 methods to String and each make a simple call to Kernel#system to execute their programs. That is a quick and easy approach as #system returns false on failure, true on success, and the exit status of the process in $?

However, many processes output text as the they are being executed such as status or error messages. Before I came across festivaltts4r I had actually written my own kind of festivaltts4r for a Rails project. My approach is to capture all of the output of the process and if there is an error returned from the process use the output as the message for an Exception. The process is executed by IO.popen which also captures the text of the process. Process.wait is then called to ensure to wait for the process to finish (beware of hung processes!). Eric Hodel [suggested the use of IO.popen](./pipermail/ruby/2007-February/003197.html) in this manner.

Here is the model I used for my implementation of festivaltts4r. The model uses Single Table Inheritance, look at the schema annotation for clues about the overall strategy/pattern of my MediaTransform model. Also note that MediaTransformError is just a custom Exception my application raises and catches as a part of its behavior for transforming text to mp3. btw [LAME](./index.php) is used to encode the WAV from Festival to MP3

```ruby
# == Schema Information

# Schema version: 12

#

# Table name: media_transforms

#

#  id                :integer(11)   not null, primary key

#  type              :string(255)   

#  media_bot_id      :integer(11)   

#  text2wave_program :string(255)   default("/usr/bin/text2wave -scale 7 -o \"OUTWAV\" \"INTEXT\" 2>&1")

#  wav2mp3_program   :string(255)   default("/usr/bin/lame -h \"INWAV\" \"OUTMP3\" 2>&1")

#  watermark         :string(255)   

#  watermark_program :string(255)   default("/usr/bin/composite -gravity southeast -watermark 25 \"WMIMAGE\" \"INIMAGE\" \"OUTIMAGE\" 2>&1")

#  created_at        :datetime      

#  updated_at        :datetime      

#

class 
RobotTransform
 
<
 
MediaTransform

  
def 
self.transform_mime_type

    
'
text/plain
'

  
end

  
def 
transform
(
text
)

    
# get a unique temp dir to output text2wav to

    
tmp_dir
 
=
 
Media
.
create_tmp_dir
(
text
.
id
)

    
# set up names and paths for processing

    
name
 
=
 
File
.
basename
(
text
.
filename
)

    
wav_file
 
=
 
File
.
expand_path
(
File
.
join
(
tmp_dir
,
 
name
.
sub
(/
\.
[^.]+$
/,
 
"
.wav
")))

    
mp3_file
 
=
 
File
.
expand_path
(
File
.
join
(
tmp_dir
,
 
name
.
sub
(/
\.
[^.]+$
/,
 
"
.mp3
")))

    
# run the text2wave program

    
program
 
=
 
text2wave_program
.
gsub
('
INTEXT
',
 
text
.
full_filename
)

    
program
.
gsub!
('
OUTWAV
',
 
wav_file
)

    
begin

      
out
 
=
 
IO
.
popen
("
#{program}
")

      
Process
.
wait

      
e
 
=
 
$?
.
exitstatus

    
rescue
 
StandardError
 
=>
 
err

      
raise
 
MediaTransformError
.
new
(
err
)

    
else

      
raise
 
MediaTransformError
.
new
("
0 not returned:
\n
#{program}
\n
#{out.readlines}
"

        
)
 
unless
 
e
.
eql?
(
0
)

    
end

    
# run the wav2mp3 program

    
program
 
=
 
wav2mp3_program
.
gsub
('
INWAV
',
 
wav_file
)

    
program
.
gsub!
('
OUTMP3
',
 
mp3_file
)

    
begin

      
out
 
=
 
IO
.
popen
("
#{program}
")

      
Process
.
wait

      
e
 
=
 
$?
.
exitstatus

    
rescue
 
StandardError
 
=>
 
err

      
raise
 
MediaTransformError
.
new
(
err
)

    
else

      
raise
 
MediaTransformError
.
new
("
0 not returned:
\n
#{program}
\n
#{out.readlines}
"

        
)
 
unless
 
e
.
eql?
(
0
)

    
end

    
fu
 
=
 
FuFile
.
new
('
audio/mpeg
',
 
mp3_file
)

    
mp3
 
=
 
FileSystemMedia
.
new

    
mp3
.
uploaded_data
 
=
 
fu

    
mp3
.
save!

    
FileUtils
.
rm_rf
(
tmp_dir
)

    
mp3

  
end

end
```

```
ruby script/plugin install svn+ssh://rubyforge.org/var/svn/festivaltts4r/plugins/festivaltts_on_rails
```

festival4r.rb adds #to\_speech and #to\_mp3 methods to String and each make a simple call to Kernel#system to execute their programs. That is a quick and easy approach as #system returns false on failure, true on success, and the exit status of the process in $?

However, many processes output text as the they are being executed such as status or error messages. Before I came across festivaltts4r I had actually written my own kind of festivaltts4r for a Rails project. My approach is to capture all of the output of the process and if there is an error returned from the process use the output as the message for an Exception. The process is executed by IO.popen which also captures the text of the process. Process.wait is then called to ensure to wait for the process to finish (beware of hung processes!). Eric Hodel [suggested the use of IO.popen](./pipermail/ruby/2007-February/003197.html) in this manner.

Here is the model I used for my implementation of festivaltts4r. The model uses Single Table Inheritance, look at the schema annotation for clues about the overall strategy/pattern of my MediaTransform model. Also note that MediaTransformError is just a custom Exception my application raises and catches as a part of its behavior for transforming text to mp3. btw [LAME](./index.php) is used to encode the WAV from Festival to MP3

```ruby
# == Schema Information

# Schema version: 12

#

# Table name: media_transforms

#

#  id                :integer(11)   not null, primary key

#  type              :string(255)   

#  media_bot_id      :integer(11)   

#  text2wave_program :string(255)   default("/usr/bin/text2wave -scale 7 -o \"OUTWAV\" \"INTEXT\" 2>&1")

#  wav2mp3_program   :string(255)   default("/usr/bin/lame -h \"INWAV\" \"OUTMP3\" 2>&1")

#  watermark         :string(255)   

#  watermark_program :string(255)   default("/usr/bin/composite -gravity southeast -watermark 25 \"WMIMAGE\" \"INIMAGE\" \"OUTIMAGE\" 2>&1")

#  created_at        :datetime      

#  updated_at        :datetime      

#

class 
RobotTransform
 
<
 
MediaTransform

  
def 
self.transform_mime_type

    
'
text/plain
'

  
end

  
def 
transform
(
text
)

    
# get a unique temp dir to output text2wav to

    
tmp_dir
 
=
 
Media
.
create_tmp_dir
(
text
.
id
)

    
# set up names and paths for processing

    
name
 
=
 
File
.
basename
(
text
.
filename
)

    
wav_file
 
=
 
File
.
expand_path
(
File
.
join
(
tmp_dir
,
 
name
.
sub
(/
\.
[^.]+$
/,
 
"
.wav
")))

    
mp3_file
 
=
 
File
.
expand_path
(
File
.
join
(
tmp_dir
,
 
name
.
sub
(/
\.
[^.]+$
/,
 
"
.mp3
")))

    
# run the text2wave program

    
program
 
=
 
text2wave_program
.
gsub
('
INTEXT
',
 
text
.
full_filename
)

    
program
.
gsub!
('
OUTWAV
',
 
wav_file
)

    
begin

      
out
 
=
 
IO
.
popen
("
#{program}
")

      
Process
.
wait

      
e
 
=
 
$?
.
exitstatus

    
rescue
 
StandardError
 
=>
 
err

      
raise
 
MediaTransformError
.
new
(
err
)

    
else

      
raise
 
MediaTransformError
.
new
("
0 not returned:
\n
#{program}
\n
#{out.readlines}
"

        
)
 
unless
 
e
.
eql?
(
0
)

    
end

    
# run the wav2mp3 program

    
program
 
=
 
wav2mp3_program
.
gsub
('
INWAV
',
 
wav_file
)

    
program
.
gsub!
('
OUTMP3
',
 
mp3_file
)

    
begin

      
out
 
=
 
IO
.
popen
("
#{program}
")

      
Process
.
wait

      
e
 
=
 
$?
.
exitstatus

    
rescue
 
StandardError
 
=>
 
err

      
raise
 
MediaTransformError
.
new
(
err
)

    
else

      
raise
 
MediaTransformError
.
new
("
0 not returned:
\n
#{program}
\n
#{out.readlines}
"

        
)
 
unless
 
e
.
eql?
(
0
)

    
end

    
fu
 
=
 
FuFile
.
new
('
audio/mpeg
',
 
mp3_file
)

    
mp3
 
=
 
FileSystemMedia
.
new

    
mp3
.
uploaded_data
 
=
 
fu

    
mp3
.
save!

    
FileUtils
.
rm_rf
(
tmp_dir
)

    
mp3

  
end

end
```
