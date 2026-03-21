---
title: "Maintaining Your Own Typo 4.0.3"
date: 2007-04-08
categories: [Typo, Rails, Subversion, Gentoo, Apache]
tags: [apache, rails, subversion, typo]
---

This is the combined experience from my previous entry [Typo 4.0 + Apache2 + MySQL + Gentoo](./articles/2006/10/24/typo-4-0-apache2-mysql-gentoo) and [Chapter 27 Deployment and Production / Agile Web Development with Rails](./titles/rails/index.html "2nd Ed.") and [Capistrano: Automating Application Deployment](./read/book/17/index.html)

What I am illustrating here is how to maintain a Typo blog. What I mean by maintain is that you are creating your own
source repository for your instance of Typo. This will allow you to patch the application with fixes and your own
modifications. You will also integrate Capistrano into your repository so that you deploy your updates with ease.
Also, I show you my implementation of a Mongrel init.d script on Gentoo that will ensure Mongrel starts back up on
server reboot.

## Machine layouts

Try to remember this as I step through these instructions. The initial source setup for Typo is on your
local host. You create a Subversion repository where ever you keep yours. My Subversion repository is on
a remote machine that I can access with `svn+ssh://` URL. Assumed is that you are the administrator of
the deployment machine. You are going to check the Typo instance you set up locally into your source repository.
Your setup will also contain a Capistrano configuration. Your deployment server must have access to your
Subversion repository. Once you do an initial Capistrano deployment you will finalize your Typo source checked
into Subversion. Once you have this initial check in and deployment completed I’ll show you how to patch the
broken Google sitemap.xml in Typo 4.0.3, and redeploy your version of Typo. Your finished Typo blog will
be deployed to `http://www.mysite.com/`

## Software Versions

Software installed at the time of this writing:

```bash
$ uname -a
Linux toki 2.6.19-gentoo-r5 #2 SMP Fri Feb 23 14:57:32 PST 2007 i686 Celeron (Mendocino) GenuineIntel GNU/Linux
```

- dev-lang/ruby-1.8.5\_p2
- dev-ruby/rubygems-0.8.11-r6 \* dev-db/sqlite-3.3.5-r1
- dev-db/mysql-5.0.26-r2
- net-www/apache-2.2.4

## Tools Preparation

The basic gems needed for Typo are:

```ruby
gem install --remote rails --version 1.2.2 --include-dependencies --rdoc
gem install --remote rails --version 1.1.6 --include-dependencies --rdoc
gem install --remote typo --version 4.0.3 --include-dependencies --rdoc
gem install --remote termios --include-dependencies termios --rdoc
gem install --remote capistrano --include-dependencies --rdoc
gem install --remote mongrel --include-dependencies --rdoc
gem install --remote mongrel_cluster --include-dependencies --rdoc
```

## Typo Instance Install And Preparation

We are going to prepare our Typo instance in a local directory. Later on we’ll source this in a
Subversion repository. local\_user is the user directory where you are going to set up the
Capistrano deployment configuration as well. Installing withe Typo script:

```
typo install /home/local_user/projects/typo
```

The Typo installer script invokes an instance of Mongrel. Stop the mongrel that the Typo
installer invokes:

```
typo stop /home/local_user/projects/typo
```

## (Example Only) Typo configure command

We don’t need to do this but for reference sake here’s how to invoke Typo’s configure command with lots of
options. We’ll be using the equivalent settings in our Capistrano configuration. Typo’s web server settings:

`rails-environment=production web-server=mongrel_cluster port-number=8900 threads=2 bind-address=127.0.0.1 database=mysql`

```
typo config /var/www/mysite_com/typo rails-environment=production web-server=mongrel port-number=8900 threads=2 bind-address=127.0.0.1 database=mysql
```

## Mysql Preparation

For convenience sake here’s how to create all three mysql environments at once on a single mysql instance. Prepare the development, test, and production mysql Typo database users and databases like so:

```bash
$ mysql -u root -p -h localhost
mysql> create database mysite_com_typodb_development character set utf8;
mysql> create database mysite_com_typodb_test character set utf8;
mysql> create database mysite_com_typodb_production character set utf8;
mysql> grant all on mysite_com_typodb_development.* to typo_dev@localhost identified by 'changeme';
mysql> grant all on mysite_com_typodb_test.* to typo_test@localhost identified by 'changeme';
mysql> grant all on mysite_com_typodb_production.* to typo_prod@localhost identified by 'changeme';
mysql> flush privileges;
mysql> quit;
```

Configure your database settings in `config/database.yml`. Typo’s default is sqlite3 based. We’ll
be using Capistrano’s `after_update_code` task to copy in real our production database settings
rather have them reside in the copy of config/database.yml that is checked into our source repository.

## Subversion Check in

Now do a quick and dirty setup to manage your Typo source in Subversion. The example below is from my
[Subversion + Rails In Five Minutes](./articles/2006/11/05/subversion-rails-in-five-minutes) post.
`/path/to/repository/typo` is where ever your Subversion repository is at. Remember that your Subversion
repository must be accessible to your production Mongrel server.

This is on machine where your Subversion repository lives:

```bash
svnadmin create /path/to/repository/typo
svn mkdir --message="Creating my project's repository ..." file:///path/to/project/trunk file:///path/to/project/tags file:///path/to/project/branches
```

The example below is using a local `file://` Subversion URL, but this could also be `svn+ssh://`
Subversion URL is your Subversion repository is remote. This is on the localhost where we are
setting up our Typo configuration:

```bash
cd /home/local_user/projects/typo
svn import . file:///path/to/source/code/trunk -m "Importing the existing code for my rails project" 
```

Once initially checked in we need to check out source

```bash
cd ..
mv typo typo.old
svn checkout file:///path/to/source/code/trunk typo
```

Prepare Subversion to be rails aware in your project.

```bash
$ svn remove log/*
$ svn commit -m 'removing all log files from subversion'
$ svn propset svn:ignore "*.log" log/
$ svn update log/
$ svn commit -m 'Ignoring all files in /log/ ending in .log'
$ svn remove tmp/*
$ svn commit -m 'removing all tmp artifacts from subversion'
$ svn propset svn:ignore "*" tmp/
$ svn update tmp/
$ svn commit -m "ignore tmp/ content from now on" 
```

## Mongel cluster & Capistrano configuration

I derived this experience from Chapter 27 Setting Up A Deployment Environment appendix of the Agile book.
A thorough discussion of the Apache details is at:
[Apache Best Practice Deployment](./docs/apache.html)

Now we’ll setup our Typo configuration to be in a Mongrel Cluster:

```bash
mongrel_rails cluster::configure -e production -p 8900 -a 127.0.0.1 -N 3 -c /var/www/mysite/typo/current
```

The Mongrel configuration is dropped to
`config/mongrel_cluster.yml`

## Setup Capistrano

```
cap --apply-to /home/local_user/projects/typo typo
```

Add this require statement to the top of your `config/deploy.rb`

```
require
 
'
mongrel_cluster/recipes
'
```

Example Capistrano settings. Your repository is at `http://svn.host.com/` and you’ve named your
application `typo` . The Typo deployment directory on your production server is:
`/var/www/mysite/typo`

```
set
 
:application
,
 
"
typo
"

set
 
:repository
,
 
"
http://svn.host.com/
#{application}
/trunk
"

set
 
:deploy_to
,
 
"
/var/www/mysite/
#{application}
"

role
 
:web
,
 
"
your.host.com
"

role
 
:app
,
 
"
your.host.com
"

role
 
:db
,
 
"
your.host.com
"
 
,
 
:primary
 
=>
 
true

set
 
:user
,
 
"
mydeployeruser
"
            
# defaults to the currently logged in user

set
 
:mongrel_conf
,
 
"
#{current_path}
/config/mongrel_cluster.yml
"
```

Also notice that I’m declaring a remote user `mydeployeruser` that Capistrano will become while doing
its tasks on the remote server. I add that user to the apache group on the server. I use the apache
group as the default web administration group on that server. `mydeployeruser` needs to be allowed
to invoke the mongrel\_rails executable in the `/etc/sudoers` file on the deployment server. This is
how mongrel\_rails might look in my `/etc/sudoers`

```
mydeployeruser        ALL=/usr/bin/mongrel_rails
```

On your production server, make a config directory in your Capistrano shared directory for your production database.yml:

```bash
mkdir -p /var/www/mysite/typo/shared/config
chown -R mydeployeruser.mydeployeruser /var/www/mysite/typo/shared/config
```

then copy your production database.yml.production into the `shared/config` directory. Below
we’ll create a after\_update\_code Capistrano task to copy that production database.yml into production.
Secure your production database.yml:

```bash
chown -R mydeployeruser.mydeployeruser /var/www/mysite/typo/shared/config/database.yml.production
chmod 771 /var/www/mysite/typo/shared/config/
chmod 660 /var/www/mysite/typo/shared/config/database.yml.production
```

This idea of having after\_update\_code Capistrano task to copy over the production database.yml from
the Agile book. In `config/deploy.rb` :

```bash
task :after_update_code, :roles => :app do
  db_config = "#{shared_path}/config/database.yml.production" 
  run "cp #{db_config} #{release_path}/config/database.yml" 
end
```

to copy in your production database settings securely.
Now finish the Capistrano setup locally:

```
cap setup
cap cold_deploy
```

Now check in the completed Capistrano configuration to into your source repository:

```
svn status
svn commit
```

## Additional Mysql And Typo Preparation

On your production server change directory to where you installed typo and install the MySQL schema for typo
for your three instances

```bash
$ mysql -u typo_dev -p mysite_com_typodb_development < db/schema.mysql.sql
$ mysql -u typo_test -p mysite_com_typodb_test < db/schema.mysql.sql
$ mysql -u typo_prod -p mysite_com_typodb_production < db/schema.mysql.sql
```

## Apache2 Configuration

These instructions are Gentoo specific, modify to suit your Apache deployment.

We will use mod\_proxy to route requests from port 80 of a virtual host to port 8900 on local host.
To enable mod\_proxy in Apache2 on Gentoo you need to have a PROXY defined in your /etc/conf.d/apache2, such as:

```
APACHE2_OPTS="-D DEFAULT_VHOST -D PROXY" 
```

And in the /etc/apache2/httpd.conf you need to configure your PROXY with an IfDefine statement such as (its usually already set up by default):

```html
<IfDefine PROXY>
    LoadModule proxy_module                  modules/mod_proxy.so
    LoadModule proxy_connect_module          modules/mod_proxy_connect.so
    LoadModule proxy_http_module             modules/mod_proxy_http.so
</IfDefine>
```

## Apache2 VirtualHost Configuration

The minimum virtual host file you need to have Apache2 route requests to Mongrel are as follows. You will need to change the specific path and server name details to your installation in /etc/apache2/vhosts.d/01\_mysite\_com\_vhost.conf (or what ever you name your vhost file)

The following virtual host implies NameVirtualHost \*:80 in 00\_default\_vhost.conf or httpd.conf

```bash
<VirtualHost *:80>
  ServerName www.mysite.com
  DocumentRoot /var/www/mysite/typo/current/public

  ErrorLog /var/www/mysite/logs/error_log
  CustomLog /var/www/mysite/logs/access_log combined

  <Directory "/var/www/mysite/typo/current/public" >
    Options FollowSymLinks
    AllowOverride None
    Order allow,deny
    Allow from all
  </Directory>

  ProxyRequests Off
  <Proxy *>
    Order Deny,Allow
    Deny from all
    Allow from all
  </Proxy>

  <Proxy balancer://mongrel_cluster>
    BalancerMember http://127.0.0.1:8900
    BalancerMember http://127.0.0.1:8901
  </Proxy>

  RewriteEngine On
  # Check for  maintenance file and redirect all requests
  RewriteCond  %{DOCUMENT_ROOT}/system/maintenance.html -f
  RewriteCond  %{SCRIPT_FILENAME} !maintenance.html
  RewriteRule  ^.*$ /system/maintenance.html [L]
  # Rewrite index to check for static
  RewriteRule ^/$ /index.html [QSA]
  # Rewrite to check for Rails cached page
  RewriteRule ^([^.]+)$ $1.html [QSA]
  # Redirect all non-static requests to cluster
  RewriteCond %{DOCUMENT_ROOT}/%{REQUEST_FILENAME} !-f
  RewriteRule ^/(.*)$ balancer://mongrel_cluster%{REQUEST_URI} [P,QSA,L]
</VirtualHost>
```

Use apache2ctl to make sure you have a good virtual host configuration.

```
apache2ctl configtest
```

Reload Apache2 after getting a configuration to pass.

```
/etc/init.d/apache2 reload
```

Now open a web browser to http://www.mysite.com/ (change to the real name of your site) you should be redirected
to http://www.mysite.com/ your bare Typo installation. If things are not working tail the Apache2 log and
the Mongrel logs to see if you can find answers to your errors there:

```
tail -f /var/www/mysite/logs/error_log
tail -f /var/www/mysite/typo/log/production.log
```

Once its all lined up your blog should be running on `http://www.mysite.com/`

## Gentoo init.d for Mogrel clusters

Here’s an example init.d script for you Mongrel clusters

```bash
#!/sbin/runscript
depend() {
  need net
  use mysql apache2
   after apache2
}

start() {
  ebegin "Starting mongrels" 
  /usr/bin/mongrel_rails cluster::start -C /var/www/mysite/typo/current/config/mongrel_cluster.yml
  res=$?
  # force mongrel to initialize the indexex
  wget -o /dev/null http://localhost:8900/
  wget -o /dev/null http://localhost:8901/
  eend $res
}

stop() {
  ebegin "Stopping mongrels" 
  /usr/bin/mongrel_rails cluster::stop -C /var/www/mysite/typo/current/config/mongrel_cluster.yml
  eend $?
}

reload() {
  ebegin "Restarting mongrels" 
  /usr/bin/mongrel_rails cluster::restart -C /var/www/mysite/typo/current/config/mongrel_cluster.yml
  res=$?
  # force mongrel to initialize the indexex
  wget -o /dev/null http://localhost:8900/
  wget -o /dev/null http://localhost:8901/
  eend $res
}
```

Add your mongrel script to the default run levels of the server.

```
rc-update add mongrel default
```

## Helpful Capistrano commands

Show tasks

```
cap show_tasks
```

Re-deploy Typo

```
cap disable_web
cap update
cap enable_web
```

Stop/stop your cluster

```
cap stop_mongrel_cluster
cap start_mongrel_cluster
```

## Additional Typo patches

You patch your Typo in the project directory that you’ve checkout from your Subversion repository.
Once patched you check the changes in. Then you do a Capistrano redeployment of your application
to propagate your changes, e.g.:

```
cap disable_web
cap update
cap enable_web
```

The current sitemap.xml in Typo 4.0.3 is broken for Google. You need to fix it for Google love:

[Typo Google Sitemap fix](./articles/2007/01/16/typo-google-sitemap-fix/index.html)

Here’s how to add those neato Web 2.0 WP Notable icon links in Typo

[Notable social bookmarking/networking for Typo](./blog/2006/09/02/notable-social-bookmarking-networking-for-typo/index.html)

My version also shows how to add them to Typo “pages”

## Machine layouts

Try to remember this as I step through these instructions. The initial source setup for Typo is on your
local host. You create a Subversion repository where ever you keep yours. My Subversion repository is on
a remote machine that I can access with `svn+ssh://` URL. Assumed is that you are the administrator of
the deployment machine. You are going to check the Typo instance you set up locally into your source repository.
Your setup will also contain a Capistrano configuration. Your deployment server must have access to your
Subversion repository. Once you do an initial Capistrano deployment you will finalize your Typo source checked
into Subversion. Once you have this initial check in and deployment completed I’ll show you how to patch the
broken Google sitemap.xml in Typo 4.0.3, and redeploy your version of Typo. Your finished Typo blog will
be deployed to `http://www.mysite.com/`

## Software Versions

Software installed at the time of this writing:

```bash
$ uname -a
Linux toki 2.6.19-gentoo-r5 #2 SMP Fri Feb 23 14:57:32 PST 2007 i686 Celeron (Mendocino) GenuineIntel GNU/Linux
```

- dev-lang/ruby-1.8.5\_p2
- dev-ruby/rubygems-0.8.11-r6 \* dev-db/sqlite-3.3.5-r1
- dev-db/mysql-5.0.26-r2
- net-www/apache-2.2.4

## Tools Preparation

The basic gems needed for Typo are:

```ruby
gem install --remote rails --version 1.2.2 --include-dependencies --rdoc
gem install --remote rails --version 1.1.6 --include-dependencies --rdoc
gem install --remote typo --version 4.0.3 --include-dependencies --rdoc
gem install --remote termios --include-dependencies termios --rdoc
gem install --remote capistrano --include-dependencies --rdoc
gem install --remote mongrel --include-dependencies --rdoc
gem install --remote mongrel_cluster --include-dependencies --rdoc
```

## Typo Instance Install And Preparation

We are going to prepare our Typo instance in a local directory. Later on we’ll source this in a
Subversion repository. local\_user is the user directory where you are going to set up the
Capistrano deployment configuration as well. Installing withe Typo script:

```
typo install /home/local_user/projects/typo
```

The Typo installer script invokes an instance of Mongrel. Stop the mongrel that the Typo
installer invokes:

```
typo stop /home/local_user/projects/typo
```

## (Example Only) Typo configure command

We don’t need to do this but for reference sake here’s how to invoke Typo’s configure command with lots of
options. We’ll be using the equivalent settings in our Capistrano configuration. Typo’s web server settings:

`rails-environment=production web-server=mongrel_cluster port-number=8900 threads=2 bind-address=127.0.0.1 database=mysql`

```
typo config /var/www/mysite_com/typo rails-environment=production web-server=mongrel port-number=8900 threads=2 bind-address=127.0.0.1 database=mysql
```

## Mysql Preparation

For convenience sake here’s how to create all three mysql environments at once on a single mysql instance. Prepare the development, test, and production mysql Typo database users and databases like so:

```bash
$ mysql -u root -p -h localhost
mysql> create database mysite_com_typodb_development character set utf8;
mysql> create database mysite_com_typodb_test character set utf8;
mysql> create database mysite_com_typodb_production character set utf8;
mysql> grant all on mysite_com_typodb_development.* to typo_dev@localhost identified by 'changeme';
mysql> grant all on mysite_com_typodb_test.* to typo_test@localhost identified by 'changeme';
mysql> grant all on mysite_com_typodb_production.* to typo_prod@localhost identified by 'changeme';
mysql> flush privileges;
mysql> quit;
```

Configure your database settings in `config/database.yml`. Typo’s default is sqlite3 based. We’ll
be using Capistrano’s `after_update_code` task to copy in real our production database settings
rather have them reside in the copy of config/database.yml that is checked into our source repository.

## Subversion Check in

Now do a quick and dirty setup to manage your Typo source in Subversion. The example below is from my
[Subversion + Rails In Five Minutes](./articles/2006/11/05/subversion-rails-in-five-minutes) post.
`/path/to/repository/typo` is where ever your Subversion repository is at. Remember that your Subversion
repository must be accessible to your production Mongrel server.

This is on machine where your Subversion repository lives:

```bash
svnadmin create /path/to/repository/typo
svn mkdir --message="Creating my project's repository ..." file:///path/to/project/trunk file:///path/to/project/tags file:///path/to/project/branches
```

The example below is using a local `file://` Subversion URL, but this could also be `svn+ssh://`
Subversion URL is your Subversion repository is remote. This is on the localhost where we are
setting up our Typo configuration:

```bash
cd /home/local_user/projects/typo
svn import . file:///path/to/source/code/trunk -m "Importing the existing code for my rails project" 
```

Once initially checked in we need to check out source

```bash
cd ..
mv typo typo.old
svn checkout file:///path/to/source/code/trunk typo
```

Prepare Subversion to be rails aware in your project.

```bash
$ svn remove log/*
$ svn commit -m 'removing all log files from subversion'
$ svn propset svn:ignore "*.log" log/
$ svn update log/
$ svn commit -m 'Ignoring all files in /log/ ending in .log'
$ svn remove tmp/*
$ svn commit -m 'removing all tmp artifacts from subversion'
$ svn propset svn:ignore "*" tmp/
$ svn update tmp/
$ svn commit -m "ignore tmp/ content from now on" 
```

## Mongel cluster & Capistrano configuration

I derived this experience from Chapter 27 Setting Up A Deployment Environment appendix of the Agile book.
A thorough discussion of the Apache details is at:
[Apache Best Practice Deployment](./docs/apache.html)

Now we’ll setup our Typo configuration to be in a Mongrel Cluster:

```bash
mongrel_rails cluster::configure -e production -p 8900 -a 127.0.0.1 -N 3 -c /var/www/mysite/typo/current
```

The Mongrel configuration is dropped to
`config/mongrel_cluster.yml`

## Setup Capistrano

```
cap --apply-to /home/local_user/projects/typo typo
```

Add this require statement to the top of your `config/deploy.rb`

```
require
 
'
mongrel_cluster/recipes
'
```

Example Capistrano settings. Your repository is at `http://svn.host.com/` and you’ve named your
application `typo` . The Typo deployment directory on your production server is:
`/var/www/mysite/typo`

```
set
 
:application
,
 
"
typo
"

set
 
:repository
,
 
"
http://svn.host.com/
#{application}
/trunk
"

set
 
:deploy_to
,
 
"
/var/www/mysite/
#{application}
"

role
 
:web
,
 
"
your.host.com
"

role
 
:app
,
 
"
your.host.com
"

role
 
:db
,
 
"
your.host.com
"
 
,
 
:primary
 
=>
 
true

set
 
:user
,
 
"
mydeployeruser
"
            
# defaults to the currently logged in user

set
 
:mongrel_conf
,
 
"
#{current_path}
/config/mongrel_cluster.yml
"
```

Also notice that I’m declaring a remote user `mydeployeruser` that Capistrano will become while doing
its tasks on the remote server. I add that user to the apache group on the server. I use the apache
group as the default web administration group on that server. `mydeployeruser` needs to be allowed
to invoke the mongrel\_rails executable in the `/etc/sudoers` file on the deployment server. This is
how mongrel\_rails might look in my `/etc/sudoers`

```
mydeployeruser        ALL=/usr/bin/mongrel_rails
```

On your production server, make a config directory in your Capistrano shared directory for your production database.yml:

```bash
mkdir -p /var/www/mysite/typo/shared/config
chown -R mydeployeruser.mydeployeruser /var/www/mysite/typo/shared/config
```

then copy your production database.yml.production into the `shared/config` directory. Below
we’ll create a after\_update\_code Capistrano task to copy that production database.yml into production.
Secure your production database.yml:

```bash
chown -R mydeployeruser.mydeployeruser /var/www/mysite/typo/shared/config/database.yml.production
chmod 771 /var/www/mysite/typo/shared/config/
chmod 660 /var/www/mysite/typo/shared/config/database.yml.production
```

This idea of having after\_update\_code Capistrano task to copy over the production database.yml from
the Agile book. In `config/deploy.rb` :

```bash
task :after_update_code, :roles => :app do
  db_config = "#{shared_path}/config/database.yml.production" 
  run "cp #{db_config} #{release_path}/config/database.yml" 
end
```

to copy in your production database settings securely.
Now finish the Capistrano setup locally:

```
cap setup
cap cold_deploy
```

Now check in the completed Capistrano configuration to into your source repository:

```
svn status
svn commit
```

## Additional Mysql And Typo Preparation

On your production server change directory to where you installed typo and install the MySQL schema for typo
for your three instances

```bash
$ mysql -u typo_dev -p mysite_com_typodb_development < db/schema.mysql.sql
$ mysql -u typo_test -p mysite_com_typodb_test < db/schema.mysql.sql
$ mysql -u typo_prod -p mysite_com_typodb_production < db/schema.mysql.sql
```

## Apache2 Configuration

These instructions are Gentoo specific, modify to suit your Apache deployment.

We will use mod\_proxy to route requests from port 80 of a virtual host to port 8900 on local host.
To enable mod\_proxy in Apache2 on Gentoo you need to have a PROXY defined in your /etc/conf.d/apache2, such as:

```
APACHE2_OPTS="-D DEFAULT_VHOST -D PROXY" 
```

And in the /etc/apache2/httpd.conf you need to configure your PROXY with an IfDefine statement such as (its usually already set up by default):

```html
<IfDefine PROXY>
    LoadModule proxy_module                  modules/mod_proxy.so
    LoadModule proxy_connect_module          modules/mod_proxy_connect.so
    LoadModule proxy_http_module             modules/mod_proxy_http.so
</IfDefine>
```

## Apache2 VirtualHost Configuration

The minimum virtual host file you need to have Apache2 route requests to Mongrel are as follows. You will need to change the specific path and server name details to your installation in /etc/apache2/vhosts.d/01\_mysite\_com\_vhost.conf (or what ever you name your vhost file)

The following virtual host implies NameVirtualHost \*:80 in 00\_default\_vhost.conf or httpd.conf

```bash
<VirtualHost *:80>
  ServerName www.mysite.com
  DocumentRoot /var/www/mysite/typo/current/public

  ErrorLog /var/www/mysite/logs/error_log
  CustomLog /var/www/mysite/logs/access_log combined

  <Directory "/var/www/mysite/typo/current/public" >
    Options FollowSymLinks
    AllowOverride None
    Order allow,deny
    Allow from all
  </Directory>

  ProxyRequests Off
  <Proxy *>
    Order Deny,Allow
    Deny from all
    Allow from all
  </Proxy>

  <Proxy balancer://mongrel_cluster>
    BalancerMember http://127.0.0.1:8900
    BalancerMember http://127.0.0.1:8901
  </Proxy>

  RewriteEngine On
  # Check for  maintenance file and redirect all requests
  RewriteCond  %{DOCUMENT_ROOT}/system/maintenance.html -f
  RewriteCond  %{SCRIPT_FILENAME} !maintenance.html
  RewriteRule  ^.*$ /system/maintenance.html [L]
  # Rewrite index to check for static
  RewriteRule ^/$ /index.html [QSA]
  # Rewrite to check for Rails cached page
  RewriteRule ^([^.]+)$ $1.html [QSA]
  # Redirect all non-static requests to cluster
  RewriteCond %{DOCUMENT_ROOT}/%{REQUEST_FILENAME} !-f
  RewriteRule ^/(.*)$ balancer://mongrel_cluster%{REQUEST_URI} [P,QSA,L]
</VirtualHost>
```

Use apache2ctl to make sure you have a good virtual host configuration.

```
apache2ctl configtest
```

Reload Apache2 after getting a configuration to pass.

```
/etc/init.d/apache2 reload
```

Now open a web browser to http://www.mysite.com/ (change to the real name of your site) you should be redirected
to http://www.mysite.com/ your bare Typo installation. If things are not working tail the Apache2 log and
the Mongrel logs to see if you can find answers to your errors there:

```
tail -f /var/www/mysite/logs/error_log
tail -f /var/www/mysite/typo/log/production.log
```

Once its all lined up your blog should be running on `http://www.mysite.com/`

## Gentoo init.d for Mogrel clusters

Here’s an example init.d script for you Mongrel clusters

```bash
#!/sbin/runscript
depend() {
  need net
  use mysql apache2
   after apache2
}

start() {
  ebegin "Starting mongrels" 
  /usr/bin/mongrel_rails cluster::start -C /var/www/mysite/typo/current/config/mongrel_cluster.yml
  res=$?
  # force mongrel to initialize the indexex
  wget -o /dev/null http://localhost:8900/
  wget -o /dev/null http://localhost:8901/
  eend $res
}

stop() {
  ebegin "Stopping mongrels" 
  /usr/bin/mongrel_rails cluster::stop -C /var/www/mysite/typo/current/config/mongrel_cluster.yml
  eend $?
}

reload() {
  ebegin "Restarting mongrels" 
  /usr/bin/mongrel_rails cluster::restart -C /var/www/mysite/typo/current/config/mongrel_cluster.yml
  res=$?
  # force mongrel to initialize the indexex
  wget -o /dev/null http://localhost:8900/
  wget -o /dev/null http://localhost:8901/
  eend $res
}
```

Add your mongrel script to the default run levels of the server.

```
rc-update add mongrel default
```

## Helpful Capistrano commands

Show tasks

```
cap show_tasks
```

Re-deploy Typo

```
cap disable_web
cap update
cap enable_web
```

Stop/stop your cluster

```
cap stop_mongrel_cluster
cap start_mongrel_cluster
```

## Additional Typo patches

You patch your Typo in the project directory that you’ve checkout from your Subversion repository.
Once patched you check the changes in. Then you do a Capistrano redeployment of your application
to propagate your changes, e.g.:

```
cap disable_web
cap update
cap enable_web
```

The current sitemap.xml in Typo 4.0.3 is broken for Google. You need to fix it for Google love:

[Typo Google Sitemap fix](./articles/2007/01/16/typo-google-sitemap-fix/index.html)

Here’s how to add those neato Web 2.0 WP Notable icon links in Typo

[Notable social bookmarking/networking for Typo](./blog/2006/09/02/notable-social-bookmarking-networking-for-typo/index.html)

My version also shows how to add them to Typo “pages”
