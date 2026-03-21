---
title: "Subversion + Rails In Five Minutes"
date: 2006-11-05
categories: [Rails, Nuby Rails, Subversion]
tags: [nuby, rails, subversion]
---

This is a quick set of subversion commands to create a repository for your Rails application. The repository is dedicated to your Rails app so the head of your source will be in the trunk, version releases will be in tags, and branches for you code base will be in branches.

Nicholas Evan’s [Subversion In Fifteen Minutes](./wp-content/uploads/2006/05/subversion.html) is a good reference for quick subversion setup, what your getting here is the 5 minute version with Rails specifics. The [HowtoUseRailsWithSubversion](./rails/pages/HowtoUseRailsWithSubversion/index.html) page at RubyOnRails goes into more detail about additional things to consider when sharing a Rails project across many developers (like how you might handle database.yml for example).

First, create the project directory structure with svnadmin, the path given is not where you actually edit your source code. **Important** notice the difference between these two paths:

*/path/to/repository*

*/path/to/source/code*

the first is the path to your repository, the second is the path to where you edit your code. Also keep an eye out for the “*trunk*” directory in the Subversion URLs.

```bash
$ svnadmin create /path/to/repository
```

Here’s the URL to the head of the repository on your local machine.

file:///path/to/source/code/trunk

Here’s how it might look from a remote machine using SSH to connect to your repository.

svn+ssh://mike@foo.myserver.com/path/to/source/code/trunk

Now create the trunk, tags, and branches directories:

```bash
$ svn mkdir --message="Creating my project's repository ..." file:///path/to/project/trunk file:///path/to/project/tags file:///path/to/project/branches
```

Now cd to where the source code for your project is residing:

```bash
$ cd /path/to/source/code
```

Now import your existing source into your new repository. If you have already been working on your rails app and running it with the server script delete the \* .logs from the logs directory and delete everything in the tmp directory (files and sub-directories like cache, sessions, sockets, etc.). I’ll show how to make subversion ignore the tmp and log directories after we have checked out our project the first time. Here’s the import command (notice the ’.’ dot after import that means everything in the local directory).

```bash
$ svn import . file:///path/to/source/code/trunk -m "Importing the existing code for my rails project" 
```

Now double check that the import worked, cd .. one directory up to the parent directory. Move your “code” directory to “code.old” (change code with your real project’s directory name)

```bash
$ mv code code.old
$ svn checkout file:///path/to/source/code/trunk code
```

What you just did is asked subversion to fetch the current version of your source code (some call this this the ‘head’ of the mainline of the code i.e. the ‘trunk’) into a directory called ‘code’. Now move to the ‘code’ directory you just checked out.

```bash
$ cd code
```

Now that you are in the directory that you checked out from Subversion, Subversion will know how to treat your commands without having to provide the URL to the repository. Here are the commands to make subversion ignore the log and tmp directory. You should see what the RubyOnRails page says about this as well because it goes into some other details about a strategy for handling the database.yml and config directory.

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

Try out looking at the subversion log for the project to make sure it all really worked, again note that the svn command doesn’t require a URL now.

```bash
$ svn log .
------------------------------------------------------------------------
r2 | mike | 2006-11-05 11:32:41 -0800 (Sun, 05 Nov 2006) | 1 line

Importing the existing code for my rails project
------------------------------------------------------------------------
r1 | mike | 2006-11-05 11:31:17 -0800 (Sun, 05 Nov 2006) | 1 line

Creating my project's repository ...
------------------------------------------------------------------------
$ svn log log/
------------------------------------------------------------------------
r3 | mike | 2006-11-05 11:35:33 -0800 (Sun, 05 Nov 2006) | 1 line

Ignoring all files in /log/ ending in .log
------------------------------------------------------------------------
r2 | mike | 2006-11-05 11:32:41 -0800 (Sun, 05 Nov 2006) | 1 line

Importing the existing code for my rails project
------------------------------------------------------------------------
$ svn log tmp/
------------------------------------------------------------------------
r4 | mike | 2006-11-05 11:37:14 -0800 (Sun, 05 Nov 2006) | 1 line

ignore tmp/ content from now on
------------------------------------------------------------------------
r2 | mike | 2006-11-05 11:32:41 -0800 (Sun, 05 Nov 2006) | 1 line

Importing the existing code for my rails project
------------------------------------------------------------------------
```

Enjoy, have fun.

**Extra cool guy tip**

When you have a working/stable version of your code that you will release you should tag it. What that means is that you can continue to add new code/features to the head of your source but that you’ll have a reference back to the code as it was when you released a particular version. Here’s tagging the COOL-V2.0 release (back slashes are line wrap or continuation characters in the command shell):

```bash
$ svn copy file:///path/to/source/code/trunk \
         file:///path/to/source/code/tags/COOL-V2.0 \
         -m "Tagging the 2.0 release of cool code" 
```

And at a later time here’s checking out a copy of the COOL-V2.0 version:

```bash
$ svn checkout file:///path/to/source/code/tags/COOL-V2.0 code-2.0
```

**Extra cool guy tip #2**

Chris on ERR THE BLOG announced the release of [sake](./post/6069/index.html) a universal rake task tool. In his post he shows a SVN rake task [svn.rake](./73224.txt) that does the processing of the your Rails project as above after you have checked out your first copy of the project.

First, create the project directory structure with svnadmin, the path given is not where you actually edit your source code. **Important** notice the difference between these two paths:

*/path/to/repository*

*/path/to/source/code*

the first is the path to your repository, the second is the path to where you edit your code. Also keep an eye out for the “*trunk*” directory in the Subversion URLs.

```bash
$ svnadmin create /path/to/repository
```

Here’s the URL to the head of the repository on your local machine.

file:///path/to/source/code/trunk

Here’s how it might look from a remote machine using SSH to connect to your repository.

svn+ssh://mike@foo.myserver.com/path/to/source/code/trunk

Now create the trunk, tags, and branches directories:

```bash
$ svn mkdir --message="Creating my project's repository ..." file:///path/to/project/trunk file:///path/to/project/tags file:///path/to/project/branches
```

Now cd to where the source code for your project is residing:

```bash
$ cd /path/to/source/code
```

Now import your existing source into your new repository. If you have already been working on your rails app and running it with the server script delete the \* .logs from the logs directory and delete everything in the tmp directory (files and sub-directories like cache, sessions, sockets, etc.). I’ll show how to make subversion ignore the tmp and log directories after we have checked out our project the first time. Here’s the import command (notice the ’.’ dot after import that means everything in the local directory).

```bash
$ svn import . file:///path/to/source/code/trunk -m "Importing the existing code for my rails project" 
```

Now double check that the import worked, cd .. one directory up to the parent directory. Move your “code” directory to “code.old” (change code with your real project’s directory name)

```bash
$ mv code code.old
$ svn checkout file:///path/to/source/code/trunk code
```

What you just did is asked subversion to fetch the current version of your source code (some call this this the ‘head’ of the mainline of the code i.e. the ‘trunk’) into a directory called ‘code’. Now move to the ‘code’ directory you just checked out.

```bash
$ cd code
```

Now that you are in the directory that you checked out from Subversion, Subversion will know how to treat your commands without having to provide the URL to the repository. Here are the commands to make subversion ignore the log and tmp directory. You should see what the RubyOnRails page says about this as well because it goes into some other details about a strategy for handling the database.yml and config directory.

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

Try out looking at the subversion log for the project to make sure it all really worked, again note that the svn command doesn’t require a URL now.

```bash
$ svn log .
------------------------------------------------------------------------
r2 | mike | 2006-11-05 11:32:41 -0800 (Sun, 05 Nov 2006) | 1 line

Importing the existing code for my rails project
------------------------------------------------------------------------
r1 | mike | 2006-11-05 11:31:17 -0800 (Sun, 05 Nov 2006) | 1 line

Creating my project's repository ...
------------------------------------------------------------------------
$ svn log log/
------------------------------------------------------------------------
r3 | mike | 2006-11-05 11:35:33 -0800 (Sun, 05 Nov 2006) | 1 line

Ignoring all files in /log/ ending in .log
------------------------------------------------------------------------
r2 | mike | 2006-11-05 11:32:41 -0800 (Sun, 05 Nov 2006) | 1 line

Importing the existing code for my rails project
------------------------------------------------------------------------
$ svn log tmp/
------------------------------------------------------------------------
r4 | mike | 2006-11-05 11:37:14 -0800 (Sun, 05 Nov 2006) | 1 line

ignore tmp/ content from now on
------------------------------------------------------------------------
r2 | mike | 2006-11-05 11:32:41 -0800 (Sun, 05 Nov 2006) | 1 line

Importing the existing code for my rails project
------------------------------------------------------------------------
```

Enjoy, have fun.

**Extra cool guy tip**

When you have a working/stable version of your code that you will release you should tag it. What that means is that you can continue to add new code/features to the head of your source but that you’ll have a reference back to the code as it was when you released a particular version. Here’s tagging the COOL-V2.0 release (back slashes are line wrap or continuation characters in the command shell):

```bash
$ svn copy file:///path/to/source/code/trunk \
         file:///path/to/source/code/tags/COOL-V2.0 \
         -m "Tagging the 2.0 release of cool code" 
```

And at a later time here’s checking out a copy of the COOL-V2.0 version:

```bash
$ svn checkout file:///path/to/source/code/tags/COOL-V2.0 code-2.0
```

**Extra cool guy tip #2**

Chris on ERR THE BLOG announced the release of [sake](./post/6069/index.html) a universal rake task tool. In his post he shows a SVN rake task [svn.rake](./73224.txt) that does the processing of the your Rails project as above after you have checked out your first copy of the project.
