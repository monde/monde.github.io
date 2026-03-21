---
title: "RV2 Camping on Gentoo"
date: 2007-07-05
categories: [Linux, Ruby, Gentoo, Camping]
tags: [camping, gentoo, linux, ruby]
---

Evan Weaver wrote a SysV init.d setup for daemonizing Camping apps on a \*Nix system and documents it in [rv, a tool for luxurious camping](./articles/2006/12/19/rv-a-tool-for-luxurious-camping/index.html)

I used that blog entry as a reference to build one called RV2 that is a little bit more Gentoo specific. Here are my scripts and directory layout

On a Gentoo system make a directory **/etc/rv2** and any files in that directory will trigger the rv2 init.d script to attempt to start a corresponding camping app.

for [hurl it](./index.html) the file is **/etc/rv2/hurl\_rv2.conf** and it contains something like:

**sample my-app-rv2.conf**

```
CAMPING_ENV=production
RV2_APP_DIR=/path/to/app/hurl
PORT=1999
ADDRESS=127.0.0.1
```

The rv2 init.d script expects RV2\_APP\_DIR to specify the application directory, PORT to specify the port that the Mongrel harness will listen to, and ADDRESS the machine address that Mongrel will bind to. See the source code for the [Hurl Campling app](./articles/2007/07/04/small-urls-with-camping) to see how Hurl makes use of a ENV variable CAMPING\_ENV to help in configuration for testing and production.

I’m running Hurl as Mongrel behind an Apache Proxy, more details about that can by found in my  [Maintaining Your Own Typo 4.0.3](./articles/2007/04/08/maintaining-your-own-typo-4-0-3) which is nice guide for rolling your own Rails stack.

Here is the rv2\_harness.rb that resides in /path/to/app/hurl. Every Camping app that uses RV2 will need to have a harness named rv2\_harness.rb in its application directory

**sample rv2\_harness.rb @ /path/to/app/hurl/rv2\_harness.rb**

```bash
# Example mongrel harness for camping apps with rv2

# based on Evan Weaver's original rv implementation:

# http://blog.evanweaver.com/articles/2006/12/19/rv-a-tool-for-luxurious-camping

#

# author: Mike Mondragon

# url: http://blog.mondragon.cc/

# license: AFL 3.0

# from the command line:

# ruby rv_harness2.rb PORT ADDRESS

require
 
'
rubygems
'

require
 
'
mongrel
'

require
 
'
mongrel/camping
'

$LOAD_PATH
.
unshift
 
File
.
dirname
(
__FILE__
)

ENV
['
CAMPING_ENV
']
 
||=
 
'
production
'

LOGFILE
 
=
 
"
#{File.dirname(__FILE__)}
/mongrel.log
"

PIDFILE
 
=
 
"
#{File.dirname(__FILE__)}
/mongrel.pid
"

# or whatever else you want passed in

PORT
 
=
 
ARGV
[
0
].
to_i

ADDR
 
=
 
ARGV
[
1
]

# this is your camping app

require
 
'
hurl
'

app
 
=
 
Hurl

if
 
ENV
['
CAMPING_ENV
'].
eql?
('
production
')

  
app
::
Models
::
Base
.
establish_connection
 
:adapter
 
=>
 
'
mysql
',

    
:database
 
=>
 
'
hurl
',

    
:host
 
=>
 
'
localhost
',

    
:username
 
=>
 
'
root
',

    
:password
 
=>
 
'
'

else

  
app
::
Models
::
Base
.
establish_connection
 
:adapter
 
=>
 
'
sqlite3
',

   
:database
 
=>
 
'
db/hurl.db
'

end

app
::
Models
::
Base
.
logger
 
=
 
Logger
.
new
(
LOGFILE
)
 
# comment me out if you don't want to log

app
::
Models
::
Base
.
threaded_connections
=
false

app
.
create

config
 
=
 
Mongrel
::
Configurator
.
new
 
:host
 
=>
 
ADDR
,
 
:pid_file
 
=>
 
PIDFILE
 
do

  
listener
 
:port
 
=>
 
PORT
 
do

    
uri
 
'
/
',
 
:handler
 
=>
 
Mongrel
::
Camping
::
CampingHandler
.
new
(
app
)

    
# use the mongrel static server in production instead of the camping controller

    
uri
 
'
/static/
',
 
:handler
 
=>
 
Mongrel
::
DirHandler
.
new
("
static/
")

    
uri
 
'
/favicon.ico
',
 
:handler
 
=>
 
Mongrel
::
Error404Handler
.
new
('
')

    
setup_signals

    
run

    
write_pid_file

    
log
 
"
#{app}
 available at 
#{ADDR}
:
#{PORT}
"

    
join

  
end

end
```

Below is the /etc/init.d/rv2 script. After you install it be sure to enable it for system startup and shut down:

```
rc-update add rv2 default
```

Also since the script is running the Mongrel as the “apache” user and group be sure to chown your applications directory with those credentials since Mongrel will bite if it doesn’t have permissions to write its pid file

```bash
chown -R apache.apache /path/to/your/camping/app
```

**/etc/init.d/rv2**

```bash
#!/sbin/runscript
depend() {
        need net
        use mysql apache2
        after apache2
}

USER=apache
GROUP=apache
RV2_HARNESS=rv2_harness.rb
RV2_CONF_DIR=/etc/rv2

start() {
        ebegin "Starting Camping Apps in RV2" 
        for apps in `ls -1 ${RV2_CONF_DIR}`
        do
                # the config needs to have CAMPING_ENV,
                # RV2_APP_DIR, PORT, and ADDRESS specified
                . ${RV2_CONF_DIR}/$apps

                start-stop-daemon --start --quiet --background \
                        --chuid ${USER:-apache}:${GROUP:-apache} \
                        --exec /usr/bin/env ruby \
                        -- $RV2_APP_DIR/${RV2_HARNESS} $PORT $ADDRESS 1>&2

                res=$?
                # if one is broken do not continue
                if [ $res -ne 0 ]; then break; fi
        done
        eend ${res}
}

stop() {
        ebegin "Stopping Camping Apps in RV2" 
        for apps in `ls -1 ${RV2_CONF_DIR}`
        do
                . ${RV2_CONF_DIR}/$apps
                start-stop-daemon --stop --pidfile $RV2_APP_DIR/mongrel.pid
                ret=$?
                rm -f $RV2_APP_DIR/mongrel.pid
                # force unloading of all apps
        done
        eend ${ret}
}

restart() {
        svc_stop
        svc_start
}
```

Enjoy!

On a Gentoo system make a directory **/etc/rv2** and any files in that directory will trigger the rv2 init.d script to attempt to start a corresponding camping app.

for [hurl it](./index.html) the file is **/etc/rv2/hurl\_rv2.conf** and it contains something like:

**sample my-app-rv2.conf**

```
CAMPING_ENV=production
RV2_APP_DIR=/path/to/app/hurl
PORT=1999
ADDRESS=127.0.0.1
```

The rv2 init.d script expects RV2\_APP\_DIR to specify the application directory, PORT to specify the port that the Mongrel harness will listen to, and ADDRESS the machine address that Mongrel will bind to. See the source code for the [Hurl Campling app](./articles/2007/07/04/small-urls-with-camping) to see how Hurl makes use of a ENV variable CAMPING\_ENV to help in configuration for testing and production.

I’m running Hurl as Mongrel behind an Apache Proxy, more details about that can by found in my  [Maintaining Your Own Typo 4.0.3](./articles/2007/04/08/maintaining-your-own-typo-4-0-3) which is nice guide for rolling your own Rails stack.

Here is the rv2\_harness.rb that resides in /path/to/app/hurl. Every Camping app that uses RV2 will need to have a harness named rv2\_harness.rb in its application directory

**sample rv2\_harness.rb @ /path/to/app/hurl/rv2\_harness.rb**

```bash
# Example mongrel harness for camping apps with rv2

# based on Evan Weaver's original rv implementation:

# http://blog.evanweaver.com/articles/2006/12/19/rv-a-tool-for-luxurious-camping

#

# author: Mike Mondragon

# url: http://blog.mondragon.cc/

# license: AFL 3.0

# from the command line:

# ruby rv_harness2.rb PORT ADDRESS

require
 
'
rubygems
'

require
 
'
mongrel
'

require
 
'
mongrel/camping
'

$LOAD_PATH
.
unshift
 
File
.
dirname
(
__FILE__
)

ENV
['
CAMPING_ENV
']
 
||=
 
'
production
'

LOGFILE
 
=
 
"
#{File.dirname(__FILE__)}
/mongrel.log
"

PIDFILE
 
=
 
"
#{File.dirname(__FILE__)}
/mongrel.pid
"

# or whatever else you want passed in

PORT
 
=
 
ARGV
[
0
].
to_i

ADDR
 
=
 
ARGV
[
1
]

# this is your camping app

require
 
'
hurl
'

app
 
=
 
Hurl

if
 
ENV
['
CAMPING_ENV
'].
eql?
('
production
')

  
app
::
Models
::
Base
.
establish_connection
 
:adapter
 
=>
 
'
mysql
',

    
:database
 
=>
 
'
hurl
',

    
:host
 
=>
 
'
localhost
',

    
:username
 
=>
 
'
root
',

    
:password
 
=>
 
'
'

else

  
app
::
Models
::
Base
.
establish_connection
 
:adapter
 
=>
 
'
sqlite3
',

   
:database
 
=>
 
'
db/hurl.db
'

end

app
::
Models
::
Base
.
logger
 
=
 
Logger
.
new
(
LOGFILE
)
 
# comment me out if you don't want to log

app
::
Models
::
Base
.
threaded_connections
=
false

app
.
create

config
 
=
 
Mongrel
::
Configurator
.
new
 
:host
 
=>
 
ADDR
,
 
:pid_file
 
=>
 
PIDFILE
 
do

  
listener
 
:port
 
=>
 
PORT
 
do

    
uri
 
'
/
',
 
:handler
 
=>
 
Mongrel
::
Camping
::
CampingHandler
.
new
(
app
)

    
# use the mongrel static server in production instead of the camping controller

    
uri
 
'
/static/
',
 
:handler
 
=>
 
Mongrel
::
DirHandler
.
new
("
static/
")

    
uri
 
'
/favicon.ico
',
 
:handler
 
=>
 
Mongrel
::
Error404Handler
.
new
('
')

    
setup_signals

    
run

    
write_pid_file

    
log
 
"
#{app}
 available at 
#{ADDR}
:
#{PORT}
"

    
join

  
end

end
```

Below is the /etc/init.d/rv2 script. After you install it be sure to enable it for system startup and shut down:

```
rc-update add rv2 default
```

Also since the script is running the Mongrel as the “apache” user and group be sure to chown your applications directory with those credentials since Mongrel will bite if it doesn’t have permissions to write its pid file

```bash
chown -R apache.apache /path/to/your/camping/app
```

**/etc/init.d/rv2**

```bash
#!/sbin/runscript
depend() {
        need net
        use mysql apache2
        after apache2
}

USER=apache
GROUP=apache
RV2_HARNESS=rv2_harness.rb
RV2_CONF_DIR=/etc/rv2

start() {
        ebegin "Starting Camping Apps in RV2" 
        for apps in `ls -1 ${RV2_CONF_DIR}`
        do
                # the config needs to have CAMPING_ENV,
                # RV2_APP_DIR, PORT, and ADDRESS specified
                . ${RV2_CONF_DIR}/$apps

                start-stop-daemon --start --quiet --background \
                        --chuid ${USER:-apache}:${GROUP:-apache} \
                        --exec /usr/bin/env ruby \
                        -- $RV2_APP_DIR/${RV2_HARNESS} $PORT $ADDRESS 1>&2

                res=$?
                # if one is broken do not continue
                if [ $res -ne 0 ]; then break; fi
        done
        eend ${res}
}

stop() {
        ebegin "Stopping Camping Apps in RV2" 
        for apps in `ls -1 ${RV2_CONF_DIR}`
        do
                . ${RV2_CONF_DIR}/$apps
                start-stop-daemon --stop --pidfile $RV2_APP_DIR/mongrel.pid
                ret=$?
                rm -f $RV2_APP_DIR/mongrel.pid
                # force unloading of all apps
        done
        eend ${ret}
}

restart() {
        svc_stop
        svc_start
}
```

Enjoy!
