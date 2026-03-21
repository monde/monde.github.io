---
title: "Typo 4.0 + Apache2 + MySQL + Gentoo"
date: 2006-10-24
categories: [Typo, Rails, Apache]
tags: [apache, rails, typo]
---

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

This article deprecated by my [Maintaining Your Own Typo 4.0.3](./articles/2007/04/08/maintaining-your-own-typo-4-0-3) article.

The section in this article about the apache proxy is flawed, it doesn’t actually balance the load. There is also a better way to craft an init.d script generically for Mongrel in my new article.

I’ll leave the article in place for reference only.

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

I’ve almost completed my Typo 4.0 + Apache2 + MySQL + Gentoo configuration. Some system administration is Gentoo flavored but I think this is a good rececipe for anyone looking to do setup of Typo 4.0 within an Apache2 instance with MySQL for the datasource.

*This is a recipe for configuring Typo 4.0.3 on Gentoo 1.12.4 Linux with Apache2 and MySQL.*

### Index

- [Introduction](#Introduction)
- [Software Versions](#Software_Versions)
- [Tools Preparation](#Tools_Preparation)
- [Mysql Preparation](#Mysql_Preparation)
- [Typo Instance Install And Preparation](#Typo_Instance_Install_And_Preparation)
- [Additional Mysql And Typo Preparation](#Additional_Mysql_And_Typo_Preparation)
- [Typo Configuration](#Typo_Configuration)
- [Apache2 Configuration](#Apache2_Configuration)
- [Apache2 VirtualHost Configuration](#Apache2_VirtualHost_Configuration)
- [RC init.d Script For Typo](#RC_init_d_Script_For_Typo)
- [logrotate](#logrotate)
- [Resouces](#Resouces)

### Introduction

In this server configuration Apache2 will route requests to the **/blog** URI which are then handled by Typo. The ‘typo’ script that its gem installs invokes the Mongrel Ruby/HTTP server to run the typo application. When Apache2 hands off the **/blog** request it is passing it to the Mongrel server. This configuration will give us the best of both worlds of Apache2 and Mongrel. Apache2 is good at handling static files and has many additional modules that can be used for web applications that are not dependant on Mongrel or Typo. The same can be said about Mongrel, its best at serving rails applications and its not dependant on Apache2.

I used the tutorial at the [Dev411](./wiki/Installing_Typo:_MySQL%2C_Apache%2C_lighttpd_and_FastCGI/index.html) site as a starting point to craft this tutorial that is specific to Apache2/MySQL/Rails/Typo on Gentoo. Also [FolkWolf](./blog/pages/installation/index.html) has good notes on Apache2 mod\_proxy routing to Mongrel invoked by the typo script.

### Software Versions

Here are the software versions for the various pieces that make up this system.

```ruby
$ gem list typo
typo (4.0.3)
```

```bash
$ more /etc/gentoo-release
Gentoo Base System version 1.12.4
```

Note: I will use dollar sign ’$’ to denote the start of a shell command. Some of the commands should be run as root or with sudo but I’ll assume you know when to become the super user.

These are the other Gentoo packages that were available to the Typo system that I configured.

- net-www/apache-2.0.58-r2
- dev-db/mysql-4.1.21
- dev-lang/ruby-1.8.4-r3
- dev-ruby/rubygems-0.8.11-r5
- dev-db/sqlite-3.3.5-r1

### Tools Preparation

The basic gem packages needed for typo are:

```ruby
$ gem install --include-dependencies mysql
$ gem install --include-dependencies typo
```

When gem builds typo it creates the typo program/script. The gem command on Gentoo places the ‘typo’ script in */usr/bin* so its in your path. Note, on another Debian system I have the typo gem’s resulting bin directory is **/var/lib/gems/1.8/bin/**

You normally will be using the three rails environments on different systems in your use of Rails and typo. Even though typo is “stable” you should be using a code versioning system or application deployment system to manage your application. [HowtoUseRailsWithSubversion](./rails/pages/HowtoUseRailsWithSubversion/index.html) on the Rails wiki and the Capistrano [Automating Application Deployment](./read/book/17/index.html) are must reads for understanding deployment strategies.

### Mysql Preparation

For convenience sake here’s how to create all three mysql environments at once on a single mysql instance. Prepare the development, test, and production mysql typo database users and databases like so:

```bash
$ mysql -u root -p -h localhost
mysql> create database mysite_com_typodb_development;
mysql> create database mysite_com_typodb_test;
mysql> create database mysite_com_typodb_production;
mysql> grant all on mysite_com_typodb_development.* to typo_dev@localhost identified by 'changeme';
mysql> grant all on mysite_com_typodb_test.* to typo_test@localhost identified by 'changeme';
mysql> grant all on mysite_com_typodb_production.* to typo_prod@localhost identified by 'changeme';
mysql> flush privileges;
mysql> quit;
```

### Typo Instance Install And Preparation

Now we’ll use the typo script that gem placed in the system path to install an instance of typo for our server:

```bash
$ typo install /var/www/mysite_com/typo
```

At this point you’ll see bunch information from typo line by line during its build and installation. Hopefully you don’t get any errors and it will end with the following:

```
 Typo is now running on http://localhost:4093
 Use 'typo start /var/www/mysite_com/typo' to restart after boot.
 Look in installer/*.conf.example to see how to integrate with your web server.
```

For now shut down typo so we can finish installation and configuration of typo on our Apache2/MySQL system.

```bash
$ typo stop /var/www/mysite_com/typo
```

### Additional Mysql And Typo Preparation

Change directory to where you installed typo

```bash
$ cd /var/www/mysite_com/typo
```

Install the MySQL schema for typo for your three instances

```bash
$ mysql -u typo_dev -p mysite_com_typodb_development < db/schema.mysql.sql
$ mysql -u typo_test -p mysite_com_typodb_test < db/schema.mysql.sql
$ mysql -u typo_prod -p mysite_com_typodb_production < db/schema.mysql.sql
```

Backup the default database yaml configuration if you want to save it for future reference.

```bash
$ cp config/database.yml config/database.yml.sqlite
```

Typo installs a database yaml example file that has the mysql adapter (instead of sqlite) as its adapter, use it as the basis of your mysql configuration. Also, the typo yaml shows a nifty technique of using a yaml object for your database credentials and then referencing the object for each environment, development, test, and production. We’ll specify our three environments explicitly.

```bash
$ cp config/database.yml.example config/database.yml
```

Here’s an example:

```
development:
  database: mysite_com_typodb_development
  adapter: mysql
  host: localhost
  username: typo_dev
  password: changeme

test:
  database: mysite_com_typodb_test
  adapter: mysql
  host: localhost
  username: typo_test
  password: changeme

production:
  database: mysite_com_typodb_production
  adapter: mysql
  host: localhost
  username: typo_prod
  password: changeme
```

### Typo Configuration

The typo script has a configuration option to configure your instance of that application. WEBrick runs rails application by default on port 3000. However, we don’t want to clobber that port for others in the future so we are going to run our typo on port 3057. Remember its Mongrel that will be running our typo application and Apache2 will accept requests for **/blog** on port 80 but route those requests to port 3057 on the localhost which Mongrel will answer. Port 3057 should **not** be open to requests from the outside world so be sure to protect your server with a firewall strategy.

Here’s the options used to configure a production typo installation:

```bash
$ typo config /var/www/mysite_com/typo rails-environment=production web-server=mongrel port-number=3057 url-prefix=/blog
```

This configuration will run in production mode, in a mongrel server, on port 3057, and its url base will be **/blog**. Again the **/blog** URL base is that it can coexist withing Apache2’s world. All the of the typo configuration operation options are documented in its gem directory **typo-4.0.3/doc/Installer.txt**.

Start typo now before your Apache2 is configured so that you can set your blog defaults such as the blogs name, etc.

```bash
$ typo start /var/www/mysite_com/typo
```

On your desktop (assuming its not your server) you can forward a port to the server using SSH as the proxy. For instance here is how to forward port 8080 to the server:

```bash
$ ssh -L 8080:localhost:3057 root@www.mysite.com
```

Now open your browser to:

**http://localhost:8080/blog**

and you’ll prompted to do your first time typo configuration.

### Apache2 Configuration

We will use [mod\_proxy](./docs/2.0/mod/mod_proxy.html) to route requests from port 80 of a virtual host to port 3057 on local host. To enable mod\_proxy in Apache2 on Gentoo you need to have a PROXY defined in your **/etc/conf.d/apache2**, such as:

```
APACHE2_OPTS="-D DEFAULT_VHOST -D PHP5 -D FASTCGI -D PROXY" 
```

And in the **/etc/apache2/httpd.conf** you need to configure your PROXY with an IfDefine statement such as:

```bash
<IfDefine PROXY>
    LoadModule proxy_module                  modules/mod_proxy.so
    LoadModule proxy_connect_module          modules/mod_proxy_connect.so
#    LoadModule proxy_ftp_module              modules/mod_proxy_ftp.so
    LoadModule proxy_http_module             modules/mod_proxy_http.so
</IfDefine>
```

### Apache2 VirtualHost Configuration

The minimum virtual host file you need to have Apache2 route **/blog** requests to Mongrel are as follows. You will need to change the specific path and server name details to your installation in
**/etc/apache2/vhosts.d/01\_mysite\_com\_vhost.conf** (or what ever you name your vhost file)

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

This article deprecated by my [Maintaining Your Own Typo 4.0.3](./articles/2007/04/08/maintaining-your-own-typo-4-0-3) article.

The proxy information below doesn’t actually balance the load to the mongrel instance running Typo. Use the new article for reference how to do balancing properly.

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

```bash
# implies NameVirtualHost *:80 in 00_default_vhost.conf
# or httpd.conf
<VirtualHost *:80>
    ServerAdmin webmaster@mysite.com
    DocumentRoot "/var/www/mysite_com/htdocs" 
    ServerName mysite.com

    ErrorLog /var/www/mysite_com/logs/error_log
    CustomLog /var/www/mysite_com/logs/access_log combined

    # lock down your proxy
    ProxyRequests Off
    <Proxy *>
       Order deny,allow
       Allow from all
    </Proxy>
    ProxyPass         /blog http://localhost:3057/blog
    ProxyPassReverse  /blog http://localhost:3057/blog

    # make index rout to the blog
    RedirectMatch ^/$ http://mysite.com/blog/
    RedirectMatch ^$ http://mysite.com/blog/
    RedirectMatch ^index.html$ http://mysite.com/blog/

    <Directory "/var/www/mysite_com/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride None
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
```

Use apache2ctl to make sure you have a good virtual host configuration.

```bash
$ apache2ctl configtest
```

Reload Apache2 after getting a configuration to pass.

```bash
$ /etc/init.d/apache2 reload
```

Now open a web browser to **http://www.mysite.com/** (change to the real name of your site) you should be redirected to **http://www.mysite.com/blog** your bare typo installation. If things are not working tail the Apache2 log and the Mongrel logs to see if you can find answers to your errors there:

```bash
$ tail -f /var/www/mysite_com/logs/error_log
$ tail -f /var/www/mysite_com/typo/log/production.log
```

### RC init.d Script For Typo

We will need a Gentoo system init.d script that loads typo after Apache2. The [Gentoo Wiki](./HOWTO_Make_an_rc_script/index.html) has basic instructions for this. Here’s a bare bones init.d script as **/etc/init.d/typo-mysite\_com**

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

This article deprecated by my [Maintaining Your Own Typo 4.0.3](./articles/2007/04/08/maintaining-your-own-typo-4-0-3) article.

The init.d example below is brutally ugly. Use the new article for reference how to how elegantly create an init.d script for Mongrel generically.

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

```
#!/sbin/runscript
depend() {
        need net
        use mysql apache2
        after apache2
}

start() {
        ebegin "Starting typo for mysite.com" 
        typo start /var/www/mysite_com/typo
        eend $?
}

stop() {
        ebegin "Stopping typo for mysite.com" 
        typo stop /var/www/mysite_com/typo
        eend $?
}

reload() {
        ebegin "Restarting typo for mysite.com" 
        typo restart /var/www/mysite_com/typo
        eend $?
}
```

Add rc links to your init.d script with the rc-update command

```bash
$ rc-update add typo-mysite_com default
```

### logrotate

A logrotate snippet should be added to your logrotate.d directory if you are using logrotate on your system, something like the following in **/etc/logrotate.d/typo-mysite\_com**

```bash
# typo logrotate snipet for Gentoo Linux
/var/www/mysite_com/typo/log/*.log {
  missingok
  notifempty
  sharedscripts
  postrotate
  /etc/init.d/typo-mysite_com restart > /dev/null 2>&1 || true
  endscript
}
```

*Note*: I’m not entirely convinced this is the best logrotate script for typo, I’ll update this post of if find something better.

### Resouces

- [Dev411](./wiki/Installing_Typo:_MySQL%2C_Apache%2C_lighttpd_and_FastCGI/index.html)
- [HowtoUseRailsWithSubversion](./rails/pages/HowtoUseRailsWithSubversion/index.html)
- [Capistrano/Ruby Application Deployment](./read/book/17/index.html)
- [FolkWolf’’s Apache2+Typo4.0 Config](./blog/pages/installation/index.html)
- [Apache2 mod\_proxy](./docs/2.0/mod/mod_proxy.html)
- [Gentoo RC init.d scripts](./HOWTO_Make_an_rc_script/index.html)

*This is a recipe for configuring Typo 4.0.3 on Gentoo 1.12.4 Linux with Apache2 and MySQL.*

### Index

- [Introduction](#Introduction)
- [Software Versions](#Software_Versions)
- [Tools Preparation](#Tools_Preparation)
- [Mysql Preparation](#Mysql_Preparation)
- [Typo Instance Install And Preparation](#Typo_Instance_Install_And_Preparation)
- [Additional Mysql And Typo Preparation](#Additional_Mysql_And_Typo_Preparation)
- [Typo Configuration](#Typo_Configuration)
- [Apache2 Configuration](#Apache2_Configuration)
- [Apache2 VirtualHost Configuration](#Apache2_VirtualHost_Configuration)
- [RC init.d Script For Typo](#RC_init_d_Script_For_Typo)
- [logrotate](#logrotate)
- [Resouces](#Resouces)

### Introduction

In this server configuration Apache2 will route requests to the **/blog** URI which are then handled by Typo. The ‘typo’ script that its gem installs invokes the Mongrel Ruby/HTTP server to run the typo application. When Apache2 hands off the **/blog** request it is passing it to the Mongrel server. This configuration will give us the best of both worlds of Apache2 and Mongrel. Apache2 is good at handling static files and has many additional modules that can be used for web applications that are not dependant on Mongrel or Typo. The same can be said about Mongrel, its best at serving rails applications and its not dependant on Apache2.

I used the tutorial at the [Dev411](./wiki/Installing_Typo:_MySQL%2C_Apache%2C_lighttpd_and_FastCGI/index.html) site as a starting point to craft this tutorial that is specific to Apache2/MySQL/Rails/Typo on Gentoo. Also [FolkWolf](./blog/pages/installation/index.html) has good notes on Apache2 mod\_proxy routing to Mongrel invoked by the typo script.

### Software Versions

Here are the software versions for the various pieces that make up this system.

```ruby
$ gem list typo
typo (4.0.3)
```

```bash
$ more /etc/gentoo-release
Gentoo Base System version 1.12.4
```

Note: I will use dollar sign ’$’ to denote the start of a shell command. Some of the commands should be run as root or with sudo but I’ll assume you know when to become the super user.

These are the other Gentoo packages that were available to the Typo system that I configured.

- net-www/apache-2.0.58-r2
- dev-db/mysql-4.1.21
- dev-lang/ruby-1.8.4-r3
- dev-ruby/rubygems-0.8.11-r5
- dev-db/sqlite-3.3.5-r1

### Tools Preparation

The basic gem packages needed for typo are:

```ruby
$ gem install --include-dependencies mysql
$ gem install --include-dependencies typo
```

When gem builds typo it creates the typo program/script. The gem command on Gentoo places the ‘typo’ script in */usr/bin* so its in your path. Note, on another Debian system I have the typo gem’s resulting bin directory is **/var/lib/gems/1.8/bin/**

You normally will be using the three rails environments on different systems in your use of Rails and typo. Even though typo is “stable” you should be using a code versioning system or application deployment system to manage your application. [HowtoUseRailsWithSubversion](./rails/pages/HowtoUseRailsWithSubversion/index.html) on the Rails wiki and the Capistrano [Automating Application Deployment](./read/book/17/index.html) are must reads for understanding deployment strategies.

### Mysql Preparation

For convenience sake here’s how to create all three mysql environments at once on a single mysql instance. Prepare the development, test, and production mysql typo database users and databases like so:

```bash
$ mysql -u root -p -h localhost
mysql> create database mysite_com_typodb_development;
mysql> create database mysite_com_typodb_test;
mysql> create database mysite_com_typodb_production;
mysql> grant all on mysite_com_typodb_development.* to typo_dev@localhost identified by 'changeme';
mysql> grant all on mysite_com_typodb_test.* to typo_test@localhost identified by 'changeme';
mysql> grant all on mysite_com_typodb_production.* to typo_prod@localhost identified by 'changeme';
mysql> flush privileges;
mysql> quit;
```

### Typo Instance Install And Preparation

Now we’ll use the typo script that gem placed in the system path to install an instance of typo for our server:

```bash
$ typo install /var/www/mysite_com/typo
```

At this point you’ll see bunch information from typo line by line during its build and installation. Hopefully you don’t get any errors and it will end with the following:

```
 Typo is now running on http://localhost:4093
 Use 'typo start /var/www/mysite_com/typo' to restart after boot.
 Look in installer/*.conf.example to see how to integrate with your web server.
```

For now shut down typo so we can finish installation and configuration of typo on our Apache2/MySQL system.

```bash
$ typo stop /var/www/mysite_com/typo
```

### Additional Mysql And Typo Preparation

Change directory to where you installed typo

```bash
$ cd /var/www/mysite_com/typo
```

Install the MySQL schema for typo for your three instances

```bash
$ mysql -u typo_dev -p mysite_com_typodb_development < db/schema.mysql.sql
$ mysql -u typo_test -p mysite_com_typodb_test < db/schema.mysql.sql
$ mysql -u typo_prod -p mysite_com_typodb_production < db/schema.mysql.sql
```

Backup the default database yaml configuration if you want to save it for future reference.

```bash
$ cp config/database.yml config/database.yml.sqlite
```

Typo installs a database yaml example file that has the mysql adapter (instead of sqlite) as its adapter, use it as the basis of your mysql configuration. Also, the typo yaml shows a nifty technique of using a yaml object for your database credentials and then referencing the object for each environment, development, test, and production. We’ll specify our three environments explicitly.

```bash
$ cp config/database.yml.example config/database.yml
```

Here’s an example:

```
development:
  database: mysite_com_typodb_development
  adapter: mysql
  host: localhost
  username: typo_dev
  password: changeme

test:
  database: mysite_com_typodb_test
  adapter: mysql
  host: localhost
  username: typo_test
  password: changeme

production:
  database: mysite_com_typodb_production
  adapter: mysql
  host: localhost
  username: typo_prod
  password: changeme
```

### Typo Configuration

The typo script has a configuration option to configure your instance of that application. WEBrick runs rails application by default on port 3000. However, we don’t want to clobber that port for others in the future so we are going to run our typo on port 3057. Remember its Mongrel that will be running our typo application and Apache2 will accept requests for **/blog** on port 80 but route those requests to port 3057 on the localhost which Mongrel will answer. Port 3057 should **not** be open to requests from the outside world so be sure to protect your server with a firewall strategy.

Here’s the options used to configure a production typo installation:

```bash
$ typo config /var/www/mysite_com/typo rails-environment=production web-server=mongrel port-number=3057 url-prefix=/blog
```

This configuration will run in production mode, in a mongrel server, on port 3057, and its url base will be **/blog**. Again the **/blog** URL base is that it can coexist withing Apache2’s world. All the of the typo configuration operation options are documented in its gem directory **typo-4.0.3/doc/Installer.txt**.

Start typo now before your Apache2 is configured so that you can set your blog defaults such as the blogs name, etc.

```bash
$ typo start /var/www/mysite_com/typo
```

On your desktop (assuming its not your server) you can forward a port to the server using SSH as the proxy. For instance here is how to forward port 8080 to the server:

```bash
$ ssh -L 8080:localhost:3057 root@www.mysite.com
```

Now open your browser to:

**http://localhost:8080/blog**

and you’ll prompted to do your first time typo configuration.

### Apache2 Configuration

We will use [mod\_proxy](./docs/2.0/mod/mod_proxy.html) to route requests from port 80 of a virtual host to port 3057 on local host. To enable mod\_proxy in Apache2 on Gentoo you need to have a PROXY defined in your **/etc/conf.d/apache2**, such as:

```
APACHE2_OPTS="-D DEFAULT_VHOST -D PHP5 -D FASTCGI -D PROXY" 
```

And in the **/etc/apache2/httpd.conf** you need to configure your PROXY with an IfDefine statement such as:

```bash
<IfDefine PROXY>
    LoadModule proxy_module                  modules/mod_proxy.so
    LoadModule proxy_connect_module          modules/mod_proxy_connect.so
#    LoadModule proxy_ftp_module              modules/mod_proxy_ftp.so
    LoadModule proxy_http_module             modules/mod_proxy_http.so
</IfDefine>
```

### Apache2 VirtualHost Configuration

The minimum virtual host file you need to have Apache2 route **/blog** requests to Mongrel are as follows. You will need to change the specific path and server name details to your installation in
**/etc/apache2/vhosts.d/01\_mysite\_com\_vhost.conf** (or what ever you name your vhost file)

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

This article deprecated by my [Maintaining Your Own Typo 4.0.3](./articles/2007/04/08/maintaining-your-own-typo-4-0-3) article.

The proxy information below doesn’t actually balance the load to the mongrel instance running Typo. Use the new article for reference how to do balancing properly.

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

```bash
# implies NameVirtualHost *:80 in 00_default_vhost.conf
# or httpd.conf
<VirtualHost *:80>
    ServerAdmin webmaster@mysite.com
    DocumentRoot "/var/www/mysite_com/htdocs" 
    ServerName mysite.com

    ErrorLog /var/www/mysite_com/logs/error_log
    CustomLog /var/www/mysite_com/logs/access_log combined

    # lock down your proxy
    ProxyRequests Off
    <Proxy *>
       Order deny,allow
       Allow from all
    </Proxy>
    ProxyPass         /blog http://localhost:3057/blog
    ProxyPassReverse  /blog http://localhost:3057/blog

    # make index rout to the blog
    RedirectMatch ^/$ http://mysite.com/blog/
    RedirectMatch ^$ http://mysite.com/blog/
    RedirectMatch ^index.html$ http://mysite.com/blog/

    <Directory "/var/www/mysite_com/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride None
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
```

Use apache2ctl to make sure you have a good virtual host configuration.

```bash
$ apache2ctl configtest
```

Reload Apache2 after getting a configuration to pass.

```bash
$ /etc/init.d/apache2 reload
```

Now open a web browser to **http://www.mysite.com/** (change to the real name of your site) you should be redirected to **http://www.mysite.com/blog** your bare typo installation. If things are not working tail the Apache2 log and the Mongrel logs to see if you can find answers to your errors there:

```bash
$ tail -f /var/www/mysite_com/logs/error_log
$ tail -f /var/www/mysite_com/typo/log/production.log
```

### RC init.d Script For Typo

We will need a Gentoo system init.d script that loads typo after Apache2. The [Gentoo Wiki](./HOWTO_Make_an_rc_script/index.html) has basic instructions for this. Here’s a bare bones init.d script as **/etc/init.d/typo-mysite\_com**

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

This article deprecated by my [Maintaining Your Own Typo 4.0.3](./articles/2007/04/08/maintaining-your-own-typo-4-0-3) article.

The init.d example below is brutally ugly. Use the new article for reference how to how elegantly create an init.d script for Mongrel generically.

**IMPORTANT!!!** **IMPORTANT!!!** **IMPORTANT!!!**

```
#!/sbin/runscript
depend() {
        need net
        use mysql apache2
        after apache2
}

start() {
        ebegin "Starting typo for mysite.com" 
        typo start /var/www/mysite_com/typo
        eend $?
}

stop() {
        ebegin "Stopping typo for mysite.com" 
        typo stop /var/www/mysite_com/typo
        eend $?
}

reload() {
        ebegin "Restarting typo for mysite.com" 
        typo restart /var/www/mysite_com/typo
        eend $?
}
```

Add rc links to your init.d script with the rc-update command

```bash
$ rc-update add typo-mysite_com default
```

### logrotate

A logrotate snippet should be added to your logrotate.d directory if you are using logrotate on your system, something like the following in **/etc/logrotate.d/typo-mysite\_com**

```bash
# typo logrotate snipet for Gentoo Linux
/var/www/mysite_com/typo/log/*.log {
  missingok
  notifempty
  sharedscripts
  postrotate
  /etc/init.d/typo-mysite_com restart > /dev/null 2>&1 || true
  endscript
}
```

*Note*: I’m not entirely convinced this is the best logrotate script for typo, I’ll update this post of if find something better.

### Resouces

- [Dev411](./wiki/Installing_Typo:_MySQL%2C_Apache%2C_lighttpd_and_FastCGI/index.html)
- [HowtoUseRailsWithSubversion](./rails/pages/HowtoUseRailsWithSubversion/index.html)
- [Capistrano/Ruby Application Deployment](./read/book/17/index.html)
- [FolkWolf’’s Apache2+Typo4.0 Config](./blog/pages/installation/index.html)
- [Apache2 mod\_proxy](./docs/2.0/mod/mod_proxy.html)
- [Gentoo RC init.d scripts](./HOWTO_Make_an_rc_script/index.html)
