---
title: "compiling ruby 1.8.5 w/ openssl on Debian (Etch/testing) and FreeBSD in $HOME"
date: 2007-02-03
categories: [Linux, Ruby, Rails, Nuby Rails]
tags: [rails, ruby]
---

If you want to have control over the version of ruby that is available in your user space here’s how to build and install it in your $HOME directory. The Debian Way of packaging ruby and gem deviates from the Ruby Way on other Nix platforms. So its better to just do it Your Way so that you have control of which ruby and ruby tools (gem, rake, rails, etc.) is available to your user environment.

This is a way to compile and install ruby 1.8.5 with local dependency on openssl, readline, and openssl on Debian (Etch/testing) 686 in your $HOME directory. The method also works for FreeBSD 4.8-STABLE. (BTW if you have root privilege on your machine and you just want to enable openssl to your already installed ruby make sure the libopenssl-ruby Debian package is installed and ignore the rest of the knowledge presented here.)

In googling around to find out how to do this I noticed that often people would break readline support when adding openssl support building their local ruby. I also wanted to have control over the version of ruby running on a hosting account I have at pair.com. My host account has ruby 1.8.4 installed on a FreeBSD 4.8-STABLE machine. Some FreeBSD builds of ruby have problems with broken iconv support (needed by the TMail library that is used in parsing email in ActionMailer). The technique I’m about to discuss will show how to deal with that as well.

On pages 35-36 [Agile Web Development with Rails](./titles/rails/index.html) section “3.4 Installing on Linux” Dave Thomas also describes building a local copy of ruby in the $HOME directory of accounts he has on Linux. We’ll do that and also build a local gem as well.

First make sure the environment of your shell (in the example here its bash) has $HOME/bin in its path and the system library environment variable set with $HOME/lib . Place these export commands at the end of your $HOME/.bashrc and then source your updated bashrc into the current environment after your changes are saved.

```ruby
#this is at the end of $HOME/.bashrc
export PATH=$HOME/bin:$PATH
export MAN_PATH=$HOME/man
export LD_LIBRARY_PATH=$HOME/lib:/usr/local/lib:/usr/lib
#the gem portion
export PATH=$HOME/gems/bin:$PATH
export GEM_PATH=$HOME/gems
export GEM_HOME=$HOME/gems
```

Now source your updated .bashrc into your current environment

```
. ~/.bashrc
```

Create a directory called builds in your $HOME (or somewhere that you want to do your builds). Change into that directory and download the ruby, iconv, openssl, and readline sources (check for the latest versions when you do this). Then extract each archive.

```bash
mkdir $HOME/builds
cd $HOME/builds
wget ftp://ftp.cwru.edu/pub/bash/readline-5.2.tar.gz
wget http://www.openssl.org/source/openssl-0.9.8d.tar.gz
wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.11.tar.gz
wget ftp://ftp.ruby-lang.org/pub/ruby/ruby-1.8.5.tar.gz
wget http://rubyforge.org/frs/download.php/11289/rubygems-0.9.0.tgz
tar xzf readline-5.2.tar.gz
tar xzf openssl-0.9.8d.tar.gz
tar xzf libiconv-1.11.tar.gz
tar xzf ruby-1.8.5.tar.gz
tar xzf rubygems-0.9.0.tgz
```

Now build each library, then ruby, we’ll install gem later at the end.

OpenSSL

```bash
cd $HOME/builds/openssl-0.9.8d
./config --prefix=$HOME --openssldir=$HOME/openssl shared
make
make test
make install
```

ReadLine Library

```bash
cd $HOME/builds/readline-5.2
./configure --prefix=$HOME
make
make install
```

Iconv library

```bash
cd $HOME/builds/libiconv-1.11
./configure --prefix=$HOME
make
make install
```

Ruby for Debian and FreeBSD. I think not having libncurses5-dev installed on the host system will affect the build of readline support. If you don’t have libncurses.so in /usr/lib or /usr/local/lib then you’ll have to build it locally (as with the other libraries) and include it as a—with-ncurses-dir=$HOME parameter to configure. If you don’t see libreadline.so in the ldd output (below) then you’ll have install your own local libncurses.so library.

```bash
cd $HOME/builds/ruby-1.8.5
./configure --prefix=$HOME --with-static-linked-ext --with-iconv-dir=$HOME --with-openssl-dir=$HOME --with-readline-dir=$HOME
make
make test
make install
```

As you can see the local version of ruby is installed and is using the local openssl, readline, and iconv libraries.

```bash
mike@lab ~/builds/ruby-1.8.5$ which ruby
/home/mike/bin/ruby
mike@lab ~/builds/ruby-1.8.5$ ruby --version
ruby 1.8.5 (2006-08-25) [i686-linux]
mike@lab ~/builds/ruby-1.8.5$ ldd $HOME/bin/ruby
        linux-gate.so.1 =>  (0xffffe000)
        libdl.so.2 => /lib/tls/i686/cmov/libdl.so.2 (0xa7f55000)
        libcrypt.so.1 => /lib/tls/i686/cmov/libcrypt.so.1 (0xa7f26000)
        libm.so.6 => /lib/tls/i686/cmov/libm.so.6 (0xa7f01000)
        libreadline.so.5 => /home/mike/lib/libreadline.so.5 (0xa7ed4000)
        libncurses.so.5 => /usr/lib/libncurses.so.5 (0xa7e93000)
        libssl.so.0.9.8 => /home/mike/lib/libssl.so.0.9.8 (0xa7e59000)
        libcrypto.so.0.9.8 => /home/mike/lib/libcrypto.so.0.9.8 (0xa7d30000)
        libiconv.so.2 => /home/mike/lib/libiconv.so.2 (0xa7c51000)
        libutil.so.1 => /lib/tls/i686/cmov/libutil.so.1 (0xa7c4d000)
        libz.so.1 => /usr/lib/libz.so.1 (0xa7c39000)
        libc.so.6 => /lib/tls/i686/cmov/libc.so.6 (0xa7b08000)
        /lib/ld-linux.so.2 (0xa7f72000)
```

This is how to set up your local gems.

```bash
mkdir $HOME/gems
cd $HOME/builds/rubygems-0.9.0
ruby setup.rb all --prefix=$HOME
```

Make sure its working

```ruby
mike@lab ~/builds/rubygems-0.9.0$ gem environment
Rubygems Environment:
  - VERSION: 0.9.0 (0.9.0)
  - INSTALLATION DIRECTORY: /home/mike/gems
  - GEM PATH:
     - /home/mike/gems
  - REMOTE SOURCES:
     - http://gems.rubyforge.org
mike@lab ~/builds/rubygems-0.9.0$ gem list --local

*** LOCAL GEMS ***

sources (0.0.1)
    This package provides download sources for remote gem installation
```

Install rails and the rails command will be in your path as $HOME/gems/bin/rails. The include dependencies flag will cause rails, rake, activesupport, activerecord, actionpack, actionmailer, and actionwebservice to be installed.

```ruby
gem install --remote --rdoc --ri --include-dependencies rails
gem list --local
```

Run gem\_server to view your freshly minted documentation.

In googling around to find out how to do this I noticed that often people would break readline support when adding openssl support building their local ruby. I also wanted to have control over the version of ruby running on a hosting account I have at pair.com. My host account has ruby 1.8.4 installed on a FreeBSD 4.8-STABLE machine. Some FreeBSD builds of ruby have problems with broken iconv support (needed by the TMail library that is used in parsing email in ActionMailer). The technique I’m about to discuss will show how to deal with that as well.

On pages 35-36 [Agile Web Development with Rails](./titles/rails/index.html) section “3.4 Installing on Linux” Dave Thomas also describes building a local copy of ruby in the $HOME directory of accounts he has on Linux. We’ll do that and also build a local gem as well.

First make sure the environment of your shell (in the example here its bash) has $HOME/bin in its path and the system library environment variable set with $HOME/lib . Place these export commands at the end of your $HOME/.bashrc and then source your updated bashrc into the current environment after your changes are saved.

```ruby
#this is at the end of $HOME/.bashrc
export PATH=$HOME/bin:$PATH
export MAN_PATH=$HOME/man
export LD_LIBRARY_PATH=$HOME/lib:/usr/local/lib:/usr/lib
#the gem portion
export PATH=$HOME/gems/bin:$PATH
export GEM_PATH=$HOME/gems
export GEM_HOME=$HOME/gems
```

Now source your updated .bashrc into your current environment

```
. ~/.bashrc
```

Create a directory called builds in your $HOME (or somewhere that you want to do your builds). Change into that directory and download the ruby, iconv, openssl, and readline sources (check for the latest versions when you do this). Then extract each archive.

```bash
mkdir $HOME/builds
cd $HOME/builds
wget ftp://ftp.cwru.edu/pub/bash/readline-5.2.tar.gz
wget http://www.openssl.org/source/openssl-0.9.8d.tar.gz
wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.11.tar.gz
wget ftp://ftp.ruby-lang.org/pub/ruby/ruby-1.8.5.tar.gz
wget http://rubyforge.org/frs/download.php/11289/rubygems-0.9.0.tgz
tar xzf readline-5.2.tar.gz
tar xzf openssl-0.9.8d.tar.gz
tar xzf libiconv-1.11.tar.gz
tar xzf ruby-1.8.5.tar.gz
tar xzf rubygems-0.9.0.tgz
```

Now build each library, then ruby, we’ll install gem later at the end.

OpenSSL

```bash
cd $HOME/builds/openssl-0.9.8d
./config --prefix=$HOME --openssldir=$HOME/openssl shared
make
make test
make install
```

ReadLine Library

```bash
cd $HOME/builds/readline-5.2
./configure --prefix=$HOME
make
make install
```

Iconv library

```bash
cd $HOME/builds/libiconv-1.11
./configure --prefix=$HOME
make
make install
```

Ruby for Debian and FreeBSD. I think not having libncurses5-dev installed on the host system will affect the build of readline support. If you don’t have libncurses.so in /usr/lib or /usr/local/lib then you’ll have to build it locally (as with the other libraries) and include it as a—with-ncurses-dir=$HOME parameter to configure. If you don’t see libreadline.so in the ldd output (below) then you’ll have install your own local libncurses.so library.

```bash
cd $HOME/builds/ruby-1.8.5
./configure --prefix=$HOME --with-static-linked-ext --with-iconv-dir=$HOME --with-openssl-dir=$HOME --with-readline-dir=$HOME
make
make test
make install
```

As you can see the local version of ruby is installed and is using the local openssl, readline, and iconv libraries.

```bash
mike@lab ~/builds/ruby-1.8.5$ which ruby
/home/mike/bin/ruby
mike@lab ~/builds/ruby-1.8.5$ ruby --version
ruby 1.8.5 (2006-08-25) [i686-linux]
mike@lab ~/builds/ruby-1.8.5$ ldd $HOME/bin/ruby
        linux-gate.so.1 =>  (0xffffe000)
        libdl.so.2 => /lib/tls/i686/cmov/libdl.so.2 (0xa7f55000)
        libcrypt.so.1 => /lib/tls/i686/cmov/libcrypt.so.1 (0xa7f26000)
        libm.so.6 => /lib/tls/i686/cmov/libm.so.6 (0xa7f01000)
        libreadline.so.5 => /home/mike/lib/libreadline.so.5 (0xa7ed4000)
        libncurses.so.5 => /usr/lib/libncurses.so.5 (0xa7e93000)
        libssl.so.0.9.8 => /home/mike/lib/libssl.so.0.9.8 (0xa7e59000)
        libcrypto.so.0.9.8 => /home/mike/lib/libcrypto.so.0.9.8 (0xa7d30000)
        libiconv.so.2 => /home/mike/lib/libiconv.so.2 (0xa7c51000)
        libutil.so.1 => /lib/tls/i686/cmov/libutil.so.1 (0xa7c4d000)
        libz.so.1 => /usr/lib/libz.so.1 (0xa7c39000)
        libc.so.6 => /lib/tls/i686/cmov/libc.so.6 (0xa7b08000)
        /lib/ld-linux.so.2 (0xa7f72000)
```

This is how to set up your local gems.

```bash
mkdir $HOME/gems
cd $HOME/builds/rubygems-0.9.0
ruby setup.rb all --prefix=$HOME
```

Make sure its working

```ruby
mike@lab ~/builds/rubygems-0.9.0$ gem environment
Rubygems Environment:
  - VERSION: 0.9.0 (0.9.0)
  - INSTALLATION DIRECTORY: /home/mike/gems
  - GEM PATH:
     - /home/mike/gems
  - REMOTE SOURCES:
     - http://gems.rubyforge.org
mike@lab ~/builds/rubygems-0.9.0$ gem list --local

*** LOCAL GEMS ***

sources (0.0.1)
    This package provides download sources for remote gem installation
```

Install rails and the rails command will be in your path as $HOME/gems/bin/rails. The include dependencies flag will cause rails, rake, activesupport, activerecord, actionpack, actionmailer, and actionwebservice to be installed.

```ruby
gem install --remote --rdoc --ri --include-dependencies rails
gem list --local
```

Run gem\_server to view your freshly minted documentation.
